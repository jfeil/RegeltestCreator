import webbrowser
from typing import List, Dict

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QTreeWidgetItem, QFileDialog, \
    QApplication
from bs4 import BeautifulSoup

from . import controller, document_builder
from .basic_config import app_version, app_author
from .datatypes import Rulegroup, create_rulegroups, create_questions_and_mchoice
from .regeltestcreator import QuestionTree, RegeltestSaveDialog, RegeltestSetup
from .ui_mainwindow import Ui_MainWindow


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


def save_dataset(parent: QWidget):
    file_name = QFileDialog.getSaveFileName(parent, caption="Save Questionfile", filter="DFB Regeldaten (*.xml)")
    if len(file_name) == 0 or file_name[0] == "":
        return
    QApplication.setOverrideCursor(Qt.WaitCursor)
    dataset = "<?xml version=\"1.0\" encoding=\"iso-8859-1\" ?>\n\
<REGELTEST>\n"
    for rulegroup in controller.get_all_rulegroups():
        dataset += rulegroup.export()
    for question in controller.get_all_questions():
        question_set = question[0].export()
        dataset += question_set[0]
        if question[1]:
            for mchoice in question[1]:
                dataset += mchoice.export()
        dataset += question_set[1]
    dataset += "</REGELTEST>"
    with open(file_name[0], "w+") as file:
        file.writelines(dataset)
    QApplication.restoreOverrideCursor()


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
        self.ui.actionRegeldatensatz_exportieren.triggered.connect(lambda: save_dataset(self))

        self.ui.regeltest_list.model().rowsInserted.connect(self.rows_changed)
        self.ui.regeltest_list.model().rowsRemoved.connect(self.rows_changed)

        self.ui.add_questionlist.clicked.connect(self.setup_regeltest)
        self.ui.clear_questionlist.clicked.connect(self.clear_questionlist)

        self.ui.create_regeltest.clicked.connect(self.create_regeltest)

        self.ruletabs = {}  # type: Dict[int, QuestionTree]
        self.questions = {}  # type: Dict[QTreeWidgetItem, str]

    def clear_questionlist(self):
        self.ui.regeltest_list.clear()
        self.ui.regeltest_list.questions.clear()
        self.rows_changed()

    def rows_changed(self):
        self.ui.regeltest_stats.setText(
            f"{self.ui.regeltest_list.count()} Fragen selektiert ({self.ui.regeltest_list.count() * 2} Punkte)")

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
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(tab), f"{rulegroup.id:02d} {rulegroup.name}")

    def setup_regeltest(self):
        regeltest_setup = RegeltestSetup(self)
        if regeltest_setup.exec():
            for question in regeltest_setup.collect_questions():
                self.ui.regeltest_list.add_question(question)

    def create_regeltest(self):
        question_set = []
        for signature in self.ui.regeltest_list.questions:
            question_set += [
                (controller.get_question(signature), controller.get_multiplechoice_by_foreignkey(signature))]
        settings = RegeltestSaveDialog(self)
        settings.ui.title_edit.setFocus()
        result = settings.exec()
        output_path = settings.ui.output_edit.text()
        if result:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            document_builder.create_document(question_set, output_path, settings.ui.title_edit.text()
                                             , icon_path=settings.ui.icon_path_edit.text())
            QApplication.restoreOverrideCursor()
            webbrowser.open_new(output_path)
