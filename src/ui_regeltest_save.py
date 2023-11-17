# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'regeltest_save.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            Qt)
from PySide6.QtWidgets import (QCheckBox, QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QScrollArea,
                               QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_RegeltestSave(object):
    def setupUi(self, RegeltestSave):
        if not RegeltestSave.objectName():
            RegeltestSave.setObjectName(u"RegeltestSave")
        RegeltestSave.resize(760, 566)
        RegeltestSave.setFocusPolicy(Qt.NoFocus)
        self.gridLayout = QGridLayout(RegeltestSave)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(RegeltestSave)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.icon_path_edit = QLineEdit(self.widget)
        self.icon_path_edit.setObjectName(u"icon_path_edit")

        self.horizontalLayout.addWidget(self.icon_path_edit)

        self.icon_edit_button = QPushButton(self.widget)
        self.icon_edit_button.setObjectName(u"icon_edit_button")

        self.horizontalLayout.addWidget(self.icon_edit_button)

        self.gridLayout.addWidget(self.widget, 1, 5, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 22, 0, 1, 1)

        self.widget_6 = QWidget(RegeltestSave)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.ppt_edit = QLineEdit(self.widget_6)
        self.ppt_edit.setObjectName(u"ppt_edit")

        self.horizontalLayout_8.addWidget(self.ppt_edit)

        self.ppt_edit_button = QPushButton(self.widget_6)
        self.ppt_edit_button.setObjectName(u"ppt_edit_button")

        self.horizontalLayout_8.addWidget(self.ppt_edit_button)

        self.gridLayout.addWidget(self.widget_6, 11, 2, 1, 1)

        self.widget_4 = QWidget(RegeltestSave)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.csv_edit = QLineEdit(self.widget_4)
        self.csv_edit.setObjectName(u"csv_edit")

        self.horizontalLayout_5.addWidget(self.csv_edit)

        self.csv_edit_button = QPushButton(self.widget_4)
        self.csv_edit_button.setObjectName(u"csv_edit_button")

        self.horizontalLayout_5.addWidget(self.csv_edit_button)

        self.gridLayout.addWidget(self.widget_4, 15, 2, 1, 4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.activate_mc_button = QPushButton(RegeltestSave)
        self.activate_mc_button.setObjectName(u"activate_mc_button")

        self.horizontalLayout_4.addWidget(self.activate_mc_button)

        self.deactivate_mc_button = QPushButton(RegeltestSave)
        self.deactivate_mc_button.setObjectName(u"deactivate_mc_button")

        self.horizontalLayout_4.addWidget(self.deactivate_mc_button)

        self.gridLayout.addLayout(self.horizontalLayout_4, 21, 0, 1, 6)

        self.label_4 = QLabel(RegeltestSave)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 6, 3, 1, 1)

        self.label_2 = QLabel(RegeltestSave)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)

        self.label_10 = QLabel(RegeltestSave)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 14, 0, 1, 1)

        self.line = QFrame(RegeltestSave)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 13, 0, 1, 6)

        self.label_3 = QLabel(RegeltestSave)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)

        self.widget_3 = QWidget(RegeltestSave)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setFocusPolicy(Qt.StrongFocus)
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.title_edit = QLineEdit(self.widget_3)
        self.title_edit.setObjectName(u"title_edit")

        self.horizontalLayout_3.addWidget(self.title_edit)

        self.gridLayout.addWidget(self.widget_3, 1, 2, 1, 1)

        self.label_7 = QLabel(RegeltestSave)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 3)

        self.label_13 = QLabel(RegeltestSave)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 17, 0, 1, 1)

        self.widget_8 = QWidget(RegeltestSave)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.spinBox_ppt_time = QSpinBox(self.widget_8)
        self.spinBox_ppt_time.setObjectName(u"spinBox_ppt_time")
        self.spinBox_ppt_time.setMinimum(1)
        self.spinBox_ppt_time.setMaximum(280)
        self.spinBox_ppt_time.setValue(60)

        self.horizontalLayout_10.addWidget(self.spinBox_ppt_time)

        self.gridLayout.addWidget(self.widget_8, 12, 2, 1, 1)

        self.label = QLabel(RegeltestSave)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_11 = QLabel(RegeltestSave)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 11, 3, 1, 1)

        self.line_2 = QFrame(RegeltestSave)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 8, 0, 1, 6)

        self.scrollArea = QScrollArea(RegeltestSave)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.question_scrollable = QWidget()
        self.question_scrollable.setObjectName(u"question_scrollable")
        self.question_scrollable.setGeometry(QRect(0, 0, 740, 69))
        self.scrollArea.setWidget(self.question_scrollable)

        self.gridLayout.addWidget(self.scrollArea, 23, 0, 1, 6)

        self.widget_2 = QWidget(RegeltestSave)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pdf_edit = QLineEdit(self.widget_2)
        self.pdf_edit.setObjectName(u"pdf_edit")

        self.horizontalLayout_2.addWidget(self.pdf_edit)

        self.pdf_edit_button = QPushButton(self.widget_2)
        self.pdf_edit_button.setObjectName(u"pdf_edit_button")

        self.horizontalLayout_2.addWidget(self.pdf_edit_button)

        self.gridLayout.addWidget(self.widget_2, 6, 2, 1, 1)

        self.widget_5 = QWidget(RegeltestSave)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.fontsize_spinBox = QSpinBox(self.widget_5)
        self.fontsize_spinBox.setObjectName(u"fontsize_spinBox")
        self.fontsize_spinBox.setMinimum(9)
        self.fontsize_spinBox.setMaximum(15)
        self.fontsize_spinBox.setValue(11)

        self.horizontalLayout_6.addWidget(self.fontsize_spinBox)

        self.gridLayout.addWidget(self.widget_5, 6, 5, 1, 1)

        self.line_3 = QFrame(RegeltestSave)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_3, 3, 0, 1, 6)

        self.buttonBox = QDialogButtonBox(RegeltestSave)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 24, 0, 1, 6)

        self.label_12 = QLabel(RegeltestSave)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 12, 0, 1, 1)

        self.label_6 = QLabel(RegeltestSave)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 11, 0, 1, 1)

        self.label_5 = QLabel(RegeltestSave)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 15, 0, 1, 1)

        self.label_9 = QLabel(RegeltestSave)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 10, 0, 1, 6)

        self.line_4 = QFrame(RegeltestSave)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_4, 16, 0, 1, 6)

        self.widget_7 = QWidget(RegeltestSave)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.spinBox_ppt_groups = QSpinBox(self.widget_7)
        self.spinBox_ppt_groups.setObjectName(u"spinBox_ppt_groups")
        self.spinBox_ppt_groups.setMinimum(1)
        self.spinBox_ppt_groups.setMaximum(2)
        self.spinBox_ppt_groups.setValue(1)

        self.horizontalLayout_9.addWidget(self.spinBox_ppt_groups)

        self.gridLayout.addWidget(self.widget_7, 11, 5, 1, 1)

        self.label_8 = QLabel(RegeltestSave)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 6)

        self.regeltest_archive_checkBox = QCheckBox(RegeltestSave)
        self.regeltest_archive_checkBox.setObjectName(u"regeltest_archive_checkBox")
        self.regeltest_archive_checkBox.setChecked(True)

        self.gridLayout.addWidget(self.regeltest_archive_checkBox, 2, 0, 1, 6)

        QWidget.setTabOrder(self.title_edit, self.icon_path_edit)
        QWidget.setTabOrder(self.icon_path_edit, self.icon_edit_button)
        QWidget.setTabOrder(self.icon_edit_button, self.pdf_edit)
        QWidget.setTabOrder(self.pdf_edit, self.pdf_edit_button)
        QWidget.setTabOrder(self.pdf_edit_button, self.widget_3)

        self.retranslateUi(RegeltestSave)
        self.buttonBox.accepted.connect(RegeltestSave.accept)
        self.buttonBox.rejected.connect(RegeltestSave.reject)
        RegeltestSave.windowTitleChanged.connect(self.title_edit.setFocus)

        QMetaObject.connectSlotsByName(RegeltestSave)
    # setupUi

    def retranslateUi(self, RegeltestSave):
        RegeltestSave.setWindowTitle(QCoreApplication.translate("RegeltestSave", u"Save Regeltest", None))
        self.icon_edit_button.setText(QCoreApplication.translate("RegeltestSave", u"Ausw\u00e4hlen", None))
        self.ppt_edit_button.setText(QCoreApplication.translate("RegeltestSave", u"Ausw\u00e4hlen", None))
        self.csv_edit_button.setText(QCoreApplication.translate("RegeltestSave", u"Ausw\u00e4hlen", None))
        self.activate_mc_button.setText(
            QCoreApplication.translate("RegeltestSave", u"Alle Multiple-Choice aktivieren", None))
        self.deactivate_mc_button.setText(
            QCoreApplication.translate("RegeltestSave", u"Alle Multiple-Choice deaktivieren", None))
        self.label_4.setText(QCoreApplication.translate("RegeltestSave", u"Schriftgr\u00f6\u00dfe", None))
        self.label_2.setText(QCoreApplication.translate("RegeltestSave", u"Iconpfad", None))
        self.label_10.setText(QCoreApplication.translate("RegeltestSave", u"Advanced: CSV", None))
        self.label_3.setText(QCoreApplication.translate("RegeltestSave", u"Speicherort", None))
        self.label_7.setText(QCoreApplication.translate("RegeltestSave", u"Allgemeines", None))
        self.label_13.setText(QCoreApplication.translate("RegeltestSave", u"Fragen-Setup", None))
        self.spinBox_ppt_time.setSuffix(QCoreApplication.translate("RegeltestSave", u" Sekunden", None))
        self.label.setText(QCoreApplication.translate("RegeltestSave", u"Titel", None))
        self.label_11.setText(QCoreApplication.translate("RegeltestSave", u"Gruppen", None))
        self.pdf_edit_button.setText(QCoreApplication.translate("RegeltestSave", u"Ausw\u00e4hlen", None))
        self.fontsize_spinBox.setSuffix(QCoreApplication.translate("RegeltestSave", u"pt", None))
        self.label_12.setText(QCoreApplication.translate("RegeltestSave", u"Zeit pro Frage", None))
        self.label_6.setText(QCoreApplication.translate("RegeltestSave", u"Speicherort", None))
        self.label_5.setText(QCoreApplication.translate("RegeltestSave", u"Speicherort", None))
        self.label_9.setText(QCoreApplication.translate("RegeltestSave", u"Powerpoint Regeltest", None))
        self.label_8.setText(QCoreApplication.translate("RegeltestSave", u"PDF Regeltest", None))
        self.regeltest_archive_checkBox.setText(
            QCoreApplication.translate("RegeltestSave", u"Regeltest zus\u00e4tzlich im Archiv speichern?", None))
    # retranslateUi

