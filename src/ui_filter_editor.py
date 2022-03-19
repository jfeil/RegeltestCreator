# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filter_editor.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QComboBox, QDialogButtonBox, QGridLayout, QLabel, QSizePolicy,
                               QSpacerItem)


class Ui_FilterEditor(object):
    def setupUi(self, FilterEditor):
        if not FilterEditor.objectName():
            FilterEditor.setObjectName(u"FilterEditor")
        FilterEditor.resize(400, 129)
        self.gridLayout = QGridLayout(FilterEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(FilterEditor)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Discard | QDialogButtonBox.Save)

        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 1)

        self.label_spalte = QLabel(FilterEditor)
        self.label_spalte.setObjectName(u"label_spalte")

        self.gridLayout.addWidget(self.label_spalte, 0, 0, 1, 1)

        self.label_filter = QLabel(FilterEditor)
        self.label_filter.setObjectName(u"label_filter")

        self.gridLayout.addWidget(self.label_filter, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 1, 1, 1)

        self.combobox_column = QComboBox(FilterEditor)
        self.combobox_column.setObjectName(u"combobox_column")

        self.gridLayout.addWidget(self.combobox_column, 0, 1, 1, 1)

        self.combobox_filteroption = QComboBox(FilterEditor)
        self.combobox_filteroption.setObjectName(u"combobox_filteroption")

        self.gridLayout.addWidget(self.combobox_filteroption, 1, 1, 1, 1)

        self.label_filteroption = QLabel(FilterEditor)
        self.label_filteroption.setObjectName(u"label_filteroption")

        self.gridLayout.addWidget(self.label_filteroption, 1, 0, 1, 1)

        self.retranslateUi(FilterEditor)
        self.buttonBox.accepted.connect(FilterEditor.accept)
        self.buttonBox.rejected.connect(FilterEditor.reject)

        QMetaObject.connectSlotsByName(FilterEditor)

    # setupUi

    def retranslateUi(self, FilterEditor):
        FilterEditor.setWindowTitle(QCoreApplication.translate("FilterEditor", u"Dialog", None))
        self.label_spalte.setText(QCoreApplication.translate("FilterEditor", u"Spalte", None))
        self.label_filter.setText(QCoreApplication.translate("FilterEditor", u"Filter", None))
        self.label_filteroption.setText(QCoreApplication.translate("FilterEditor", u"Filteroption", None))
    # retranslateUi
