# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'question_group_editor.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QAbstractSpinBox, QDialogButtonBox, QGridLayout, QLineEdit, QSizePolicy,
                               QSpinBox)


class Ui_QuestionGroupEditor(object):
    def setupUi(self, QuestionGroupEditor):
        if not QuestionGroupEditor.objectName():
            QuestionGroupEditor.setObjectName(u"QuestionGroupEditor")
        QuestionGroupEditor.resize(293, 69)
        self.gridLayout = QGridLayout(QuestionGroupEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.question_group_name = QLineEdit(QuestionGroupEditor)
        self.question_group_name.setObjectName(u"question_group_name")

        self.gridLayout.addWidget(self.question_group_name, 1, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(QuestionGroupEditor)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.question_group_id = QSpinBox(QuestionGroupEditor)
        self.question_group_id.setObjectName(u"question_group_id")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.question_group_id.sizePolicy().hasHeightForWidth())
        self.question_group_id.setSizePolicy(sizePolicy)
        self.question_group_id.setMinimum(1)
        self.question_group_id.setMaximum(99)
        self.question_group_id.setStepType(QAbstractSpinBox.DefaultStepType)

        self.gridLayout.addWidget(self.question_group_id, 1, 0, 1, 1)

        self.retranslateUi(QuestionGroupEditor)
        self.buttonBox.accepted.connect(QuestionGroupEditor.accept)
        self.buttonBox.rejected.connect(QuestionGroupEditor.reject)

        QMetaObject.connectSlotsByName(QuestionGroupEditor)

    # setupUi

    def retranslateUi(self, QuestionGroupEditor):
        QuestionGroupEditor.setWindowTitle(QCoreApplication.translate("QuestionGroupEditor", u"Regelgruppe", None))
    # retranslateUi
