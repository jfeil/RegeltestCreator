import random
from typing import List, Tuple

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QListWidget, QVBoxLayout, QDialog, QFileDialog, QWidget, \
    QSpacerItem, QSizePolicy
from PySide6.QtWidgets import QListWidgetItem

from src import controller
from src.datatypes import Question, Rulegroup
from src.ui_regeltest_save import Ui_RegeltestSave
from src.ui_regeltest_setup import Ui_RegeltestSetup
from src.ui_regeltest_setup_widget import Ui_RegeltestSetup_Rulegroup


class RegeltestCreator(QListWidget):
    def __init__(self, *args):
        super(RegeltestCreator, self).__init__(*args)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.questions = []  # type: List[str]
        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self, None, None, Qt.WidgetShortcut)
        delete_shortcut.activated.connect(self.delete_selected_items)

    def add_question(self, question: Question):
        if question.signature in self.questions:
            return
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole, question.signature)
        item.setText(question.question)
        self.questions.append(question.signature)

    def delete_selected_items(self):
        rows = sorted([index.row() for index in self.selectedIndexes()], reverse=True)
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


class RegeltestSaveDialog(QDialog, Ui_RegeltestSave):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_RegeltestSave()
        self.ui.setupUi(self)
        self.ui.icon_edit_button.clicked.connect(self.open_icon)
        self.ui.output_edit_button.clicked.connect(self.create_save)

    def open_icon(self):
        file_name = QFileDialog.getOpenFileName(self, caption="Icon auswählen", filter="Icon file (*.jpg;*.png)")
        if len(file_name) == 0 or file_name[0] == "":
            return
        self.ui.icon_path_edit.setText(file_name[0])

    def create_save(self):
        file_name = QFileDialog.getSaveFileName(self, caption="Regeltest speichern", filter="Regeltest (*.pdf)")
        if len(file_name) == 0 or file_name[0] == "":
            return
        self.ui.output_edit.setText(file_name[0])


class RegeltestSetupRulegroup(QWidget, Ui_RegeltestSetup_Rulegroup):
    changed = Signal()

    def __init__(self, parent, rulegroup_parameters: Tuple[Rulegroup, int, int]):
        super(RegeltestSetupRulegroup, self).__init__(parent)
        self.ui = Ui_RegeltestSetup_Rulegroup()
        self.ui.setupUi(self)

        suffix = " von %d"
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
        divisor = 5
        for i in range(len(parameters) // divisor):
            self.create_tab(f"{parameters[i*divisor + 1][0].id:02d} - {parameters[(i+1)*divisor-1][0].id:02d}", parameters[i*divisor:(i+1)*divisor])
        if len(parameters) // divisor != len(parameters) / divisor:
            len_rest = len(parameters) % divisor
            if len_rest == 1:
                text = f"{parameters[-1][0].id:02d}"
            else:
                text = f"{parameters[len(parameters)-len_rest][0].id:02d} - {parameters[-1][0].id:02d}"
            self.create_tab(text, parameters[len(parameters) - len_rest:])
        self.updated()

    def updated(self):
        question_count = 0
        for rulegroup_widget in self.rulegroup_widgets:
            _, text, mchoice = rulegroup_widget.get_parameters()
            question_count += text + mchoice
        self.ui.statistics.setText(f"{question_count} Fragen aktuell ausgewählt ({question_count * 2} Punkte)")

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

    def collect_questions(self):
        questions = []
        for rulegroup_widget in self.rulegroup_widgets:
            rulegroup, text, mchoice = rulegroup_widget.get_parameters()
            text_questions = []
            mchoice_questions = []
            if text:
                text_questions = controller.get_questions_by_foreignkey(rulegroup.id, mchoice=False, randomize=True)[0:text]
            if mchoice:
                mchoice_questions = controller.get_questions_by_foreignkey(rulegroup.id, mchoice=True, randomize=True)[0:mchoice]
            text_questions += mchoice_questions
            if self.ui.checkbox_textmchoice.isChecked():
                random.shuffle(text_questions)
            questions += text_questions
        if self.ui.checkbox_rulegroups.isChecked():
            random.shuffle(questions)
        return questions
