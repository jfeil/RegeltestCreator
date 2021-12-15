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
    QDialogButtonBox, QLabel, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

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
        self.verticalSpacer = QSpacerItem(20, 257, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.statistics = QLabel(RegeltestSetup)
        self.statistics.setObjectName(u"statistics")

        self.verticalLayout.addWidget(self.statistics)

        self.checkbox_rulegroups = QCheckBox(RegeltestSetup)
        self.checkbox_rulegroups.setObjectName(u"checkbox_rulegroups")

        self.verticalLayout.addWidget(self.checkbox_rulegroups)

        self.checkbox_textmchoice = QCheckBox(RegeltestSetup)
        self.checkbox_textmchoice.setObjectName(u"checkbox_textmchoice")

        self.verticalLayout.addWidget(self.checkbox_textmchoice)

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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("RegeltestSetup", u"Tab 2", None))
        self.statistics.setText("")
        self.checkbox_rulegroups.setText(QCoreApplication.translate("RegeltestSetup", u"Shuffle rulegroups", None))
        self.checkbox_textmchoice.setText(QCoreApplication.translate("RegeltestSetup", u"Mix multiple choice and text questions within rulegroup", None))
    # retranslateUi

