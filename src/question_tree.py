from typing import Dict, Union, Any

import PySide6
from PySide6.QtCore import Qt, QPoint, QAbstractTableModel
from PySide6.QtGui import QAction, QDrag
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QVBoxLayout, QDialog, QMessageBox, QMenu, QListView, \
    QTableView, QStyledItemDelegate, QWidget

from src import controller
from src.datatypes import Question
from src.question_editor import QuestionEditor


class RuleDelegate(QStyledItemDelegate):
    def createEditor(self, parent: PySide6.QtWidgets.QWidget, option: PySide6.QtWidgets.QStyleOptionViewItem,
                     index: Union[
                         PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex]) -> PySide6.QtWidgets.QWidget:
        editor = QWidget(parent)
        question = index.model().data(index, role=Qt.UserRole)
        dialog = QuestionEditor(question, parent=editor)
        if dialog.exec() == QDialog.Accepted:
            # was updated
            index.model().setData(index, (dialog.question, dialog.mchoice), Qt.UserRole)
        return editor


class RuleDataModel(QAbstractTableModel):
    # When subclassing QAbstractTableModel, you must implement rowCount(), columnCount(), and data(). Default
    # implementations of the index() and parent() functions are provided by QAbstractTableModel. Well behaved models
    # will also implement headerData().

    # Models that provide interfaces to resizable data structures can provide implementations of insertRows(),
    # removeRows(), insertColumns(), and removeColumns(). When implementing these functions, it is important to call
    # the appropriate functions so that all connected views are aware of any changes:
    #
    # An insertRows() implementation must call beginInsertRows() before inserting new rows into the data structure,
    # and it must call endInsertRows() immediately afterwards. An insertColumns() implementation must call
    # beginInsertColumns() before inserting new columns into the data structure, and it must call endInsertColumns()
    # immediately afterwards. A removeRows() implementation must call beginRemoveRows() before the rows are removed
    # from the data structure, and it must call endRemoveRows() immediately afterwards. A removeColumns()
    # implementation must call beginRemoveColumns() before the columns are removed from the data structure,
    # and it must call endRemoveColumns() immediately afterwards.
    def __init__(self, rulegroup_id, parent):
        super(RuleDataModel, self).__init__(parent)
        self.rulegroup_id = rulegroup_id
        self.questions = controller.get_questions_by_foreignkey(rulegroup_id)
        self.header = [
            "Regelnummer",
            "Frage",
            "Multiple choice",
            "Antwort",
            "Änderungsdatum"]
        self.keys = [
            'rule_id',
            'question',
            'answer_index',
            'answer_text',
            'last_edited']

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self.questions)

    def columnCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return 5

    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex],
             role: int = ...) -> Any:
        col = index.column()
        row = index.row()
        if role == Qt.UserRole:
            return self.questions[row]
        elif col == 2 and role == Qt.CheckStateRole:
            return 2 * (self.questions[row].__dict__[self.keys[col]] != -1)
        elif col != 2 and role == Qt.DisplayRole:
            return f"{self.questions[row].__dict__[self.keys[col]]}"
        elif (col == 1 or col == 3) and role == Qt.ToolTipRole:
            return f"{self.questions[row].__dict__[self.keys[col]]}"
        else:
            return None

    def setData(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], value: Any,
                role: int = ...) -> bool:
        if role == Qt.UserRole:
            #             signature = controller.update_question_set(dialog.question, dialog.mchoice)
            #             self._set_question(item, controller.get_question(signature))
            print(value)
            return False
        return False

    def headerData(self, section: int, orientation: PySide6.QtCore.Qt.Orientation, role: int = ...) -> Any:
        if orientation == Qt.Vertical:
            return None
        if role == Qt.DisplayRole:
            return self.header[section]
        else:
            return None

    def insertRows(self, row: int, count: int,
                   parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> bool:
        return
        self.beginInsertRows(parent)
        self.endInsertRows()

    def flags(self, index: Union[
        PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex]) -> PySide6.QtCore.Qt.ItemFlags:
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def add_new_question(self):
        new_question = Question()
        new_question.rulegroup = controller.get_rulegroup(self.rulegroup_id)
        new_question.rule_id = controller.get_new_question_id(self.rulegroup_id)
        editor = QuestionEditor(new_question)
        if editor.exec() == QDialog.Accepted:
            signature = controller.update_question_set(editor.question, editor.mchoice)
            self.add_question(controller.get_question(signature))


class RulegroupView(QTableView):
    def __init__(self, parent, rulegroup_id):
        super(RulegroupView, self).__init__(parent)
        self.rulegroup_id = rulegroup_id
        self.questions = {}  # type: Dict[QTreeWidgetItem, str]
        self.setSelectionMode(QTreeWidget.ExtendedSelection)
        # self.doubleClicked.connect(self._handle_double_click)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.prepare_menu)
        self.setObjectName("tree_widget")

        self.setItemDelegate(RuleDelegate(self))
        self.setEditTriggers(QTableView.DoubleClicked | QTableView.SelectedClicked)

        self.setShowGrid(True)
        self.setGridStyle(Qt.NoPen)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QListView.SelectRows)

        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)

        self.setDragEnabled(True)
        self.setDefaultDropAction(Qt.CopyAction)

        vertical_layout = QVBoxLayout(parent)
        vertical_layout.addWidget(self)

    def _handle_double_click(self, index):
        print(index)
        return
        editor = QuestionEditor(controller.get_question(self.questions[item]))
        if editor.exec() == QDialog.Accepted:
            # was updated
            signature = controller.update_question_set(editor.question, editor.mchoice)
            self._set_question(item, controller.get_question(signature))

    def refresh_questions(self):
        for item, question_signature in self.questions.items():
            self._set_question(item, controller.get_question(question_signature))

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
            return "✘"

        self.questions[item] = question.signature
        item.setText(0, str(question.rule_id))
        item.setText(1, question.question)
        item.setText(2, bool_to_char(question.answer_index != -1))
        item.setText(3, question.answer_text)
        item.setText(4, str(question.last_edited))
        item.setToolTip(1, question.question)
        item.setToolTip(3, question.answer_text)

    def startDrag(self, supportedActions: Qt.DropActions) -> None:
        super(RulegroupView, self).startDrag(supportedActions)
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
