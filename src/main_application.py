from typing import List, Dict

from PyQt6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout

from .ui_mainwindow import Ui_MainWindow
from .datatypes import Rulegroup, Question


def _create_ruletable(parent):
    tree_widget = QTreeWidget(parent)
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


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tabWidget.clear()

        self.ruletabs = {}  # type: Dict[int, QWidget]

    def insert_question(self, rulegroup: Rulegroup, questions: List[Question]):
        tree_widget = self.ruletabs[rulegroup.id].findChild(QTreeWidget)
        for question in questions:
            item = QTreeWidgetItem(tree_widget)
            item.setText(0, str(question.rule_id))
            item.setText(1, question.question)
            item.setText(2, str(question.answer_index != -1))
            item.setText(3, question.answer_text)
            item.setText(4, str(question.last_edited))
            item.setToolTip(1, question.question)
            item.setToolTip(3, question.answer_text)

    def create_ruletabs(self, rulegroups: List[Rulegroup]):
        for rulegroup in rulegroups:
            tab = QWidget()
            self.ruletabs[rulegroup.id] = tab
            self.ui.tabWidget.addTab(tab, "")
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(tab), f"{rulegroup.id} {rulegroup.name}")
            _create_ruletable(tab)
