from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING
from typing import Union, List, Tuple, Dict

from PySide6.QtCore import Signal, QSortFilterProxyModel
from PySide6.QtGui import QKeySequence, QShortcut, Qt
from PySide6.QtWidgets import QWidget, QListView, QMessageBox, QDialog, QDialogButtonBox, QListWidgetItem, \
    QTreeWidgetItem

from src import main_application
from src.database import db
from src.datatypes import QuestionGroup
from src.filter_editor import FilterEditor
from src.question_table import RuleSortFilterProxyModel, QuestionGroupTableView, QuestionGroupDataModel
from src.ui_first_setup_widget import Ui_FirstSetupWidget
from src.ui_question_overview_widget import Ui_QuestionOverviewWidget
from src.ui_rulegroup_editor import Ui_RulegroupEditor

if TYPE_CHECKING:
    from src.main_application import MainWindow


class EditorResult(Enum):
    Success = auto()
    Invalid = auto()
    Canceled = auto()


class QuestionGroupEditor(QDialog, Ui_RulegroupEditor):
    def __init__(self, id: int = 1, name: str = "", parent=None):
        super(QuestionGroupEditor, self).__init__(parent=parent)
        self.ui = Ui_RulegroupEditor()
        self.ui.setupUi(self)
        self.id = id
        self.name = name

    @property
    def id(self):
        return self.ui.rulegroup_id.value()

    @id.setter
    def id(self, value):
        self.ui.rulegroup_id.setValue(value)

    @property
    def name(self):
        return self.ui.rulegroup_name.text()

    @name.setter
    def name(self, value):
        self.ui.rulegroup_name.setText(value)


