import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from src.database import db
from src.datatypes import Question, MultipleChoice
from src.ui_question_editor import Ui_QuestionDialog


def bool_2_checkstate(value: bool):
    if value:
        return Qt.CheckState.Checked
    return Qt.CheckState.Unchecked


def checkstate_2_bool(value: Qt.CheckState):
    if value == Qt.CheckState.Checked:
        return True
    return False


class QuestionEditor(QDialog, Ui_QuestionDialog):
    def __init__(self, question: Question, parent=None, window_flags=Qt.Dialog):
        super(QuestionEditor, self).__init__(parent, window_flags)
        self.ui = Ui_QuestionDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Frage bearbeiten")
        self.question = question
        self.mchoice = []
        if question.answer_index == -1:
            mchoice = False
            index = 0
        else:
            mchoice = True
            multiple_choice = db.get_multiplechoice_by_foreignkey(question)
            for mchoice_option in multiple_choice:
                if mchoice_option.index == 0:
                    self.ui.option_1_edit.setText(mchoice_option.text)
                elif mchoice_option.index == 1:
                    self.ui.option_2_edit.setText(mchoice_option.text)
                elif mchoice_option.index == 2:
                    self.ui.option_3_edit.setText(mchoice_option.text)
            index = question.answer_index + 1
        self.ui.checkBox.setCheckState(bool_2_checkstate(mchoice))
        self.ui.checkBox.checkStateChanged.connect(self.mchoice_changed)
        self.activate_mchoice(checkstate_2_bool(self.ui.checkBox.checkState()))
        self.ui.mchoice_combo.setCurrentIndex(index)

        self.ui.question_edit.setText(question.question)
        self.ui.answer_edit.setText(question.answer_text)
        self.ui.signature_value.setText(question.signature)
        self.ui.edited_value.setText(str(question.last_edited))
        self.ui.created_value.setText(str(question.created))

        self.ui.buttonBox.accepted.connect(self.save_changes)

    def mchoice_changed(self, value: Qt.CheckState):
        self.activate_mchoice(checkstate_2_bool(value))

    def activate_mchoice(self, value: bool):
        value = not value
        self.ui.option_1_edit.setDisabled(value)
        self.ui.option_2_edit.setDisabled(value)
        self.ui.option_3_edit.setDisabled(value)
        self.ui.mchoice_combo.setDisabled(value)

    def save_changes(self):
        self.question.question = self.ui.question_edit.toPlainText()
        self.question.answer_text = self.ui.answer_edit.toPlainText()
        if checkstate_2_bool(self.ui.checkBox.checkState()):
            # activated
            self.question.answer_index = self.ui.mchoice_combo.currentIndex() - 1
            self.mchoice += [MultipleChoice(index=0, text=self.ui.option_1_edit.text())]
            self.mchoice += [MultipleChoice(index=1, text=self.ui.option_2_edit.text())]
            self.mchoice += [MultipleChoice(index=2, text=self.ui.option_3_edit.text())]
        else:
            self.question.answer_index = -1
        self.question.last_edited = datetime.date.today()
        self.question.multiple_choice = self.mchoice
        if self.ui.mchoice_combo.currentIndex() == 0 and checkstate_2_bool(self.ui.checkBox.checkState()):
            # wrong! Don't close!
            pass
        else:
            self.accept()
