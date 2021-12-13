from typing import Dict

from PySide6.QtCore import Qt, QModelIndex, QMimeData, QCoreApplication, QRect
from PySide6.QtGui import QStandardItemModel, QDrag
from PySide6.QtWidgets import QListWidget, QTreeWidgetItem, QTreeWidget, QVBoxLayout, QDialog, QFileDialog
from PySide6.QtWidgets import QListWidgetItem

from src import controller
from src.datatypes import Question
from src.question_editor import QuestionEditor
from src.ui_regeltest_save import Ui_RegeltestSave


class RegeltestCreator(QListWidget):
    def __init__(self, *args):
        super(RegeltestCreator, self).__init__(*args)
        self.setAcceptDrops(True)
        self.questions = []  # type: List[str]

    def add_question(self, question: Question):
        if question.signature in self.questions:
            return
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole, question.signature)
        item.setText(question.question)
        self.questions.append(question.signature)

    def dropEvent(self, event):
        event.accept()
        if event.mimeData().hasFormat('application/questionitems'):
            data = event.mimeData().data('application/questionitems')
            signatures = data.data().decode()
            n = 32
            signatures = [signatures[i:i + n] for i in range(0, len(signatures), n)]
            for signature in signatures:
                self.add_question(controller.get_question(signature))


class QuestionTree(QTreeWidget):
    def __init__(self, parent):
        super(QuestionTree, self).__init__(parent)
        self.questions = {}  # type: Dict[QTreeWidgetItem, str]
        self.setDragEnabled(True)
        self.setSelectionMode(QTreeWidget.MultiSelection)
        self.setDefaultDropAction(Qt.CopyAction)
        self.itemDoubleClicked.connect(self._handle_double_click)
        self.setObjectName("tree_widget")
        vertical_layout = QVBoxLayout(parent)
        ___qtreewidgetitem = self.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"\u00c4nderungsdatum", None))
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"Antwort", None))
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Multiple choice?", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Frage", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Regelnummer", None))
        vertical_layout.addWidget(self)

    def _handle_double_click(self, item):
        editor = QuestionEditor(controller.get_question(self.questions[item]))
        if editor.exec() == 1:
            # was updated
            self._set_question(item, controller.get_question(self.questions[item]))

    def refresh_questions(self):
        for item, question_signature in self.questions.items():
            self._set_question(item, controller.get_question(question_signature))

    def add_question(self, question: Question):
        item = QTreeWidgetItem(self)
        self._set_question(item, question)

    def _set_question(self, item: QTreeWidgetItem, question: Question):
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

    def startDrag(self, supportedActions:Qt.DropActions) -> None:
        super(QuestionTree, self).startDrag(supportedActions)
        indexes = self.selectionModel().selectedRows()
        signatures = [list(self.questions.values())[index.row()] for index in indexes]
        signatures = "".join(signatures).encode()
        if not indexes:
            return
        mimeData = self.model().mimeData(indexes)
        if not mimeData:
            return
        mimeData.setData('application/questionitems', bytearray(signatures))
        drag = QDrag(self)
        drag.setMimeData(mimeData)

        result = drag.exec_(supportedActions, Qt.CopyAction)
        if result == Qt.CopyAction:
            self.clearSelection()


class RegeltestSaveDialog(QDialog, Ui_RegeltestSave):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_RegeltestSave()
        self.ui.setupUi(self)
        self.ui.icon_edit_button.clicked.connect(self.open_icon)
        self.ui.output_edit_button.clicked.connect(self.create_save)

    def open_icon(self):
        file_name = QFileDialog.getOpenFileName(self, caption="Open icon", filter="Icon file (*.jpg;*.png)")
        if len(file_name) == 0 or file_name[0] == "":
            return
        self.ui.icon_path_edit.setText(file_name[0])

    def create_save(self):
        file_name = QFileDialog.getSaveFileName(self, caption="Save Regeltest", filter="Regeltest (*.pdf)")
        if len(file_name) == 0 or file_name[0] == "":
            return
        self.ui.output_edit.setText(file_name[0])
