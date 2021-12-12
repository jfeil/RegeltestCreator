from typing import List, Dict

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QFileDialog, \
    QApplication, QListWidget
from bs4 import BeautifulSoup

from . import controller
from .basic_config import display_name, app_version, app_author
from .question_editor import QuestionEditor
from .regeltestcreator import QuestionTree
from .ui_mainwindow import Ui_MainWindow
from .datatypes import Rulegroup, Question, create_rulegroups, create_questions_and_mchoice


def load_dataset(parent: QWidget, reset_cursor=True) -> bool:
    def read_in(file_path: str):
        with open(file_path, 'r+') as file:
            soup = BeautifulSoup(file, "lxml")
        rulegroups = create_rulegroups(soup.find("gruppen"))
        questions, mchoice = create_questions_and_mchoice(soup("regelsatz"))
        return rulegroups, questions, mchoice

    file_name = QFileDialog.getOpenFileName(parent, caption="Open Questionfile", filter="DFB Regeldaten (*.xml)")
    if len(file_name) == 0 or file_name[0] == "":
        return False
    QApplication.setOverrideCursor(Qt.WaitCursor)
    datasets = read_in(file_name[0])
    controller.clear_database()
    for dataset in datasets:
        controller.fill_database(dataset)
    if reset_cursor:
        QApplication.restoreOverrideCursor()
    return True


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(QCoreApplication.translate("MainWindow", f"Regeltest Creator - {app_version} ({app_author})"
                                                       , None))
        self.ui.actionRegeldatensatz_einladen.triggered.connect(self.load_dataset)
        self.ui.tabWidget.clear()
        self.ui.regeltest_list.setAcceptDrops(True)
        self.ui.actionAnsicht_zur_cksetzen.triggered.connect(lambda: self.ui.regeltest_creator.show())
        self.ruletabs = {}  # type: Dict[int, QuestionTree]
        self.questions = {}  # type: Dict[QTreeWidgetItem, str]

    def load_dataset(self):
        load_dataset(self, reset_cursor=False)
        for question_tree in self.ruletabs.values():
            question_tree.refresh_questions()
        QApplication.restoreOverrideCursor()

    def initialize_questions(self):
        for rulegroup_index, tree_widget in self.ruletabs.items():
            questions = controller.get_questions_by_foreignkey(rulegroup_index)
            for question in questions:
                tree_widget.add_question(question)

    def create_ruletabs(self, rulegroups: List[Rulegroup]):
        for rulegroup in rulegroups:
            tab = QWidget()
            self.ruletabs[rulegroup.id] = QuestionTree(tab)
            self.ui.tabWidget.addTab(tab, "")
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(tab), f"{rulegroup.id} {rulegroup.name}")
