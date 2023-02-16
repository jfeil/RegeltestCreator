# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'first_setup_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtWidgets import (QGridLayout, QPushButton, QVBoxLayout)


class Ui_FirstSetupWidget(object):
    def setupUi(self, FirstSetupWidget):
        if not FirstSetupWidget.objectName():
            FirstSetupWidget.setObjectName(u"FirstSetupWidget")
        FirstSetupWidget.resize(466, 228)
        self.gridLayout = QGridLayout(FirstSetupWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.create_button = QPushButton(FirstSetupWidget)
        self.create_button.setObjectName(u"create_button")

        self.gridLayout.addWidget(self.create_button, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.import_local_button = QPushButton(FirstSetupWidget)
        self.import_local_button.setObjectName(u"import_local_button")

        self.verticalLayout.addWidget(self.import_local_button)

        self.import_internet_button = QPushButton(FirstSetupWidget)
        self.import_internet_button.setObjectName(u"import_internet_button")

        self.verticalLayout.addWidget(self.import_internet_button)

        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.retranslateUi(FirstSetupWidget)

        QMetaObject.connectSlotsByName(FirstSetupWidget)
    # setupUi

    def retranslateUi(self, FirstSetupWidget):
        FirstSetupWidget.setWindowTitle(QCoreApplication.translate("FirstSetupWidget", u"Form", None))
        self.create_button.setText(QCoreApplication.translate("FirstSetupWidget", u"Erste Regelgruppe erstellen", None))
        self.import_local_button.setText(QCoreApplication.translate("FirstSetupWidget", u"Aus Datei importieren", None))
        self.import_internet_button.setText(
            QCoreApplication.translate("FirstSetupWidget", u"Aus dem Internet importieren", None))
    # retranslateUi

