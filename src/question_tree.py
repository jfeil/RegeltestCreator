from typing import Dict

from PySide6.QtCore import Qt, QCoreApplication, QPoint
from PySide6.QtGui import QAction, QDrag
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QVBoxLayout, QDialog, QMessageBox, QMenu

from src import controller
from src.datatypes import Question
from src.question_editor import QuestionEditor


class SortableQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent):
        super(SortableQTreeWidgetItem, self).__init__(parent)

    def __lt__(self, other_item):
        column = self.treeWidget().sortColumn()
        try:
            return float(self.text(column)) > float(other_item.text(column))
        except ValueError:
            return self.text(column).lower() < other_item.text(column).lower()


class QuestionTree(QTreeWidget):
    def __init__(self, parent, rulegroup_id):
        super(QuestionTree, self).__init__(parent)
        self.rulegroup_id = rulegroup_id
        self.questions = {}  # type: Dict[QTreeWidgetItem, str]
        self.setDragEnabled(True)
        self.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.setDefaultDropAction(Qt.CopyAction)
        self.itemDoubleClicked.connect(self._handle_double_click)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.prepare_menu)
        self.setObjectName("tree_widget")
        self.setSortingEnabled(True)
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
        if editor.exec() == QDialog.Accepted:
            # was updated
            signature = controller.update_question_set(editor.question, editor.mchoice)
            self._set_question(item, controller.get_question(signature))

    def add_new_question(self):
        new_question = Question()
        new_question.rulegroup = controller.get_rulegroup(self.rulegroup_id)
        new_question.rule_id = controller.get_new_question_id(self.rulegroup_id)
        editor = QuestionEditor(new_question)
        if editor.exec() == QDialog.Accepted:
            signature = controller.update_question_set(editor.question, editor.mchoice)
            self.add_question(controller.get_question(signature))

    def refresh_questions(self):
        for item, question_signature in self.questions.items():
            self._set_question(item, controller.get_question(question_signature))

    def add_question(self, question: Question):
        item = SortableQTreeWidgetItem(self)
        self._set_question(item, question)

    def prepare_menu(self, pos: QPoint):
        def delete_selection(selected_items):
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Fragen löschen.")
            msgBox.setText("Fragen löschen.")
            if len(selected_items) == 1:
                text = f"Möchtest du wirklich diese Frage löschen? Dies lässt sich nicht umkehren!"
            else:
                text = f"Möchtest du wirklich diese {len(selected_items)} Fragen löschen? Dies lässt sich nicht umkehren!"
            msgBox.setInformativeText(text)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            ret = msgBox.exec()
            if ret == QMessageBox.Yes:
                for item in selected_items:
                    controller.delete(controller.get_question(self.questions[item]))
                    self.questions.pop(item)
                    self.takeTopLevelItem(self.indexOfTopLevelItem(item))

        delete_bool = True
        items = self.selectedItems()
        actions = []
        if not items:
            items = [self.itemAt(pos)]
            text = "Diese Frage löschen"
            if items[0] is None:
                delete_bool = False
        else:
            clearSelAct = QAction(self)
            clearSelAct.setText("Auswahl zurücksetzen")
            clearSelAct.triggered.connect(lambda: self.clearSelection())
            actions += [clearSelAct]
            text = "Aktuelle Auswahl löschen"

        if delete_bool:
            deleteAct = QAction(self)
            deleteAct.setText(text)
            deleteAct.triggered.connect(lambda: delete_selection(items))
            actions += [deleteAct]

        create_action = QAction(self)
        create_action.setText("Neue Frage erstellen")
        create_action.triggered.connect(self.add_new_question)
        actions += [create_action]

        menu = QMenu(self)
        menu.addActions(actions)
        menu.exec(self.mapToGlobal(pos))

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

    def startDrag(self, supportedActions: Qt.DropActions) -> None:
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
