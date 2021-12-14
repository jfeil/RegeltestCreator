# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'regeltest_setup.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_RegeltestSetup(object):
    def setupUi(self, RegeltestSetup):
        if not RegeltestSetup.objectName():
            RegeltestSetup.setObjectName(u"RegeltestSetup")
        RegeltestSetup.resize(400, 525)
        self.verticalLayout = QVBoxLayout(RegeltestSetup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(RegeltestSetup)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_4 = QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget = QWidget(self.tab_2)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox = QSpinBox(self.widget_2)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout.addWidget(self.spinBox)

        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_2 = QSpinBox(self.widget_2)
        self.spinBox_2.setObjectName(u"spinBox_2")

        self.horizontalLayout.addWidget(self.spinBox_2)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)


        self.verticalLayout_4.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 257, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.checkBox = QCheckBox(RegeltestSetup)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(RegeltestSetup)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.verticalLayout.addWidget(self.checkBox_2)

        self.widget_3 = QWidget(RegeltestSetup)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_3 = QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.verticalLayout.addWidget(self.widget_3)

        self.buttonBox = QDialogButtonBox(RegeltestSetup)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(RegeltestSetup)
        self.buttonBox.accepted.connect(RegeltestSetup.accept)
        self.buttonBox.rejected.connect(RegeltestSetup.reject)

        QMetaObject.connectSlotsByName(RegeltestSetup)
    # setupUi

    def retranslateUi(self, RegeltestSetup):
        RegeltestSetup.setWindowTitle(QCoreApplication.translate("RegeltestSetup", u"Setup Regeltest", None))
        self.label.setText(QCoreApplication.translate("RegeltestSetup", u"01 - Das Spielfeld", None))
        self.label_2.setText(QCoreApplication.translate("RegeltestSetup", u"Textquestion", None))
        self.label_3.setText(QCoreApplication.translate("RegeltestSetup", u"Multiple choice", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("RegeltestSetup", u"Tab 2", None))
        self.checkBox.setText(QCoreApplication.translate("RegeltestSetup", u"Separate rulegroups", None))
        self.checkBox_2.setText(QCoreApplication.translate("RegeltestSetup", u"Separate textquestions and multiple choice questions", None))
    # retranslateUi

