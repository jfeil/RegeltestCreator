import datetime
import json
from enum import Enum, auto, IntEnum
from typing import Dict, Any

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog, QApplication, QMessageBox, QDialog
from bs4 import BeautifulSoup

from src.basic_config import app_version, check_for_update, display_name, is_bundled
from src.database import db
from src.dataset_downloader import DatasetDownloadDialog
from src.datatypes import create_question_groups, create_questions_and_mchoice, QuestionGroup, Question, MultipleChoice
from src.dock_widgets import RegeltestCreatorDockwidget, SelfTestDockWidget
from src.main_widgets import FirstSetupWidget, QuestionOverviewWidget, SelfTestWidget
from src.ui_mainwindow import Ui_MainWindow
from src.updater import UpdateChecker


class FilterMode(Enum):
    Include = auto()
    Exclude = auto()


class ApplicationMode(IntEnum):
    initial_setup = 0
    question_overview = 1
    self_test = 2
    regeltest_setup = 3


def read_in_sr_regeltest_de(json_content: Dict[str, Any]):
    question_groups = []
    questions = []
    for question_group in json_content["question_groups"]:
        question_groups += [QuestionGroup(
            id=question_group["id"],
            name=question_group["name"]
        )]
    for question in json_content["questions"]:
        multiple_choice = []
        answer_text = question["answer_text"]
        answer_index = question["answer_index"]
        if question["multiple_choice"]:
            for i, answer_option in enumerate(question["multiple_choice"]):
                multiple_choice += [MultipleChoice(index=i, text=answer_option)]
            answer_text = multiple_choice[answer_index].text
        questions += [Question(
            group_id=question["group_id"],
            question_id=question["question_id"],
            question=question["question"],
            answer_index=answer_index,
            answer_text=answer_text,
            created=datetime.datetime.strptime(question["created"], '%Y-%m-%d').date(),
            last_edited=datetime.datetime.strptime(question["last_edited"], '%Y-%m-%d').date(),
            multiple_choice=multiple_choice
        )]
    return question_groups, questions


def read_in_origformat(soup_content: BeautifulSoup):
    question_groups = create_question_groups(soup_content.find("GRUPPEN"))
    questions, mchoice = create_questions_and_mchoice(soup_content("REGELSATZ"))
    return question_groups, questions, mchoice


def load_file_dataset(parent: QWidget, reset_cursor=True) -> bool:
    datasets = []
    filter_sr_regeltest_de = "sr-regeltest.de Export (*.json)"
    filter_orig = "DFB Regeldaten (*.xml)"
    file_name = QFileDialog.getOpenFileName(parent, caption="Fragendatei öffnen",
                                            filter=f"{filter_sr_regeltest_de};;{filter_orig}")
    if len(file_name) == 0 or file_name[0] == "":
        return False
    QApplication.setOverrideCursor(Qt.WaitCursor)
    if file_name[1] == filter_orig:
        with open(file_name[0], 'rb') as file:
            soup_content = BeautifulSoup(file, "lxml-xml")
        datasets = read_in_origformat(soup_content)
    elif file_name[1] == filter_sr_regeltest_de:
        with open(file_name[0], 'r', encoding='utf-8') as file:
            json_content = json.load(file)
        datasets = read_in_sr_regeltest_de(json_content)
    db.clear_database()
    for dataset in datasets:
        db.fill_database(dataset)
    if reset_cursor:
        QApplication.restoreOverrideCursor()
    return True


def load_online_dataset(parent: QWidget, reset_cursor=True) -> bool:
    dataset_downloader = DatasetDownloadDialog(parent)
    if dataset_downloader.exec() == QDialog.Accepted:
        datasets = read_in_sr_regeltest_de(dataset_downloader.data)
        db.clear_database()
        for dataset in datasets:
            db.fill_database(dataset)
        if reset_cursor:
            QApplication.restoreOverrideCursor()
        return True
    else:
        return False


def save_dataset(parent: QWidget):
    file_name = QFileDialog.getSaveFileName(parent, caption="Fragendatei speichern", filter="DFB Regeldaten (*.json)")
    if len(file_name) == 0 or file_name[0] == "":
        return
    QApplication.setOverrideCursor(Qt.WaitCursor)
    question_groups = []
    questions = []
    for question_group in db.get_all_question_groups():
        question_groups += [question_group.export()]
    for question in db.get_all_questions():
        questions += [question.export()]
    with open(file_name[0], "w+") as file:
        json.dump({
            "question_groups": question_groups,
            "questions": questions
        }, file)
    QApplication.restoreOverrideCursor()


def display_update_dialog(parent, releases):
    # new_version, description, url, download_url
    dialog = UpdateChecker(parent, releases, app_version.is_devrelease)
    dialog.exec()


