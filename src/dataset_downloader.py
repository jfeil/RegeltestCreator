import asyncio
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import List

import aiohttp
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QDialog, QMessageBox
from bs4 import BeautifulSoup

from src.ui_dataset_download_dialog import Ui_DownloadDialog
from src.ui_download_progress import Ui_DownloadProgress


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
        self.download_thread = None

        self.data = None

    def download_data(self):
        if self.ui.source_combobox.currentIndex() == 0:
            downloader = BfvSrRegeltest(self.ui.username_lineedit.text(), self.ui.password_lineedit.text())

        def login_successful(value: bool):
            if value:
                result = progress_dialog.exec()
                if result == QDialog.Rejected:
                    self.reject()
                else:
                    self.data = self.download_thread.data
                    self.accept()
            else:
                self.ui.password_lineedit.setText("")
                msgBox = QMessageBox(self)
                msgBox.setWindowTitle("Fehler")
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText("Der Login ist ungültig.")
                msgBox.exec()
                return

        progress_dialog = DownloadProgress(self)
        downloader.display_text.connect(progress_dialog.ui.progress_label.setText)
        downloader.successful_login.connect(login_successful)

        self.download_thread = DownloadThread(downloader)
        self.download_thread.download_progress.connect(progress_dialog.ui.progressBar.setValue)
        self.download_thread.completed.connect(progress_dialog.accept)
        self.download_thread.start()


class DownloadThread(QThread):
    download_progress = Signal(int)
    completed = Signal()

    downloaded_items = 0
    max_items = -1
    downloader = None

    def __init__(self, downloader):
        super(DownloadThread, self).__init__()
        self.downloader = downloader
        self.data = {"question_groups": [], "questions": []}

    def run(self):
        def receive_download_items(value: int):
            self.max_items = value

        def download_done():
            self.downloaded_items += 1
            self.download_progress.emit(self.downloaded_items / self.max_items * 100)

        self.downloader.available_questions.connect(receive_download_items)
        self.downloader.downloaded_element.connect(download_done)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        regelgruppen_list, regelfragen_list = loop.run_until_complete(self.downloader.download_loop())
        self.data = {"question_groups": regelgruppen_list, "questions": regelfragen_list}
        loop.run_until_complete(asyncio.sleep(0.250))
        loop.close()
        self.completed.emit()


class BfvSrRegeltest(QObject):
    base_url = "https://bfv.sr-regeltest.de"
    available_questions = Signal(int)
    downloaded_element = Signal()
    display_text = Signal(str)
    successful_login = Signal(bool)

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    async def login(self, session) -> bool:
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
            return False
        return True

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

        while True:
            async with session.get(question_url) as resp:
                detail_page = await resp.text()
            detail_page = BeautifulSoup(detail_page, 'html.parser')
            content = detail_page.findAll("div", {"class": "card-body"})
            if len(content) != 0:
                break
            print("Too many request errors, trying again..")
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
        connector = aiohttp.TCPConnector(limit_per_host=100)
        async with aiohttp.ClientSession("https://bfv.sr-regeltest.de", connector=connector) as session:
            self.successful_login.emit(await self.login(session))
            self.display_text.emit("Sammle alle verfügbaren Fragen...")
            async with session.get('/questions?page=1') as resp:
                question_page_1 = await resp.text()
            soup = BeautifulSoup(question_page_1, 'html.parser')
            last_page = int(soup.find(text="Letzte »").parent["href"].split("=")[1])

            tasks = [asyncio.ensure_future(self._fetch_list(session, page_number)) for page_number in
                     range(1, last_page + 1)]
            regelfragen_tables = [item for sublist in await asyncio.gather(*tasks) for item in sublist]
            self.display_text.emit(f"{len(regelfragen_tables)} Regelfragen gefunden! Downloade...")
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
        self.ui.progressBar.setValue(0)
        self.orig_loop = asyncio.get_event_loop()

    def accept(self) -> None:
        asyncio.set_event_loop(self.orig_loop)
        super().accept()
