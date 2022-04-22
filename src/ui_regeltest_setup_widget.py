# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'regeltest_setup_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel,
                               QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
                               QWidget)


class Ui_RegeltestSetup_QuestionGroup(object):
    def setupUi(self, RegeltestSetup_QuestionGroup):
        if not RegeltestSetup_QuestionGroup.objectName():
            RegeltestSetup_QuestionGroup.setObjectName(u"RegeltestSetup_QuestionGroup")
        RegeltestSetup_QuestionGroup.resize(400, 88)
        self.verticalLayout = QVBoxLayout(RegeltestSetup_QuestionGroup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_question_group = QLabel(RegeltestSetup_QuestionGroup)
        self.label_question_group.setObjectName(u"label_question_group")

        self.verticalLayout.addWidget(self.label_question_group)

        self.widget_2 = QWidget(RegeltestSetup_QuestionGroup)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.left_spacer)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox_textquestion = QSpinBox(self.widget_2)
        self.spinBox_textquestion.setObjectName(u"spinBox_textquestion")

        self.horizontalLayout.addWidget(self.spinBox_textquestion)

        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_mchoice = QSpinBox(self.widget_2)
        self.spinBox_mchoice.setObjectName(u"spinBox_mchoice")

        self.horizontalLayout.addWidget(self.spinBox_mchoice)

        self.right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.right_spacer)


        self.verticalLayout.addWidget(self.widget_2)

        self.line = QFrame(RegeltestSetup_QuestionGroup)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.retranslateUi(RegeltestSetup_QuestionGroup)

        QMetaObject.connectSlotsByName(RegeltestSetup_QuestionGroup)

    # setupUi

    def retranslateUi(self, RegeltestSetup_QuestionGroup):
        RegeltestSetup_QuestionGroup.setWindowTitle(
            QCoreApplication.translate("RegeltestSetup_QuestionGroup", u"Form", None))
        self.label_question_group.setText(
            QCoreApplication.translate("RegeltestSetup_QuestionGroup", u"01 - Das Spielfeld", None))
        self.label_2.setText(QCoreApplication.translate("RegeltestSetup_QuestionGroup", u"Textfragen", None))
        self.spinBox_textquestion.setSuffix(
            QCoreApplication.translate("RegeltestSetup_QuestionGroup", u" out of 32", None))
        self.label_3.setText(QCoreApplication.translate("RegeltestSetup_QuestionGroup", u"Multiple choice", None))
        self.spinBox_mchoice.setSuffix(QCoreApplication.translate("RegeltestSetup_QuestionGroup", u" out of 8", None))
    # retranslateUi
