# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'downloader.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtWidgets import (QGridLayout, QLabel,
                               QProgressBar, QPushButton)


class Ui_DownloadProgress(object):
    def setupUi(self, DownloadProgress):
        if not DownloadProgress.objectName():
            DownloadProgress.setObjectName(u"DownloadProgress")
        DownloadProgress.resize(400, 170)
        self.gridLayout = QGridLayout(DownloadProgress)
        self.gridLayout.setObjectName(u"gridLayout")
        self.progressBar = QProgressBar(DownloadProgress)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.gridLayout.addWidget(self.progressBar, 1, 1, 1, 1)

        self.progress_label = QLabel(DownloadProgress)
        self.progress_label.setObjectName(u"progress_label")

        self.gridLayout.addWidget(self.progress_label, 0, 0, 1, 3)

        self.cancel_button = QPushButton(DownloadProgress)
        self.cancel_button.setObjectName(u"cancel_button")

        self.gridLayout.addWidget(self.cancel_button, 1, 2, 1, 1)

        self.retranslateUi(DownloadProgress)
        self.cancel_button.clicked.connect(DownloadProgress.reject)

        QMetaObject.connectSlotsByName(DownloadProgress)

    # setupUi

    def retranslateUi(self, DownloadProgress):
        DownloadProgress.setWindowTitle(QCoreApplication.translate("DownloadProgress", u"Dialog", None))
        self.progress_label.setText(QCoreApplication.translate("DownloadProgress", u"TextLabel", None))
        self.cancel_button.setText(QCoreApplication.translate("DownloadProgress", u"Cancel", None))
    # retranslateUi
