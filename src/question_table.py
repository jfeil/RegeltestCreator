from __future__ import annotations

import datetime
from typing import Any, List

import PySide6
from PySide6.QtCore import Qt, QPoint, QAbstractTableModel, QSortFilterProxyModel
from PySide6.QtGui import QAction, QDrag, QShortcut, QKeySequence
from PySide6.QtWidgets import QTreeWidget, QVBoxLayout, QDialog, QMessageBox, QMenu, QListView, QTableView, \
    QStyledItemDelegate, QWidget

from src.database import db
from src.datatypes import Question
from src.question_editor import QuestionEditor

dict_key = str


class QuestionGroupDataModel(QAbstractTableModel):
    # When subclassing QAbstractTableModel, you must implement rowCount(), columnCount(), and data(). Default
    # implementations of the index() and main_window() functions are provided by QAbstractTableModel. Well-behaved
    # models will also implement headerData().

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

    headers = [('question_id', True),
               ('question', True),
               ('multiple_choice', True),
               ('answer_text', True),
               ('last_edited', True),
               ('regeltest_count', True),
               ('last_tested', False),
               ('positive_tests', False),
               ('negative_tests', False),
               ('streak', False)]
    activated_headers = [question for (question, question_bool) in headers if question_bool]

    def __init__(self, question_group, parent):
        super(QuestionGroupDataModel, self).__init__(parent)
        self.question_group = question_group
        self.questions = []  # type: List[Question]
        self.read_data()

    def read_data(self):
        self.questions = db.get_questions_by_foreignkey([self.question_group])

    def reset(self) -> None:
        self.beginResetModel()
        self.read_data()
        self.endResetModel()

    def rowCount(self, parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = ...) -> int:
        return len(self.questions)

    def columnCount(self, parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = ...) -> int:
        return len(QuestionGroupDataModel.activated_headers)

    def insertColumns(self, column: int, count: int,
                      parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = ...) -> bool:
        changed_columns = -1
        for i in range(column, column + count):
            if self.insertColumn(i):
                changed_columns += 1
        if changed_columns == -1:
            return False
        self.beginInsertColumns(parent, column, column + changed_columns)
        self.endInsertColumns()
        return True

    def removeColumns(self, column: int, count: int,
                      parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = ...) -> bool:
        changed_columns = -1
        for i in range(column, column + count):
            if self.removeColumn(i):
                changed_columns += 1
        if changed_columns == -1:
            return False
        self.beginRemoveColumns(parent, column, column + changed_columns)
        self.endRemoveColumns()
        return True

    @staticmethod
    def toggle_column(column: int):
        name, bool_ = QuestionGroupDataModel.headers[column]
        QuestionGroupDataModel.headers[column] = (name, not bool_)
        new_activated_headers = [question for (question, question_bool) in QuestionGroupDataModel.headers if
                                 question_bool]
        QuestionGroupDataModel.activated_headers = new_activated_headers

    def insertColumn(self, column: int,
                     parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = ...) -> bool:
        if QuestionGroupDataModel.headers[column][1]:
            return False
        self.toggle_column(column)
        return True

    def removeColumn(self, column: int,
                     parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = ...) -> bool:
        if not QuestionGroupDataModel.headers[column][1]:
            return False
        self.toggle_column(column)
        return True

    def data(self, index: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex | int,
             role: int = ...) -> Any:
        if type(index) == int:
            row = index
            col = 0
        else:
            col = index.column()
            row = index.row()

        if role == Qt.UserRole:
            return self.questions[row]

        if role != Qt.CheckStateRole and role != Qt.DisplayRole and role != Qt.ToolTipRole:
            return None

        if role == Qt.CheckStateRole:
            checkbox = self.questions[row].values(QuestionGroupDataModel.activated_headers[col]).table_checkbox
            return checkbox
        elif role == Qt.DisplayRole:
            value = self.questions[row].values(QuestionGroupDataModel.activated_headers[col]).table_value
            if type(value) == datetime.date or type(value) == datetime.datetime:
                value = str(value)
            return value
        elif role == Qt.ToolTipRole:
            tooltip = str(self.questions[row].values(QuestionGroupDataModel.activated_headers[col]).table_tooltip)
            return tooltip

    def setData(self, index: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex, value: Any,
                role: int = ...) -> bool:
        if role == Qt.UserRole:
            db.add_object(value)
            self.questions[index.row()] = value
            return True
        return False

    def headerData(self, section: int, orientation: PySide6.QtCore.Qt.Orientation, role: int = ...) -> Any:
        if orientation == Qt.Vertical:
            return None
        if role == Qt.DisplayRole:
            return Question.parameters[QuestionGroupDataModel.activated_headers[section]].table_header
        if role == Qt.UserRole:
            return {QuestionGroupDataModel.activated_headers[section]:
                        Question.parameters[QuestionGroupDataModel.activated_headers[section]]}

    def insertRows(self, row: int, count: int,
                   parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = ...) -> bool:
        inserted_count = -1
        for i in range(count):
            if self.insertRow(row + i):
                inserted_count += 1
        if inserted_count == -1:
            return False
        self.beginInsertRows(parent, row, self.rowCount() - 1)
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int,
                   parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = ...) -> bool:
        removed_count = -1
        for i in range(count):
            if self.removeRow(row + i):
                removed_count += 1
        if removed_count == -1:
            return False
        self.beginRemoveRows(parent, row, row + removed_count)
        self.endRemoveRows()
        return True

    def removeRow(self, row: int,
                  parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = ...) -> bool:
        db.delete(self.questions[row])
        self.questions.pop(row)
        return True

    def insertRow(self, row: int,
                  parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = ...) -> bool:
        new_question = Question()
        new_question.question_group = self.question_group
        new_question.question_id = db.get_new_question_id(self.question_group)
        editor = QuestionEditor(new_question)
        if editor.exec() == QDialog.Accepted:
            db.add_object(editor.question)
            self.questions.insert(row, editor.question)
            return True
        else:
            db.abort()
        return False

    def flags(self, index: PySide6.QtCore.QModelIndex |
                           PySide6.QtCore.QPersistentModelIndex) -> PySide6.QtCore.Qt.ItemFlags:
        return Qt.ItemIsDragEnabled | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def supportedDragActions(self) -> PySide6.QtCore.Qt.DropActions:
        return Qt.CopyAction


