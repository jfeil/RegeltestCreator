from typing import Dict, List, Tuple

from PySide6.QtCore import Qt, QCoreApplication, Signal
from PySide6.QtGui import QDrag, QShortcut, QKeySequence
from PySide6.QtWidgets import QListWidget, QTreeWidgetItem, QTreeWidget, QVBoxLayout, QDialog, QFileDialog, QWidget, \
    QSpacerItem, QSizePolicy
from PySide6.QtWidgets import QListWidgetItem

from src import controller
from src.datatypes import Question, Rulegroup
from src.question_editor import QuestionEditor
from src.ui_regeltest_save import Ui_RegeltestSave
from src.ui_regeltest_setup import Ui_RegeltestSetup
from src.ui_regeltest_setup_widget import Ui_RegeltestSetup_Rulegroup


class RegeltestCreator(QListWidget):
    def __init__(self, *args):
        super(RegeltestCreator, self).__init__(*args)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.MultiSelection)
        self.questions = []  # type: List[str]
        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self)
        delete_shortcut.activated.connect(self.remove_selected_items)
        self

    def add_question(self, question: Question):
        if question.signature in self.questions:
            return
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole, question.signature)
        item.setText(question.question)
        self.questions.append(question.signature)

    def remove_selected_items(self):
        rows = [index.row() for index in self.selectedIndexes()[::-1]]
        if not rows:
            return
        for index in rows:
            self.questions.pop(index)
            item = self.takeItem(index)
            del item

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


class RegeltestSetupRulegroup(QWidget, Ui_RegeltestSetup_Rulegroup):
    changed = Signal()

    def __init__(self, parent, rulegroup_parameters: Tuple[Rulegroup, int, int]):
        super(RegeltestSetupRulegroup, self).__init__(parent)
        self.ui = Ui_RegeltestSetup_Rulegroup()
        self.ui.setupUi(self)

        suffix = " out of %d"
        self.rulegroup = rulegroup_parameters[0]
        self.ui.label_rulegroup.setText(f"{rulegroup_parameters[0].id:02d} - {rulegroup_parameters[0].name}")
        if rulegroup_parameters[1] == 0:
            # No Textquestion
            self.ui.spinBox_textquestion.setHidden(True)
            self.ui.label_2.setHidden(True)
            self.ui.horizontalLayout.removeItem(self.ui.right_spacer)
        self.ui.spinBox_textquestion.setRange(0, rulegroup_parameters[1])
        self.ui.spinBox_textquestion.setSuffix(suffix % rulegroup_parameters[1])
        if rulegroup_parameters[2] == 0:
            # No mchoice question
            self.ui.spinBox_mchoice.setHidden(True)
            self.ui.label_3.setHidden(True)
            self.ui.horizontalLayout.removeItem(self.ui.left_spacer)
        self.ui.spinBox_mchoice.setRange(0, rulegroup_parameters[2])
        self.ui.spinBox_mchoice.setSuffix(suffix % rulegroup_parameters[2])

        self.ui.spinBox_textquestion.valueChanged.connect(self.changed)
        self.ui.spinBox_mchoice.valueChanged.connect(self.changed)

    def get_parameters(self) -> Tuple[Rulegroup, int, int]:
        return self.rulegroup, self.ui.spinBox_textquestion.value(), self.ui.spinBox_mchoice.value()


class RegeltestSetup(QDialog, Ui_RegeltestSetup):
    def __init__(self, parent):
        super(RegeltestSetup, self).__init__(parent)
        self.ui = Ui_RegeltestSetup()
        self.ui.setupUi(self)
        self.ui.tabWidget.clear()

        self.rulegroup_widgets = []  # type: List[RegeltestSetupRulegroup]

        parameters = controller.get_rulegroup_config()
        divisor = 6
        for i in range(len(parameters) // divisor):
            self.create_tab(f"{i*divisor + 1:02d} - {(i+1)*divisor:02d}", parameters[i*divisor:(i+1)*divisor])
        if len(parameters) // divisor != len(parameters) / divisor:
            len_rest = len(parameters) % divisor
            if len_rest == 1:
                text = f"{len(parameters):02d}"
            else:
                text = f"{len(parameters) - len_rest:02d} - {len(parameters):02d}"
            self.create_tab(text, parameters[len(parameters) - len_rest:])

    def updated(self):
        question_count = 0
        for rulegroup_widget in self.rulegroup_widgets:
            _, text, mchoice = rulegroup_widget.get_parameters()
            question_count += text + mchoice
        print(question_count)

    def create_tab(self, title: str, parameters: List[Tuple[Rulegroup, int, int]]):
        tab_widget = QWidget()
        self.ui.tabWidget.addTab(tab_widget, title)
        layout = QVBoxLayout(tab_widget)
        for parameter in parameters:
            rulegroup = RegeltestSetupRulegroup(tab_widget, parameter)
            rulegroup.changed.connect(self.updated)
            layout.addWidget(rulegroup)
            self.rulegroup_widgets += [rulegroup]
        layout.addItem(QSpacerItem(20, 257, QSizePolicy.Minimum, QSizePolicy.Expanding))