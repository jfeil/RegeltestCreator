# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'regeltest_creator_dockwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtWidgets import (QFrame, QGridLayout, QLabel,
                               QPushButton, QVBoxLayout,
                               QWidget)

from .regeltestcreator import RegeltestCreator


class Ui_regeltest_creator_dockwidget(object):
    def setupUi(self, regeltest_creator_dockwidget):
        if not regeltest_creator_dockwidget.objectName():
            regeltest_creator_dockwidget.setObjectName(u"regeltest_creator_dockwidget")
        regeltest_creator_dockwidget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(regeltest_creator_dockwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.regeltest_list = RegeltestCreator(regeltest_creator_dockwidget)
        self.regeltest_list.setObjectName(u"regeltest_list")

        self.verticalLayout.addWidget(self.regeltest_list)

        self.widget = QWidget(regeltest_creator_dockwidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.add_questionlist = QPushButton(self.widget)
        self.add_questionlist.setObjectName(u"add_questionlist")

        self.gridLayout.addWidget(self.add_questionlist, 0, 0, 1, 1)

        self.clear_questionlist = QPushButton(self.widget)
        self.clear_questionlist.setObjectName(u"clear_questionlist")

        self.gridLayout.addWidget(self.clear_questionlist, 0, 1, 1, 1)

        self.verticalLayout.addWidget(self.widget)

        self.line = QFrame(regeltest_creator_dockwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.regeltest_stats = QLabel(regeltest_creator_dockwidget)
        self.regeltest_stats.setObjectName(u"regeltest_stats")

        self.verticalLayout.addWidget(self.regeltest_stats)

        self.create_regeltest = QPushButton(regeltest_creator_dockwidget)
        self.create_regeltest.setObjectName(u"create_regeltest")

        self.verticalLayout.addWidget(self.create_regeltest)

        self.retranslateUi(regeltest_creator_dockwidget)

        QMetaObject.connectSlotsByName(regeltest_creator_dockwidget)

    # setupUi

    def retranslateUi(self, regeltest_creator_dockwidget):
        regeltest_creator_dockwidget.setWindowTitle(
            QCoreApplication.translate("regeltest_creator_dockwidget", u"Form", None))
        self.add_questionlist.setText(QCoreApplication.translate("regeltest_creator_dockwidget", u"Einrichten", None))
        self.clear_questionlist.setText(
            QCoreApplication.translate("regeltest_creator_dockwidget", u"Zur\u00fccksetzen", None))
        self.regeltest_stats.setText(
            QCoreApplication.translate("regeltest_creator_dockwidget", u"0 Fragen ausgew\u00e4hlt (0 Punkte)", None))
        self.create_regeltest.setText(
            QCoreApplication.translate("regeltest_creator_dockwidget", u"Regeltest erstellen", None))
    # retranslateUi
