from typing import Union, Any

import PySide6
from PySide6.QtCore import Qt, QPoint, QAbstractTableModel, QSortFilterProxyModel
from PySide6.QtGui import QAction, QDrag
from PySide6.QtWidgets import QTreeWidget, QVBoxLayout, QDialog, QMessageBox, QMenu, QListView, \
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


class RuleSortFilterProxyModel(QSortFilterProxyModel):
    pass


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

    def insertRow(self, row: int,
                  parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> bool:
        return
        self.beginInsertRows(parent)
        self.endInsertRows()

    def flags(self, index: Union[
        PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex]) -> PySide6.QtCore.Qt.ItemFlags:
        return Qt.ItemIsDragEnabled | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def supportedDragActions(self) -> PySide6.QtCore.Qt.DropActions:
        return Qt.CopyAction

    def add_new_question(self):
        new_question = Question()
        new_question.rulegroup = controller.get_rulegroup(self.rulegroup_id)
        new_question.rule_id = controller.get_new_question_id(self.rulegroup_id)
        editor = QuestionEditor(new_question)
        if editor.exec() == QDialog.Accepted:
            signature = controller.update_question_set(editor.question, editor.mchoice)
            self.add_question(controller.get_question(signature))

    def dropMimeData(self, data: PySide6.QtCore.QMimeData, action: PySide6.QtCore.Qt.DropAction, row: int, column: int,
                     parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex]) -> bool:
        pass


class RulegroupView(QTableView):
    def __init__(self, parent):
        super(RulegroupView, self).__init__(parent)
        self.setSelectionMode(QTreeWidget.ExtendedSelection)
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
        self.setDragDropMode(QTableView.DragOnly)
        self.setDefaultDropAction(Qt.CopyAction)

        vertical_layout = QVBoxLayout(parent)
        vertical_layout.addWidget(self)

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
                for row in selected_items:
                    self.model().removeRow(row)

        actions = []

        selection_model = self.selectionModel()
        if selection_model.hasSelection():
            items = selection_model.selectedRows()
            if len(items) == 1:
                text = "Diese Frage löschen"
            else:
                text = "Aktuelle Auswahl löschen"
            deleteAct = QAction(self)
            deleteAct.setText(text)
            deleteAct.triggered.connect(lambda: delete_selection(items))
            actions += [deleteAct]

        create_action = QAction(self)
        create_action.setText("Neue Frage erstellen")
        create_action.triggered.connect(lambda: self.model().insertRow(-1))
        actions += [create_action]

        menu = QMenu(self)
        menu.addActions(actions)
        menu.exec(self.mapToGlobal(pos))

    def startDrag(self, supportedActions: Qt.DropActions) -> None:
        super(RulegroupView, self).startDrag(supportedActions)
        rows = self.selectionModel().selectedRows()
        if not rows:
            return
        mimeData = self.model().mimeData(rows)
        if not mimeData:
            return
        data = []
        for row in rows:
            data += [self.model().data(row, role=Qt.UserRole)]
        signatures = [question.signature for question in data]
        signatures = "".join(signatures).encode()
        mimeData.setData('application/questionitems', bytearray(signatures))
        drag = QDrag(self)
        drag.setMimeData(mimeData)

        result = drag.exec_(supportedActions, Qt.CopyAction)
        if result == Qt.CopyAction:
            self.clearSelection()
