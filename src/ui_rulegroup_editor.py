# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rulegroup_editor.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QAbstractSpinBox, QDialogButtonBox, QGridLayout, QLineEdit, QSizePolicy,
                               QSpinBox)


class Ui_RulegroupEditor(object):
    def setupUi(self, RulegroupEditor):
        if not RulegroupEditor.objectName():
            RulegroupEditor.setObjectName(u"QuestionGroupEditor")
        RulegroupEditor.resize(293, 69)
        self.gridLayout = QGridLayout(RulegroupEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.rulegroup_name = QLineEdit(RulegroupEditor)
        self.rulegroup_name.setObjectName(u"rulegroup_name")

        self.gridLayout.addWidget(self.rulegroup_name, 1, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(RulegroupEditor)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.rulegroup_id = QSpinBox(RulegroupEditor)
        self.rulegroup_id.setObjectName(u"rulegroup_id")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rulegroup_id.sizePolicy().hasHeightForWidth())
        self.rulegroup_id.setSizePolicy(sizePolicy)
        self.rulegroup_id.setMinimum(1)
        self.rulegroup_id.setMaximum(99)
        self.rulegroup_id.setStepType(QAbstractSpinBox.DefaultStepType)

        self.gridLayout.addWidget(self.rulegroup_id, 1, 0, 1, 1)

        self.retranslateUi(RulegroupEditor)
        self.buttonBox.accepted.connect(RulegroupEditor.accept)
        self.buttonBox.rejected.connect(RulegroupEditor.reject)

        QMetaObject.connectSlotsByName(RulegroupEditor)

    # setupUi

    def retranslateUi(self, RulegroupEditor):
        RulegroupEditor.setWindowTitle(QCoreApplication.translate("QuestionGroupEditor", u"Regelgruppe", None))
    # retranslateUi
