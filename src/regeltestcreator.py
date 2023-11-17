import random
from typing import List, Tuple

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QListWidget, QVBoxLayout, QDialog, QFileDialog, QWidget, \
    QSpacerItem, QSizePolicy, QLabel, QRadioButton
from PySide6.QtWidgets import QListWidgetItem

from src.database import db
from src.datatypes import Question, QuestionGroup, RegeltestQuestion
from src.ui_regeltest_creator_questionwidget import Ui_RegeltestCreatorQuestionWidget
from src.ui_regeltest_save import Ui_RegeltestSave
from src.ui_regeltest_setup import Ui_RegeltestSetup
from src.ui_regeltest_setup_widget import Ui_RegeltestSetup_QuestionGroup


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
        item.setToolTip(question.question)
        self.questions.append(question.signature)

    def delete_selected_items(self):
        selection_model = self.selectionModel()
        if not selection_model.hasSelection():
            return
        selected_rows = sorted([index.row() for index in selection_model.selectedRows()], reverse=True)

        for index in selected_rows:
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
                self.add_question(db.get_question(signature))


class QuestionEditWidget(QWidget, Ui_RegeltestCreatorQuestionWidget):
    def __init__(self, question: Question, parent):
        super().__init__(parent)
        self.ui = Ui_RegeltestCreatorQuestionWidget()
        self.ui.setupUi(self)

        self.question = question

        self.layout_textanswer = QVBoxLayout()
        self.label_textanswer = QLabel(self)
        self.ui.textanswer.setLayout(self.layout_textanswer)
        self.layout_textanswer.addWidget(self.label_textanswer)
        self.layout_multiple_choice = QVBoxLayout()
        self.ui.multiple_choice.setLayout(self.layout_multiple_choice)

        self.ui.label_question.setText(question.question)
        self.label_textanswer.setText(question.answer_text)
        self.label_textanswer.setWordWrap(True)

        self.ui.checkBox_multiplechoice.stateChanged.connect(self._checkbox_changed)

        self.multiple_choice = []
        for i, multiplechoice in enumerate(question.multiple_choice):
            button = QRadioButton(self)
            button.setText(multiplechoice.text)
            button.setChecked(Qt.CheckState.Checked if question.answer_index == i else Qt.CheckState.Unchecked)
            button.setDisabled(True)
            self.multiple_choice.append(button)
            self.layout_multiple_choice.addWidget(button)

        if len(self.question.multiple_choice) <= 1:
            self.ui.checkBox_multiplechoice.setDisabled(True)
            self.ui.checkBox_multiplechoice.setCheckState(Qt.CheckState.Unchecked)
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            self.ui.checkBox_multiplechoice.setDisabled(False)
            self.ui.checkBox_multiplechoice.setCheckState(Qt.CheckState.Checked)
            self.ui.stackedWidget.setCurrentIndex(1)

    def _checkbox_changed(self, new_state: Qt.CheckState):
        if new_state == Qt.CheckState.Unchecked:
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            self.ui.stackedWidget.setCurrentIndex(1)

    def get_question(self) -> RegeltestQuestion:
        return RegeltestQuestion(
            available_points=self.ui.spinBox_points.value(),
            question=self.question,
            is_multiple_choice=(self.ui.checkBox_multiplechoice.checkState() == Qt.CheckState.Checked)
        )


class RegeltestSaveDialog(QDialog, Ui_RegeltestSave):
    def __init__(self, questions: List[Question], parent):
        super().__init__(parent)
        self.ui = Ui_RegeltestSave()
        self.ui.setupUi(self)
        self.ui.icon_edit_button.clicked.connect(self.open_icon)
        self.ui.pdf_edit_button.clicked.connect(self.create_pdf_save)
        self.ui.csv_edit_button.clicked.connect(self.create_csv_save)
        self.ui.ppt_edit_button.clicked.connect(self.create_ppt_save)
        self.questions = questions
        self.question_widgets: List[QuestionEditWidget] = []

        self.ui.activate_mc_button.clicked.connect(lambda: self.change_all_mchoice(True))
        self.ui.deactivate_mc_button.clicked.connect(lambda: self.change_all_mchoice(False))

        self.ui.question_scrollable.setLayout(QVBoxLayout())

        for question in self.questions:
            widget = QuestionEditWidget(question, self)
            self.ui.question_scrollable.layout().addWidget(widget)
            self.question_widgets += [widget]

    def change_all_mchoice(self, value: bool):
        for question in self.question_widgets:
            if not question.ui.checkBox_multiplechoice.isEnabled():
                continue
            question.ui.checkBox_multiplechoice.setCheckState(Qt.Checked if value else Qt.Unchecked)

    def open_icon(self):
        file_name = QFileDialog.getOpenFileName(self, caption="Icon auswählen", filter="Icon file (*.jpg;*.png)")
        if len(file_name) == 0 or file_name[0] == "":
            return
        self.ui.icon_path_edit.setText(file_name[0])

    def create_pdf_save(self):
        file_name = QFileDialog.getSaveFileName(self, caption="Regeltest speichern", filter="Regeltest (*.pdf)")
        if len(file_name) == 0 or file_name[0] == "":
            return
        self.ui.pdf_edit.setText(file_name[0])

    def create_csv_save(self):
        file_name = QFileDialog.getSaveFileName(self, caption="CSV speichern",
                                                filter="Regeltest-Vorlage (*.csv)")
        if len(file_name) == 0 or file_name[0] == "":
            return
        self.ui.csv_edit.setText(file_name[0])

    def create_ppt_save(self):
        file_name = QFileDialog.getSaveFileName(self, caption="Powerpoint speichern",
                                                filter="Powerpoint-Regeltest (*.pptx)")
        if len(file_name) == 0 or file_name[0] == "":
            return
        self.ui.ppt_edit.setText(file_name[0])

    def get_questions(self) -> List[RegeltestQuestion]:
        return [widget.get_question() for widget in self.question_widgets]


