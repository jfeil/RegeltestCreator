# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'update_checker.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QComboBox, QHBoxLayout,
                               QLabel, QProgressBar, QPushButton, QSizePolicy,
                               QVBoxLayout)

class Ui_UpdateChecker(object):
    def setupUi(self, UpdateChecker):
        if not UpdateChecker.objectName():
            UpdateChecker.setObjectName(u"UpdateChecker")
        UpdateChecker.resize(619, 436)
        self.verticalLayout = QVBoxLayout(UpdateChecker)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.text = QLabel(UpdateChecker)
        self.text.setObjectName(u"text")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text.sizePolicy().hasHeightForWidth())
        self.text.setSizePolicy(sizePolicy)
        self.text.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.verticalLayout.addWidget(self.text)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(UpdateChecker)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.comboBox = QComboBox(UpdateChecker)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.download_progress = QProgressBar(UpdateChecker)
        self.download_progress.setObjectName(u"download_progress")
        self.download_progress.setEnabled(True)
        self.download_progress.setValue(24)

        self.verticalLayout.addWidget(self.download_progress)

        self.install_update_button = QPushButton(UpdateChecker)
        self.install_update_button.setObjectName(u"install_update_button")

        self.verticalLayout.addWidget(self.install_update_button)

        self.retranslateUi(UpdateChecker)

        QMetaObject.connectSlotsByName(UpdateChecker)
    # setupUi

    def retranslateUi(self, UpdateChecker):
        UpdateChecker.setWindowTitle(QCoreApplication.translate("UpdateChecker", u"Dialog", None))
        self.text.setText(QCoreApplication.translate("UpdateChecker",
                                                     u"<html><head/><body><p>VERSION</p><p><br/></p><p><br/></p><p>TEST<br/></p></body></html>",
                                                     None))
        self.label_3.setText(QCoreApplication.translate("UpdateChecker", u"Gesuchte Version", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("UpdateChecker", u"Release", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("UpdateChecker", u"Development", None))

        self.install_update_button.setText(
            QCoreApplication.translate("UpdateChecker", u"Neuste Version installieren", None))
    # retranslateUi