class QuestionOverviewWidget(QWidget, Ui_QuestionOverviewWidget):
    def __init__(self, main_window: MainWindow):
        super(QuestionOverviewWidget, self).__init__(main_window)
        self.ui = Ui_QuestionOverviewWidget()
        self.ui.setupUi(self)
        self.main_window = main_window

        self.ui.tabWidget.clear()
        self.ui.tabWidget.setTabsClosable(True)
        self.ui.tabWidget.tabCloseRequested.connect(self.delete_question_group)
        self.ui.tabWidget.tabBarDoubleClicked.connect(self.rename_rulegroup)

        self.ui.filter_list.clear()
        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self.ui.filter_list, None, None, Qt.WidgetShortcut)
        delete_shortcut.activated.connect(self.delete_selected_filter)
        self.ui.filter_list.setSelectionMode(QListView.ExtendedSelection)
        self.ui.filter_list.itemDoubleClicked.connect(self.add_filter)
        self.ui.add_filter.clicked.connect(self.add_filter)

        self.ruletabs = []  # type: List[Tuple[QuestionGroup, QSortFilterProxyModel, QuestionGroupDataModel]]
        self.questions = {}  # type: Dict[QTreeWidgetItem, str]

    def delete_selected_filter(self):
        selection_model = self.ui.filter_list.selectionModel()
        if not selection_model.hasSelection():
            return
        selected_rows = sorted([index.row() for index in selection_model.selectedRows()], reverse=True)
        for index in selected_rows:
            self.__delete_filter(index)
        self.refresh_column_filter()

    def __delete_filter(self, index):
        RuleSortFilterProxyModel.filters.pop(index)
        filter_item = self.ui.filter_list.takeItem(index)
        del filter_item

    def delete_question_group(self, index_tabwidget: int):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Regelgruppe löschen.")
        msgBox.setText("Regelgruppe löschen.<br>"
                       "Möchtest du wirklich diese Fragengruppe löschen? Dies lässt sich nicht umkehren!")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel)
        ret = msgBox.exec()
        if ret == QMessageBox.Yes:
            rulegroup, _, _ = self.ruletabs[index_tabwidget]
            self.ruletabs.pop(index_tabwidget)
            db.delete(rulegroup)
            self.ui.tabWidget.removeTab(index_tabwidget)

        if not self.ruletabs:
            self.main_window.initialize()

    def create_question_group_tab(self, rulegroup: QuestionGroup):
        tab = QWidget()
        view = QuestionGroupTableView(tab)
        model = QuestionGroupDataModel(rulegroup, view)
        filter_model = RuleSortFilterProxyModel()
        filter_model.setSourceModel(model)
        view.setModel(filter_model)
        view.sortByColumn(0, Qt.AscendingOrder)
        self.ruletabs.append((rulegroup, filter_model, model))
        self.ui.tabWidget.addTab(tab, "")
        self._update_tabtitle(self.ui.tabWidget.indexOf(tab))

    def _rulegroup_editor(self, question_group: Union[QuestionGroup, None],
                          editor: QuestionGroupEditor) -> EditorResult:
        if editor.exec() == QDialog.Accepted:
            if question_group and question_group.id == editor.id:
                # ID was not changed -> update of title
                return EditorResult.Success
            if db.get_question_group(editor.id):
                QMessageBox(QMessageBox.Icon.Critical, "Fehler", "Regelgruppennummer existiert bereits!",
                            parent=self, ).exec()
                return EditorResult.Invalid
            return EditorResult.Success
        else:
            return EditorResult.Canceled

    def rename_rulegroup(self, index):
        if not self.ruletabs:
            return
        rulegroup, _, _ = self.ruletabs[index]
        editor = QuestionGroupEditor(id=rulegroup.id, name=rulegroup.name)
        result = self._rulegroup_editor(rulegroup, editor)
        while result == EditorResult.Invalid:
            result = self._rulegroup_editor(rulegroup, editor)
        if result == EditorResult.Success:
            rulegroup.id = editor.id
            rulegroup.name = editor.name
            self._update_tabtitle(index)
            db.commit()

    def add_question_group(self):
        editor = QuestionGroupEditor(id=db.get_new_question_group_id())
        result = self._rulegroup_editor(None, editor)
        while result == EditorResult.Invalid:
            result = self._rulegroup_editor(None, editor)
        if result == EditorResult.Success:
            if not self.ruletabs:
                self.ui.tabWidget.setTabsClosable(True)
                self.ui.add_filter.setDisabled(False)
                self.ui.tabWidget.clear()

            question_group = QuestionGroup(id=editor.id, name=editor.name)
            db.add_object(question_group)
            self.create_question_group_tab(question_group)

    def _update_tabtitle(self, index):
        rulegroup, _, _ = self.ruletabs[index]
        self.ui.tabWidget.setTabText(index, f"{rulegroup.id:02d} {rulegroup.name}")

    def add_filter(self, list_entry: Union[QListWidgetItem, bool] = False):
        if not list_entry or type(list_entry) == bool:
            # Add filter mode -> no list entry double_clicked
            current_configuration = None
            edit_mode = False
        else:
            # Edit mode -> Doubleclick on existing entry!
            index = self.ui.filter_list.indexFromItem(list_entry).row()
            current_configuration = RuleSortFilterProxyModel.filters[index][1]
            edit_mode = True
        first_ruletab = self.ruletabs[0][2]
        properties = {}
        for i in range(first_ruletab.columnCount()):
            properties.update(first_ruletab.headerData(i, Qt.Horizontal, Qt.UserRole))
        editor = FilterEditor(filter_configuration=properties, current_filter=current_configuration)
        editor.exec()
        if editor.result == QDialogButtonBox.ButtonRole.DestructiveRole:
            # Closed via Discard
            if not edit_mode:
                return
            else:
                self.__delete_filter(index)
        elif editor.result == QDialogButtonBox.ButtonRole.AcceptRole:
            # Closed via Save
            dict_key, filter_option, filter_value = editor.current_configuration()
            if not edit_mode:
                RuleSortFilterProxyModel.filters += [(editor.create_filter(), (dict_key, filter_option, filter_value))]
                self.ui.filter_list.addItem(
                    QListWidgetItem(f"{properties[dict_key].table_header} {filter_option} '{filter_value}'"))
            else:
                RuleSortFilterProxyModel.filters[index] = (
                    editor.create_filter(), (dict_key, filter_option, filter_value))
                list_entry.setText(f"{properties[dict_key].table_header} {filter_option} '{filter_value}'")
        elif editor.result == QDialogButtonBox.ButtonRole.RejectRole:
            # Closed via Cancel
            return
        elif editor.result is None:
            # Closed via X
            return
        else:
            raise ValueError(f"Invalid response {editor.result}")
        self.refresh_column_filter()

    def refresh_column_filter(self):
        for (_, filter_model, _) in self.ruletabs:
            filter_model = filter_model  # type: RuleSortFilterProxyModel
            filter_model.invalidateFilter()

    def create_ruletabs(self, rulegroups: List[QuestionGroup]):
        self.ui.tabWidget.setTabsClosable(True)
        self.ui.add_filter.setDisabled(False)
        for rulegroup in rulegroups:
            self.create_question_group_tab(rulegroup)

    def reset(self):
        for (_, _, model) in self.ruletabs:
            model.reset()


class FirstSetupWidget(QWidget, Ui_FirstSetupWidget):
    action_done = Signal()

    def __init__(self, main_window: MainWindow):
        super(FirstSetupWidget, self).__init__(main_window)
        self.ui = Ui_FirstSetupWidget()
        self.ui.setupUi(self)

        self.ui.create_button.clicked.connect(main_window.add_question_group)
        self.ui.import_button.clicked.connect(self.load_dataset)

    def load_dataset(self):
        main_application.load_dataset(self.parent())
        self.action_done.emit()