def about_dialog():
    msg_box = QMessageBox()
    msg_box.setWindowTitle(f"Über {display_name}")
    msg_box.setText(f"<center><b>Regeltest-Creator</b></center>"
                    f"<center>v{app_version}</center><br>"
                    "<center>entwickelt von Jan Feil</center><br>"
                    "<a href=https://github.com/jfeil/RegeltestCreator>Weitere Informationen und Programmcode</a>")
    msg_box.exec()


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 1. Setup, 2. QuestionGroupList, 3. Self-Testing, 4. Regeltest-Setup
        # DockWidgets
        self.ui.stacked_widget_dock.addWidget(QWidget())

        self.question_overview_dock = RegeltestCreatorDockwidget(self)
        self.ui.stacked_widget_dock.addWidget(self.question_overview_dock)

        self.self_test_dock = SelfTestDockWidget(self)
        self.ui.stacked_widget_dock.addWidget(self.self_test_dock)

        # MainWidgets
        self.first_setup = FirstSetupWidget(self)
        self.first_setup.action_done.connect(self.initialize)
        self.ui.stackedWidget.addWidget(self.first_setup)

        self.question_overview = QuestionOverviewWidget(self)
        self.ui.stackedWidget.addWidget(self.question_overview)

        self.self_test = SelfTestWidget(self, self.self_test_dock)
        self.ui.stackedWidget.addWidget(self.self_test)

        # noinspection PyTypeChecker
        self.setWindowTitle(QCoreApplication.translate("MainWindow", f"{display_name} - {app_version}", None))
        self.ui.actionAus_einer_Datei.triggered.connect(lambda: self.load_dataset(from_file=True))
        self.ui.actionAus_dem_Internet.triggered.connect(lambda: self.load_dataset(from_file=False))
        self.ui.actionAuf_Updates_pr_fen.triggered.connect(lambda: display_update_dialog(self, check_for_update()))
        self.ui.action_ber.triggered.connect(about_dialog)

        # self.ui.menuBearbeiten.setEnabled()
        self.ui.actionRegeltest_einrichten.setEnabled(False)
        # self.ui.actionNeue_Kategorie_erstellen.setEnabled(False)
        self.ui.actionRegeltest_l_schen.setEnabled(False)

        self.ui.actionAnsicht_zur_cksetzen.triggered.connect(self.reset_ui)
        self.ui.actionRegeldatensatz_exportieren.triggered.connect(lambda: save_dataset(self))
        self.ui.actionNeue_Kategorie_erstellen.triggered.connect(self.add_question_group)

    def show(self) -> None:
        super(MainWindow, self).show()
        if not is_bundled:
            return
        releases = check_for_update()
        update_available = False
        if (app_version.is_devrelease and releases[1]) or (not app_version.is_devrelease and releases[0]):
            update_available = True
        if update_available:
            display_update_dialog(self, releases)

    def initialize(self):
        dataset = db.get_all_question_groups()
        if dataset:
            for question_group in dataset:
                self.question_overview.create_question_group_tab(question_group)
            self.set_mode(ApplicationMode.question_overview, reset=True)
        else:
            self.set_mode(ApplicationMode.initial_setup, reset=True)

    def load_dataset(self, from_file):
        if from_file:
            load_file_dataset(self, reset_cursor=False)
        else:
            load_online_dataset(self, reset_cursor=False)
        self.question_overview.reset()
        QApplication.restoreOverrideCursor()

    def add_question_group(self):
        self.question_overview.add_question_group()
        self.set_mode(ApplicationMode.question_overview)

    def reset_ui(self):
        self.set_mode(ApplicationMode(self.ui.stackedWidget.currentIndex()), reset=True)

    def set_mode(self, mode: ApplicationMode, reset=False):
        if self.ui.stackedWidget.currentIndex() == int(mode) and not reset:
            return

        self.ui.stackedWidget.setCurrentIndex(int(mode))
        self.ui.stacked_widget_dock.setCurrentIndex(int(mode))

        if mode == ApplicationMode.initial_setup:
            self.ui.actionSelftest.setVisible(False)
            self.ui.actionAnsicht_zur_cksetzen.setDisabled(True)
            self.ui.main_window_dockwidget.close()
        else:
            self.ui.actionAnsicht_zur_cksetzen.setDisabled(False)

        if mode == ApplicationMode.question_overview:
            self.ui.actionSelftest.setVisible(True)
            self.ui.actionSelftest.setText("Selbsttest")
            self.ui.actionSelftest.triggered.disconnect()
            self.ui.actionSelftest.triggered.connect(lambda: self.set_mode(ApplicationMode.self_test))
            self.ui.main_window_dockwidget.setWindowTitle("Regeltest-Creator")
            self.ui.main_window_dockwidget.show()

        if mode == ApplicationMode.self_test:
            self.self_test.reset()
            self.ui.actionSelftest.setVisible(True)
            self.ui.actionSelftest.setText("Fragenverwaltung")
            self.ui.actionSelftest.triggered.disconnect()
            self.ui.actionSelftest.triggered.connect(lambda: self.set_mode(ApplicationMode.question_overview))
            self.ui.main_window_dockwidget.setWindowTitle("Selbsttest-Einstellungen")
            self.ui.main_window_dockwidget.show()
