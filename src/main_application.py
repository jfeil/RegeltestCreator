from typing import List, Dict

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QFileDialog, \
    QApplication
from bs4 import BeautifulSoup

from . import controller
from .basic_config import display_name, app_version, app_author
from .question_editor import QuestionEditor
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
        self.ruletabs = {}  # type: Dict[int, QWidget]
        self.questions = {}  # type: Dict[QTreeWidgetItem, str]

    def _handle_double_click(self, item):
        editor = QuestionEditor(controller.get_question(self.questions[item]))
        if editor.exec() == 1:
            # was updated
            self.set_question(item, controller.get_question(self.questions[item]))

    def _create_ruletable(self, parent):
        tree_widget = QTreeWidget(parent)
        tree_widget.itemDoubleClicked.connect(self._handle_double_click)
        tree_widget.setObjectName("tree_widget")
        vertical_layout = QVBoxLayout(parent)
        ___qtreewidgetitem = tree_widget.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"\u00c4nderungsdatum", None))
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"Antwort", None))
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Multiple choice?", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Frage", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Regelnummer", None))
        vertical_layout.addWidget(tree_widget)
        return vertical_layout

    def load_dataset(self):
        load_dataset(self, reset_cursor=False)
        self.refresh_questions()
        QApplication.restoreOverrideCursor()

    def refresh_questions(self):
        for item, question_signature in self.questions.items():
            self.set_question(item, controller.get_question(question_signature))

    def set_question(self, item: QTreeWidgetItem, question: Question):
        def bool_to_char(value: bool):
            if value:
                return "✔"
            return "🗙"

        self.questions[item] = question.signature
        item.setText(0, str(question.rule_id))
        item.setText(1, question.question)
        item.setText(2, bool_to_char(question.answer_index != -1))
        item.setText(3, question.answer_text)
        item.setText(4, str(question.last_edited))
        item.setToolTip(1, question.question)
        item.setToolTip(3, question.answer_text)

    def initialize_questions(self):
        for rulegroup_index, tree_widget_parent in self.ruletabs.items():
            questions = controller.get_questions_by_foreignkey(rulegroup_index)
            tree_widget = tree_widget_parent.findChild(QTreeWidget)
            for question in questions:
                item = QTreeWidgetItem(tree_widget)
                self.set_question(item, question)

    def create_ruletabs(self, rulegroups: List[Rulegroup]):
        for rulegroup in rulegroups:
            tab = QWidget()
            self.ruletabs[rulegroup.id] = tab
            self.ui.tabWidget.addTab(tab, "")
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(tab), f"{rulegroup.id} {rulegroup.name}")
            self._create_ruletable(tab)
