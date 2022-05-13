# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'self_test_dockwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QComboBox, QGridLayout, QGroupBox,
                               QLabel, QListWidget, QListWidgetItem, QSpinBox, QVBoxLayout, QWidget)

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

        self.widget = QWidget(self_test_dockwidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)

        self.mode_comboBox = QComboBox(self.groupBox_2)
        self.mode_comboBox.setObjectName(u"mode_comboBox")

        self.gridLayout_4.addWidget(self.mode_comboBox, 0, 1, 1, 1)

        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 2)

        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.question_visibility_spinbox = QSpinBox(self.groupBox)
        self.question_visibility_spinbox.setObjectName(u"question_visibility_spinbox")

        self.gridLayout_2.addWidget(self.question_visibility_spinbox, 0, 1, 1, 1)

        self.question_visibility_label = QLabel(self.groupBox)
        self.question_visibility_label.setObjectName(u"question_visibility_label")

        self.gridLayout_2.addWidget(self.question_visibility_label, 0, 0, 1, 1)

        self.auto_evaluate_label = QLabel(self.groupBox)
        self.auto_evaluate_label.setObjectName(u"auto_evaluate_label")

        self.gridLayout_2.addWidget(self.auto_evaluate_label, 1, 0, 1, 1)

        self.auto_evaluate_spinbox = QSpinBox(self.groupBox)
        self.auto_evaluate_spinbox.setObjectName(u"auto_evaluate_spinbox")

        self.gridLayout_2.addWidget(self.auto_evaluate_spinbox, 1, 1, 1, 1)

        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)

        self.verticalLayout.addWidget(self.widget)

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

        self.groupBox_2.setTitle(QCoreApplication.translate("self_test_dockwidget", u"Fragenauswahl", None))
        self.label.setText(QCoreApplication.translate("self_test_dockwidget", u"Modus", None))
        self.groupBox.setTitle(QCoreApplication.translate("self_test_dockwidget", u"Stressmodus", None))
        self.question_visibility_spinbox.setSuffix(
            QCoreApplication.translate("self_test_dockwidget", u" Sekunden", None))
        self.question_visibility_spinbox.setPrefix("")
        self.question_visibility_label.setText(
            QCoreApplication.translate("self_test_dockwidget", u"Frage ist sichtbar f\u00fcr", None))
        self.auto_evaluate_label.setText(
            QCoreApplication.translate("self_test_dockwidget", u"Automatische Evaluierung nach", None))
        self.auto_evaluate_spinbox.setSuffix(QCoreApplication.translate("self_test_dockwidget", u" Sekunden", None))
        self.auto_evaluate_spinbox.setPrefix("")
    # retranslateUi