class RegeltestSetupQuestionGroup(QWidget, Ui_RegeltestSetup_QuestionGroup):
    changed = Signal()

    def __init__(self, parent, question_group_parameters: Tuple[QuestionGroup, int, int]):
        super(RegeltestSetupQuestionGroup, self).__init__(parent)
        self.ui = Ui_RegeltestSetup_QuestionGroup()
        self.ui.setupUi(self)

        suffix = " von %d"
        self.question_group = question_group_parameters[0]
        self.ui.label_question_group.setText(
            f"{question_group_parameters[0].id:02d} - {question_group_parameters[0].name}")
        if question_group_parameters[1] == 0:
            # No Textquestion
            self.ui.spinBox_textquestion.setHidden(True)
            self.ui.label_2.setHidden(True)
            self.ui.horizontalLayout.removeItem(self.ui.right_spacer)
        self.ui.spinBox_textquestion.setRange(0, question_group_parameters[1])
        self.ui.spinBox_textquestion.setSuffix(suffix % question_group_parameters[1])
        if question_group_parameters[2] == 0:
            # No mchoice question
            self.ui.spinBox_mchoice.setHidden(True)
            self.ui.label_3.setHidden(True)
            self.ui.horizontalLayout.removeItem(self.ui.left_spacer)
        self.ui.spinBox_mchoice.setRange(0, question_group_parameters[2])
        self.ui.spinBox_mchoice.setSuffix(suffix % question_group_parameters[2])

        self.ui.spinBox_textquestion.valueChanged.connect(self.changed)
        self.ui.spinBox_mchoice.valueChanged.connect(self.changed)

    def get_parameters(self) -> Tuple[QuestionGroup, int, int]:
        return self.question_group, self.ui.spinBox_textquestion.value(), self.ui.spinBox_mchoice.value()


class RegeltestSetup(QDialog, Ui_RegeltestSetup):
    def __init__(self, parent):
        super(RegeltestSetup, self).__init__(parent)
        self.ui = Ui_RegeltestSetup()
        self.ui.setupUi(self)
        self.ui.tabWidget.clear()

        self.question_group_widgets = []  # type: List[RegeltestSetupQuestionGroup]

        parameters = db.get_question_group_config()
        divisor = 5
        for i in range(len(parameters) // divisor):
            self.create_tab(f"{parameters[i * divisor + 1][0].id:02d} - {parameters[(i + 1) * divisor - 1][0].id:02d}",
                            parameters[i * divisor:(i + 1) * divisor])
        if len(parameters) // divisor != len(parameters) / divisor:
            len_rest = len(parameters) % divisor
            if len_rest == 1:
                text = f"{parameters[-1][0].id:02d}"
            else:
                text = f"{parameters[len(parameters) - len_rest][0].id:02d} - {parameters[-1][0].id:02d}"
            self.create_tab(text, parameters[len(parameters) - len_rest:])
        self.updated()

    def updated(self):
        question_count = 0
        for question_group_widget in self.question_group_widgets:
            _, text, mchoice = question_group_widget.get_parameters()
            question_count += text + mchoice
        self.ui.statistics.setText(f"{question_count} Fragen aktuell ausgewählt ({question_count * 2} Punkte)")

    # noinspection PyUnresolvedReferences
    def create_tab(self, title: str, parameters: List[Tuple[QuestionGroup, int, int]]):
        tab_widget = QWidget()
        self.ui.tabWidget.addTab(tab_widget, title)
        layout = QVBoxLayout(tab_widget)
        for parameter in parameters:
            question_group = RegeltestSetupQuestionGroup(tab_widget, parameter)
            question_group.changed.connect(self.updated)
            layout.addWidget(question_group)
            self.question_group_widgets += [question_group]
        layout.addItem(QSpacerItem(20, 257, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def collect_questions(self):
        questions = []
        for question_group_widget in self.question_group_widgets:
            question_group, text, mchoice = question_group_widget.get_parameters()
            text_questions = []
            mchoice_questions = []
            if text:
                text_questions = db.get_questions_by_foreignkey([question_group], mchoice=False,
                                                                randomize=True)[
                                 0:text]
            if mchoice:
                mchoice_questions = db.get_questions_by_foreignkey([question_group], mchoice=True,
                                                                   randomize=True)[
                                    0:mchoice]
            text_questions += mchoice_questions
            if self.ui.checkbox_textmchoice.isChecked():
                random.shuffle(text_questions)
            questions += text_questions
        if self.ui.checkbox_question_groups.isChecked():
            random.shuffle(questions)
        return questions
