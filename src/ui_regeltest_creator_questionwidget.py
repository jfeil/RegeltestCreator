# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'regeltest_creator_questionwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtWidgets import (QCheckBox, QHBoxLayout, QLabel,
                               QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
                               QVBoxLayout, QWidget)


class Ui_RegeltestCreatorQuestionWidget(object):
    def setupUi(self, RegeltestCreatorQuestionWidget):
        if not RegeltestCreatorQuestionWidget.objectName():
            RegeltestCreatorQuestionWidget.setObjectName(u"RegeltestCreatorQuestionWidget")
        RegeltestCreatorQuestionWidget.resize(508, 168)
        self.horizontalLayout = QHBoxLayout(RegeltestCreatorQuestionWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_question = QVBoxLayout()
        self.verticalLayout_question.setObjectName(u"verticalLayout_question")
        self.label_question = QLabel(RegeltestCreatorQuestionWidget)
        self.label_question.setObjectName(u"label_question")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_question.sizePolicy().hasHeightForWidth())
        self.label_question.setSizePolicy(sizePolicy)
        self.label_question.setWordWrap(True)

        self.verticalLayout_question.addWidget(self.label_question)

        self.stackedWidget = QStackedWidget(RegeltestCreatorQuestionWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.textanswer = QWidget()
        self.textanswer.setObjectName(u"textanswer")
        self.stackedWidget.addWidget(self.textanswer)
        self.multiple_choice = QWidget()
        self.multiple_choice.setObjectName(u"multiple_choice")
        self.stackedWidget.addWidget(self.multiple_choice)

        self.verticalLayout_question.addWidget(self.stackedWidget)

        self.horizontalLayout.addLayout(self.verticalLayout_question)

        self.verticalLayout_settings = QVBoxLayout()
        self.verticalLayout_settings.setObjectName(u"verticalLayout_settings")
        self.checkBox_multiplechoice = QCheckBox(RegeltestCreatorQuestionWidget)
        self.checkBox_multiplechoice.setObjectName(u"checkBox_multiplechoice")

        self.verticalLayout_settings.addWidget(self.checkBox_multiplechoice)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_settings.addItem(self.verticalSpacer)

        self.spinBox_points = QSpinBox(RegeltestCreatorQuestionWidget)
        self.spinBox_points.setObjectName(u"spinBox_points")
        self.spinBox_points.setValue(2)

        self.verticalLayout_settings.addWidget(self.spinBox_points)

        self.horizontalLayout.addLayout(self.verticalLayout_settings)

        self.retranslateUi(RegeltestCreatorQuestionWidget)

        self.stackedWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(RegeltestCreatorQuestionWidget)

    # setupUi

    def retranslateUi(self, RegeltestCreatorQuestionWidget):
        RegeltestCreatorQuestionWidget.setWindowTitle(
            QCoreApplication.translate("RegeltestCreatorQuestionWidget", u"Form", None))
        self.label_question.setText(
            QCoreApplication.translate("RegeltestCreatorQuestionWidget", u"Question Text LOREM IPSUM DOLOR SIT AMED",
                                       None))
        self.checkBox_multiplechoice.setText(
            QCoreApplication.translate("RegeltestCreatorQuestionWidget", u"Multiplechoice?", None))
        self.spinBox_points.setSuffix(QCoreApplication.translate("RegeltestCreatorQuestionWidget", u" Punkte", None))
    # retranslateUi
