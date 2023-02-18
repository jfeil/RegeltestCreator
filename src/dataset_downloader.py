import asyncio
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import List

import aiohttp
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QDialog
from bs4 import BeautifulSoup

from src.ui_dataset_download_dialog import Ui_DownloadDialog
from src.ui_downloader import Ui_DownloadProgress


@dataclass
class QuestionJSON:
    group_id: int
    question_id: int
    question: str
    answer_index: int
    answer_text: str
    created: str
    last_edited: str
    multiple_choice: List[str]

    def toDict(self):
        return {
            "group_id": self.group_id,
            "question_id": self.question_id,
            "question": self.question,
            "answer_index": self.answer_index,
            "answer_text": self.answer_text,
            "created": self.created,
            "last_edited": self.last_edited,
            "multiple_choice": self.multiple_choice
        }


@dataclass
class QuestionGroupJSON:
    id: int
    name: str

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class LoginFailedException(Exception):
    pass


class DatasetDownloadDialog(QDialog, Ui_DownloadDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_DownloadDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Quelle auswählen")

        self.ui.source_combobox.addItem("bfv.sr-regeltest.de")
        self.ui.buttonBox.accepted.connect(self.download_data)
        self.session = None

        self.data = None

        self.download_progress = 0
        self.max_items = -1

        self.downloader = None

    def receive_download_items(self, value: int):
        self.max_items = value

    def download_done(self):
        self.download_progress += 1
        print(f"{self.download_progress} / {self.max_items}")

    def download_data(self):
        loop = asyncio.get_event_loop()
        if self.ui.source_combobox.currentIndex() == 0:
            self.downloader = BfvSrRegeltest(self.ui.username_lineedit.text(), self.ui.password_lineedit.text())
            self.downloader.available_questions.connect(self.receive_download_items)
            self.downloader.downloaded_element.connect(self.download_done)

            regelgruppen_list, regelfragen_list = loop.run_until_complete(self.downloader.download_loop())
            self.data = {"question_groups": regelgruppen_list, "questions": regelfragen_list}
            self.accept()


class BfvSrRegeltest(QObject):
    base_url = "https://bfv.sr-regeltest.de"
    available_questions = Signal(int)
    downloaded_element = Signal()
    login_successful = Signal(bool)

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    async def login(self, session):
        async with session.get("/users/sign_in") as resp:
            r = await resp.text()

        login_page = BeautifulSoup(r, 'html.parser')
        authenticity_token = login_page.find('input', {'name': 'authenticity_token'})['value']

        url = '/users/sign_in'
        myobj = {'authenticity_token': authenticity_token,
                 'user[email]': self.username,
                 'user[password]': self.password,
                 'user[remember_me]': "0",
                 'commit': "Anmelden"}

        async with session.post(url, data=myobj) as resp:
            r = await resp.text()
        if 'Passwort ungültig' in r:
            raise LoginFailedException()

    async def _fetch_question(self, session, soup_element):
        rows = soup_element.findAll("td")

        question_url = rows[0].find('a').attrs['href']
        regel_id = rows[0].find('a').contents[0]
        group_name = rows[1].contents[0]

        try:
            int(regel_id)
            regel_id = regel_id.zfill(5)
            group_id = int(regel_id[0:2])
            question_id = int(regel_id[2:])
        except ValueError:
            group_id = 25
            question_id = -1

        async with session.get(question_url) as resp:
            detail_page = await resp.text()
        detail_page = BeautifulSoup(detail_page, 'html.parser')
        content = detail_page.findAll("div", {"class": "card-body"})
        question = content[0].findAll("p")[1].contents[0].strip()
        if len(content[1].findAll("tr", {"class": "wrong-answer"})) > 0:
            # multiple choice!
            multiple_choice = []
            for i, answers in enumerate(content[1].findAll("tr")):
                multiple_choice_answer = answers.find("td").contents[0].strip()
                if answers["class"][0] == 'correct-answer':
                    answer_index = i
                    answer_text = multiple_choice_answer
                multiple_choice += [answers.find("td").contents[0].strip()]
        else:
            answer_elements = content[1].find("p")
            if answer_elements:
                answer_text = answer_elements.contents[0].strip()
            else:
                answer_text = ""
                print(f"Regelgruppe {group_id} - Regel-ID {question_id} hat eine leere Antwort!")
            multiple_choice = []
            answer_index = -1

        self.downloaded_element.emit()

        return QuestionJSON(
            group_id,
            question_id,
            question,
            answer_index,
            answer_text,
            str(datetime.strptime(rows[3].contents[0], '%d.%m.%Y').date()),
            str(datetime.strptime(rows[4].contents[0], '%d.%m.%Y').date()),
            multiple_choice,
        ), QuestionGroupJSON(group_id, group_name)

    @staticmethod
    async def _fetch_list(session, page_number: int):
        async with session.get(f'/questions?page={page_number}') as resp:
            content = await resp.text()
        soup = BeautifulSoup(content, 'html.parser')
        return soup.find("table").find("tbody").findAll("tr")

    async def download_loop(self):
        async with aiohttp.ClientSession("https://bfv.sr-regeltest.de") as session:
            # login
            try:
                await self.login(session)
            except LoginFailedException:
                self.login_successful.emit(False)
                return
            self.login_successful.emit(True)

            async with session.get('/questions?page=1') as resp:
                question_page_1 = await resp.text()
            soup = BeautifulSoup(question_page_1, 'html.parser')
            last_page = int(soup.find(text="Letzte »").parent["href"].split("=")[1])

            tasks = [asyncio.ensure_future(self._fetch_list(session, page_number)) for page_number in
                     range(1, last_page + 1)]
            regelfragen_tables = [item for sublist in await asyncio.gather(*tasks) for item in sublist]
            print(f"{len(regelfragen_tables)} Regelfragen gefunden!")
            self.available_questions.emit(len(regelfragen_tables))

            tasks = [asyncio.ensure_future(self._fetch_question(session, soup_set)) for soup_set in
                     regelfragen_tables]
            responses = await asyncio.gather(*tasks)

            regelfragen, regelgruppen = list(zip(*responses))

            regelgruppen_sorted = sorted(regelgruppen, key=lambda x: x.id)
            re_id = defaultdict(lambda: 1)

            for question in regelfragen:
                if question.question_id == -1:
                    question.question_id = re_id[question.group_id]
                    re_id[question.group_id] += 1

            regelgruppen_list = [regelgruppe.toDict() for regelgruppe in regelgruppen_sorted]
            regelgruppen_filtered = []
            for group in regelgruppen_list:
                if group not in regelgruppen_filtered:
                    regelgruppen_filtered += [group]
            regelfragen_list = [regelfrage.toDict() for regelfrage in regelfragen]

            return regelgruppen_filtered, regelfragen_list


class DownloadProgress(QDialog, Ui_DownloadProgress):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_DownloadProgress()
        self.ui.setupUi(self)
        self.setWindowTitle("Lade herunter...")


class DownloadThread(QThread):
    download_progress = Signal(int)

    def __init__(self, request, filesize, fileobj, buffer):
        super(DownloadThread, self).__init__()
        self.request = request
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer

    def run(self):
        try:
            offset = 0
            for chunk in self.request.iter_content(chunk_size=self.buffer):
                if not chunk:
                    break
                self.fileobj.seek(offset)
                self.fileobj.write(chunk)
                offset = offset + len(chunk)
                download_progress = offset / int(self.filesize) * 100
                if download_progress != 100:
                    self.download_progress.emit(int(download_progress))

            self.fileobj.close()
            self.download_progress.emit(100)
            self.exit(0)

        except Exception as e:
            print(e)
