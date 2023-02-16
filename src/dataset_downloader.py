from dataclasses import dataclass
from datetime import datetime
from typing import List

import requests
from PySide6.QtCore import QThread, Signal
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


class DatasetDownloadDialog(QDialog, Ui_DownloadDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_DownloadDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Quelle auswählen")

        self.ui.source_combobox.addItem("bfv.sr-regeltest.de")
        self.ui.buttonBox.accepted.connect(self.login)
        self.session = None

        self.data = None

    def login(self):
        self.session = requests.Session()
        if self.ui.source_combobox.currentIndex() == 0:
            def parse_regelfragen(soup_filtered, session):
                output_questions = []
                output_questiongroups = {}
                group_25_count = 0
                for element in soup_filtered:
                    rows = element.findAll("td")

                    question_url = rows[0].find('a').attrs['href']
                    regel_id = rows[0].find('a').contents[0]
                    group_name = rows[1].contents[0]

                    try:
                        int(regel_id)
                        regel_id = regel_id.zfill(5)
                        group_id = int(regel_id[0:2])
                        question_id = int(regel_id[2:])

                    except ValueError:
                        group_25_count += 1
                        group_id = 25
                        question_id = group_25_count

                    if group_id not in output_questiongroups:
                        output_questiongroups[group_id] = QuestionGroupJSON(group_id, group_name)

                    detail_page = BeautifulSoup(session.get(base_url + question_url).content, 'html.parser')
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

                    output_questions += [
                        QuestionJSON(
                            group_id,
                            question_id,
                            question,
                            answer_index,
                            answer_text,
                            str(datetime.strptime(rows[3].contents[0], '%d.%m.%Y').date()),
                            str(datetime.strptime(rows[4].contents[0], '%d.%m.%Y').date()),
                            multiple_choice,
                        )]
                return output_questiongroups, output_questions

            r = self.session.get("https://bfv.sr-regeltest.de/users/sign_in")
            base_url = "https://bfv.sr-regeltest.de"

            login_page = BeautifulSoup(r.content, 'html.parser')
            authenticity_token = login_page.find('input', {'name': 'authenticity_token'})['value']

            # login

            username = self.ui.username_lineedit.text()
            password = self.ui.password_lineedit.text()

            url = 'https://bfv.sr-regeltest.de/users/sign_in'
            myobj = {'authenticity_token': authenticity_token,
                     'user[email]': username,
                     'user[password]': password,
                     'user[remember_me]': "0",
                     'commit': "Anmelden"}

            login_answer = self.session.post(url, data=myobj)

            if 'Passwort ungültig' in login_answer.content.decode():
                self.session = None
                self.ui.password_lineedit.setText("")
                return
            question_page_1 = self.session.get(f'https://bfv.sr-regeltest.de/questions?page=1')
            soup = BeautifulSoup(question_page_1.content, 'html.parser')
            last_page = int(soup.find(text="Letzte »").parent["href"].split("=")[1])
            regelfragen_tables = []
            for i in range(1, last_page + 1):
                response = self.session.get(f'https://bfv.sr-regeltest.de/questions?page={i}')
                soup = BeautifulSoup(response.content, 'html.parser')
                regelfragen_tables += soup.find("table").find("tbody").findAll("tr")
            print(f"{len(regelfragen_tables)} Regelfragen gefunden!")

            regelgruppen, regelfragen = parse_regelfragen(regelfragen_tables, self.session)
            regelgruppen_sorted = list(regelgruppen.values())
            regelgruppen_sorted = sorted(regelgruppen_sorted, key=lambda x: x.id)

            regelgruppen_list = [regelgruppe.toDict() for regelgruppe in regelgruppen_sorted]
            regelfragen_list = [regelfrage.toDict() for regelfrage in regelfragen]

            self.data = {"question_groups": regelgruppen_list, "questions": regelfragen_list}
            self.accept()


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
