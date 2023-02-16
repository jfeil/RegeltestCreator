# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dataset_download_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QComboBox, QDialogButtonBox, QGridLayout, QLabel, QLineEdit)


class Ui_DownloadDialog(object):
    def setupUi(self, DownloadDialog):
        if not DownloadDialog.objectName():
            DownloadDialog.setObjectName(u"DownloadDialog")
        DownloadDialog.resize(342, 141)
        self.gridLayout = QGridLayout(DownloadDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.password_label = QLabel(DownloadDialog)
        self.password_label.setObjectName(u"password_label")

        self.gridLayout.addWidget(self.password_label, 2, 0, 1, 1)

        self.source_combobox = QComboBox(DownloadDialog)
        self.source_combobox.setObjectName(u"source_combobox")

        self.gridLayout.addWidget(self.source_combobox, 0, 0, 1, 2)

        self.username_lineedit = QLineEdit(DownloadDialog)
        self.username_lineedit.setObjectName(u"username_lineedit")

        self.gridLayout.addWidget(self.username_lineedit, 1, 1, 1, 1)

        self.password_lineedit = QLineEdit(DownloadDialog)
        self.password_lineedit.setObjectName(u"password_lineedit")
        self.password_lineedit.setInputMethodHints(
            Qt.ImhHiddenText | Qt.ImhNoAutoUppercase | Qt.ImhNoPredictiveText | Qt.ImhSensitiveData)
        self.password_lineedit.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.password_lineedit, 2, 1, 1, 1)

        self.username_label = QLabel(DownloadDialog)
        self.username_label.setObjectName(u"username_label")

        self.gridLayout.addWidget(self.username_label, 1, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(DownloadDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(DownloadDialog)
        self.buttonBox.rejected.connect(DownloadDialog.reject)

        QMetaObject.connectSlotsByName(DownloadDialog)

    # setupUi

    def retranslateUi(self, DownloadDialog):
        DownloadDialog.setWindowTitle(QCoreApplication.translate("DownloadDialog", u"Dialog", None))
        self.password_label.setText(QCoreApplication.translate("DownloadDialog", u"Password", None))
        self.username_lineedit.setText("")
        self.username_label.setText(QCoreApplication.translate("DownloadDialog", u"Username", None))
    # retranslateUi
