# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'self_test_dockwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QListWidget, QListWidgetItem, QVBoxLayout)


class Ui_self_test_dockwidget(object):
    def setupUi(self, self_test_dockwidget):
        if not self_test_dockwidget.objectName():
            self_test_dockwidget.setObjectName(u"self_test_dockwidget")
        self_test_dockwidget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(self_test_dockwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.self_test_question_groups = QListWidget(self_test_dockwidget)
        __qlistwidgetitem = QListWidgetItem(self.self_test_question_groups)
        __qlistwidgetitem.setCheckState(Qt.Unchecked);
        __qlistwidgetitem1 = QListWidgetItem(self.self_test_question_groups)
        __qlistwidgetitem1.setCheckState(Qt.Unchecked);
        self.self_test_question_groups.setObjectName(u"self_test_question_groups")
        self.self_test_question_groups.setSortingEnabled(False)

        self.verticalLayout.addWidget(self.self_test_question_groups)

        self.retranslateUi(self_test_dockwidget)

        QMetaObject.connectSlotsByName(self_test_dockwidget)

    # setupUi

    def retranslateUi(self, self_test_dockwidget):
        self_test_dockwidget.setWindowTitle(QCoreApplication.translate("self_test_dockwidget", u"Form", None))

        __sortingEnabled = self.self_test_question_groups.isSortingEnabled()
        self.self_test_question_groups.setSortingEnabled(False)
        ___qlistwidgetitem = self.self_test_question_groups.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("self_test_dockwidget", u"1: Test", None));
        ___qlistwidgetitem1 = self.self_test_question_groups.item(1)
        ___qlistwidgetitem1.setText(
            QCoreApplication.translate("self_test_dockwidget", u"2: M\u00f6gliche Antwort", None));
        self.self_test_question_groups.setSortingEnabled(__sortingEnabled)

    # retranslateUi