class RuleDelegate(QStyledItemDelegate):
    def createEditor(self, parent: PySide6.QtWidgets.QWidget, option: PySide6.QtWidgets.QStyleOptionViewItem,
                     index: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex) \
            -> PySide6.QtWidgets.QWidget:
        editor = QWidget(parent)
        question = index.model().data(index, role=Qt.UserRole)
        dialog = QuestionEditor(question, parent=editor)
        if dialog.exec() == QDialog.Accepted:
            # was updated
            index.model().setData(index, dialog.question, Qt.UserRole)
        else:
            db.abort()
        return editor


class QuestionGroupTableView(QTableView):
    def __init__(self, parent):
        super(QuestionGroupTableView, self).__init__(parent)
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

        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self, None, None, Qt.WidgetShortcut)
        delete_shortcut.activated.connect(self.delete_selected_items)
        force_delete_shortcut = QShortcut(QKeySequence(Qt.SHIFT | Qt.Key_Delete), self, None, None, Qt.WidgetShortcut)
        force_delete_shortcut.activated.connect(lambda: self.delete_selected_items(False))

        vertical_layout = QVBoxLayout(parent)
        vertical_layout.addWidget(self)

    def delete_selected_items(self, ask_for_confirmation=True):
        selection_model = self.selectionModel()
        if not selection_model.hasSelection():
            return
        selected_rows = sorted([index.row() for index in selection_model.selectedRows()], reverse=True)

        if ask_for_confirmation:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Fragen löschen.")
            if len(selected_rows) == 1:
                text = f"Möchtest du wirklich diese Frage löschen?"
            else:
                text = f"Möchtest du wirklich diese {len(selected_rows)} Fragen löschen?"
            msgBox.setText(text)
            msgBox.setInformativeText("Dies lässt sich nicht umkehren!")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            ret = msgBox.exec()
        else:
            ret = QMessageBox.Yes
        if ret == QMessageBox.Yes:
            for row in selected_rows:
                self.model().removeRow(row)

    def prepare_menu(self, pos: QPoint):
        actions = []

        selection_model = self.selectionModel()
        if selection_model.hasSelection():
            if len(selection_model.selectedRows()) == 1:
                text = "Diese Frage löschen"
            else:
                text = "Aktuelle Auswahl löschen"
            deleteAct = QAction(self)
            deleteAct.setText(text)
            deleteAct.triggered.connect(self.delete_selected_items)
            actions += [deleteAct]

        create_action = QAction(self)
        create_action.setText("Neue Frage erstellen")
        create_action.triggered.connect(lambda: self.model().insertRow(self.model().rowCount()))
        actions += [create_action]

        menu = QMenu(self)
        menu.addActions(actions)
        menu.exec(self.mapToGlobal(pos))

    def startDrag(self, supportedActions: Qt.DropAction) -> None:
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
        result = drag.exec(supportedActions, Qt.CopyAction)
        if result == Qt.CopyAction:
            self.clearSelection()


class RuleSortFilterProxyModel(QSortFilterProxyModel):
    filters = []  # List[Tuple[Tuple[dict_key, Callable], Tuple[str, FilterOption, Any]]]

    def filterAcceptsRow(self, source_row: int, source_parent: PySide6.QtCore.QModelIndex |
                                                               PySide6.QtCore.QPersistentModelIndex) -> bool:
        if not RuleSortFilterProxyModel.filters:
            return True

        cur_question = self.sourceModel().data(source_row, Qt.UserRole)
        answer = True
        for ((target, filter_function), _) in RuleSortFilterProxyModel.filters:
            answer = answer & filter_function(cur_question.values(target).table_value)
        return answer
