# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'regeltest_archive.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtWidgets import (QAbstractItemView, QHBoxLayout,
                               QPushButton, QSizePolicy, QSpacerItem,
                               QTableWidget, QTableWidgetItem, QVBoxLayout)


class Ui_RegeltestArchiveDialog(object):
    def setupUi(self, RegeltestArchiveDialog):
        if not RegeltestArchiveDialog.objectName():
            RegeltestArchiveDialog.setObjectName(u"RegeltestArchiveDialog")
        RegeltestArchiveDialog.resize(639, 360)
        self.verticalLayout = QVBoxLayout(RegeltestArchiveDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.regeltestTable = QTableWidget(RegeltestArchiveDialog)
        if (self.regeltestTable.columnCount() < 5):
            self.regeltestTable.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.regeltestTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.regeltestTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.regeltestTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.regeltestTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.regeltestTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        if (self.regeltestTable.rowCount() < 1):
            self.regeltestTable.setRowCount(1)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.regeltestTable.setVerticalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.regeltestTable.setItem(0, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.regeltestTable.setItem(0, 1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.regeltestTable.setItem(0, 2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.regeltestTable.setItem(0, 3, __qtablewidgetitem9)
        self.regeltestTable.setObjectName(u"regeltestTable")
        self.regeltestTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.regeltestTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.regeltestTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.regeltestTable.horizontalHeader().setCascadingSectionResizes(False)
        self.regeltestTable.horizontalHeader().setProperty("showSortIndicator", True)
        self.regeltestTable.horizontalHeader().setStretchLastSection(True)
        self.regeltestTable.verticalHeader().setVisible(False)
        self.regeltestTable.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.regeltestTable)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.load_button = QPushButton(RegeltestArchiveDialog)
        self.load_button.setObjectName(u"load_button")

        self.horizontalLayout.addWidget(self.load_button)

        self.cancel_button = QPushButton(RegeltestArchiveDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.horizontalLayout.addWidget(self.cancel_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(RegeltestArchiveDialog)
        self.load_button.clicked.connect(RegeltestArchiveDialog.accept)
        self.cancel_button.clicked.connect(RegeltestArchiveDialog.reject)

        QMetaObject.connectSlotsByName(RegeltestArchiveDialog)

    # setupUi

    def retranslateUi(self, RegeltestArchiveDialog):
        RegeltestArchiveDialog.setWindowTitle(
            QCoreApplication.translate("RegeltestArchiveDialog", u"Regeltest-Archiv", None))
        ___qtablewidgetitem = self.regeltestTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("RegeltestArchiveDialog", u"Nr.", None));
        ___qtablewidgetitem1 = self.regeltestTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("RegeltestArchiveDialog", u"Titel", None));
        ___qtablewidgetitem2 = self.regeltestTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("RegeltestArchiveDialog", u"Anzahl Fragen", None));
        ___qtablewidgetitem3 = self.regeltestTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("RegeltestArchiveDialog", u"Maximale Punktzahl", None));
        ___qtablewidgetitem4 = self.regeltestTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("RegeltestArchiveDialog", u"Datum", None));

        __sortingEnabled = self.regeltestTable.isSortingEnabled()
        self.regeltestTable.setSortingEnabled(False)
        ___qtablewidgetitem5 = self.regeltestTable.item(0, 0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("RegeltestArchiveDialog", u"1", None));
        ___qtablewidgetitem6 = self.regeltestTable.item(0, 1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("RegeltestArchiveDialog", u"A / KK Regeltest", None));
        ___qtablewidgetitem7 = self.regeltestTable.item(0, 2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("RegeltestArchiveDialog", u"15", None));
        ___qtablewidgetitem8 = self.regeltestTable.item(0, 3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("RegeltestArchiveDialog", u"30", None));
        self.regeltestTable.setSortingEnabled(__sortingEnabled)

        self.load_button.setText(QCoreApplication.translate("RegeltestArchiveDialog", u"Laden", None))
        self.cancel_button.setText(QCoreApplication.translate("RegeltestArchiveDialog", u"Abbrechen", None))
    # retranslateUi
