# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'first_setup_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtWidgets import (QGridLayout, QPushButton)


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

        self.import_button = QPushButton(FirstSetupWidget)
        self.import_button.setObjectName(u"import_button")

        self.gridLayout.addWidget(self.import_button, 0, 1, 1, 1)

        self.retranslateUi(FirstSetupWidget)

        QMetaObject.connectSlotsByName(FirstSetupWidget)

    # setupUi

    def retranslateUi(self, FirstSetupWidget):
        FirstSetupWidget.setWindowTitle(QCoreApplication.translate("FirstSetupWidget", u"Form", None))
        self.create_button.setText(QCoreApplication.translate("FirstSetupWidget", u"Erste Regelgruppe \n"
                                                                                  "erstellen", None))
        self.import_button.setText(QCoreApplication.translate("FirstSetupWidget", u"Existierende Regeldaten \n"
                                                                                  "importieren", None))
    # retranslateUi
