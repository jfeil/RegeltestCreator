# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'question_editor.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QCheckBox, QComboBox,
                               QDialogButtonBox, QGridLayout, QHBoxLayout,
                               QLabel, QLineEdit, QTextEdit,
                               QWidget)


class Ui_QuestionDialog(object):
    def setupUi(self, QuestionDialog):
        if not QuestionDialog.objectName():
            QuestionDialog.setObjectName(u"QuestionDialog")
        QuestionDialog.resize(505, 541)
        self.gridLayout = QGridLayout(QuestionDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.question_label = QLabel(QuestionDialog)
        self.question_label.setObjectName(u"question_label")

        self.gridLayout.addWidget(self.question_label, 0, 0, 1, 1)

        self.question_edit = QTextEdit(QuestionDialog)
        self.question_edit.setObjectName(u"question_edit")

        self.gridLayout.addWidget(self.question_edit, 0, 1, 1, 1)

        self.label_a = QLabel(QuestionDialog)
        self.label_a.setObjectName(u"label_a")
        self.label_a.setEnabled(True)

        self.gridLayout.addWidget(self.label_a, 1, 0, 1, 1)

        self.option_1_edit = QLineEdit(QuestionDialog)
        self.option_1_edit.setObjectName(u"option_1_edit")
        self.option_1_edit.setEnabled(True)

        self.gridLayout.addWidget(self.option_1_edit, 1, 1, 1, 1)

        self.label_b = QLabel(QuestionDialog)
        self.label_b.setObjectName(u"label_b")
        self.label_b.setEnabled(True)

        self.gridLayout.addWidget(self.label_b, 2, 0, 1, 1)

        self.option_2_edit = QLineEdit(QuestionDialog)
        self.option_2_edit.setObjectName(u"option_2_edit")
        self.option_2_edit.setEnabled(True)

        self.gridLayout.addWidget(self.option_2_edit, 2, 1, 1, 1)

        self.label_c = QLabel(QuestionDialog)
        self.label_c.setObjectName(u"label_c")
        self.label_c.setEnabled(True)

        self.gridLayout.addWidget(self.label_c, 3, 0, 1, 1)

        self.option_3_edit = QLineEdit(QuestionDialog)
        self.option_3_edit.setObjectName(u"option_3_edit")
        self.option_3_edit.setEnabled(True)

        self.gridLayout.addWidget(self.option_3_edit, 3, 1, 1, 1)

        self.checkBox = QCheckBox(QuestionDialog)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setLayoutDirection(Qt.LeftToRight)
        self.checkBox.setTristate(False)

        self.gridLayout.addWidget(self.checkBox, 4, 1, 1, 1)

        self.answer_label = QLabel(QuestionDialog)
        self.answer_label.setObjectName(u"answer_label")

        self.gridLayout.addWidget(self.answer_label, 5, 0, 1, 1)

        self.created_label = QLabel(QuestionDialog)
        self.created_label.setObjectName(u"created_label")

        self.gridLayout.addWidget(self.created_label, 6, 0, 1, 1)

        self.created_value = QLabel(QuestionDialog)
        self.created_value.setObjectName(u"created_value")

        self.gridLayout.addWidget(self.created_value, 6, 1, 1, 1)

        self.edited_label = QLabel(QuestionDialog)
        self.edited_label.setObjectName(u"edited_label")

        self.gridLayout.addWidget(self.edited_label, 7, 0, 1, 1)

        self.edited_value = QLabel(QuestionDialog)
        self.edited_value.setObjectName(u"edited_value")

        self.gridLayout.addWidget(self.edited_value, 7, 1, 1, 1)

        self.signature_label = QLabel(QuestionDialog)
        self.signature_label.setObjectName(u"signature_label")

        self.gridLayout.addWidget(self.signature_label, 8, 0, 1, 1)

        self.signature_value = QLabel(QuestionDialog)
        self.signature_value.setObjectName(u"signature_value")

        self.gridLayout.addWidget(self.signature_value, 8, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(QuestionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 2)

        self.widget = QWidget(QuestionDialog)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.mchoice_combo = QComboBox(self.widget)
        self.mchoice_combo.addItem("")
        self.mchoice_combo.addItem("")
        self.mchoice_combo.addItem("")
        self.mchoice_combo.addItem("")
        self.mchoice_combo.setObjectName(u"mchoice_combo")

        self.horizontalLayout.addWidget(self.mchoice_combo)

        self.answer_edit = QTextEdit(self.widget)
        self.answer_edit.setObjectName(u"answer_edit")

        self.horizontalLayout.addWidget(self.answer_edit)

        self.gridLayout.addWidget(self.widget, 5, 1, 1, 1)

        self.retranslateUi(QuestionDialog)
        self.buttonBox.rejected.connect(QuestionDialog.reject)

        self.mchoice_combo.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(QuestionDialog)

    # setupUi

    def retranslateUi(self, QuestionDialog):
        QuestionDialog.setWindowTitle(QCoreApplication.translate("QuestionDialog", u"Dialog", None))
        self.question_label.setText(QCoreApplication.translate("QuestionDialog", u"Question", None))
        self.label_a.setText(QCoreApplication.translate("QuestionDialog", u"Option A", None))
        self.label_b.setText(QCoreApplication.translate("QuestionDialog", u"Option B", None))
        self.option_2_edit.setText("")
        self.label_c.setText(QCoreApplication.translate("QuestionDialog", u"Option C", None))
        self.checkBox.setText(QCoreApplication.translate("QuestionDialog", u"Multiple Choice", None))
        self.answer_label.setText(QCoreApplication.translate("QuestionDialog", u"Answer", None))
        self.created_label.setText(QCoreApplication.translate("QuestionDialog", u"Created", None))
        self.created_value.setText(QCoreApplication.translate("QuestionDialog", u"TextLabel", None))
        self.edited_label.setText(QCoreApplication.translate("QuestionDialog", u"Last edited", None))
        self.edited_value.setText(QCoreApplication.translate("QuestionDialog", u"TextLabel", None))
        self.signature_label.setText(QCoreApplication.translate("QuestionDialog", u"Signature", None))
        self.signature_value.setText(QCoreApplication.translate("QuestionDialog", u"TextLabel", None))
        self.mchoice_combo.setItemText(0, "")
        self.mchoice_combo.setItemText(1, QCoreApplication.translate("QuestionDialog", u"A", None))
        self.mchoice_combo.setItemText(2, QCoreApplication.translate("QuestionDialog", u"B", None))
        self.mchoice_combo.setItemText(3, QCoreApplication.translate("QuestionDialog", u"C", None))

    # retranslateUi
