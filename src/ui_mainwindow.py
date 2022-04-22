# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            Qt)
from PySide6.QtGui import (QAction)
from PySide6.QtWidgets import (QDockWidget, QMenu,
                               QMenuBar, QStackedWidget, QToolBar,
                               QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(881, 634)
        self.actionNeue_Kategorie_erstellen = QAction(MainWindow)
        self.actionNeue_Kategorie_erstellen.setObjectName(u"actionNeue_Kategorie_erstellen")
        self.actionAnsicht_zur_cksetzen = QAction(MainWindow)
        self.actionAnsicht_zur_cksetzen.setObjectName(u"actionAnsicht_zur_cksetzen")
        self.actionRegeltest_l_schen = QAction(MainWindow)
        self.actionRegeltest_l_schen.setObjectName(u"actionRegeltest_l_schen")
        self.actionRegeldatensatz_einladen = QAction(MainWindow)
        self.actionRegeldatensatz_einladen.setObjectName(u"actionRegeldatensatz_einladen")
        self.actionRegeldatensatz_exportieren = QAction(MainWindow)
        self.actionRegeldatensatz_exportieren.setObjectName(u"actionRegeldatensatz_exportieren")
        self.actionRegeltest_einrichten = QAction(MainWindow)
        self.actionRegeltest_einrichten.setObjectName(u"actionRegeltest_einrichten")
        self.actionAuf_Updates_pr_fen = QAction(MainWindow)
        self.actionAuf_Updates_pr_fen.setObjectName(u"actionAuf_Updates_pr_fen")
        self.action_ber = QAction(MainWindow)
        self.action_ber.setObjectName(u"action_ber")
        self.actionSelftest = QAction(MainWindow)
        self.actionSelftest.setObjectName(u"actionSelftest")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")

        self.verticalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 881, 22))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        self.menuAnsicht = QMenu(self.menubar)
        self.menuAnsicht.setObjectName(u"menuAnsicht")
        self.menuBearbeiten = QMenu(self.menubar)
        self.menuBearbeiten.setObjectName(u"menuBearbeiten")
        self.menu_ber = QMenu(self.menubar)
        self.menu_ber.setObjectName(u"menu_ber")
        MainWindow.setMenuBar(self.menubar)
        self.main_window_dockwidget = QDockWidget(MainWindow)
        self.main_window_dockwidget.setObjectName(u"main_window_dockwidget")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stacked_widget_dock = QStackedWidget(self.dockWidgetContents)
        self.stacked_widget_dock.setObjectName(u"stacked_widget_dock")

        self.verticalLayout_3.addWidget(self.stacked_widget_dock)

        self.main_window_dockwidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.main_window_dockwidget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuBearbeiten.menuAction())
        self.menubar.addAction(self.menuAnsicht.menuAction())
        self.menubar.addAction(self.menu_ber.menuAction())
        self.menuDatei.addAction(self.actionRegeldatensatz_einladen)
        self.menuDatei.addAction(self.actionRegeldatensatz_exportieren)
        self.menuAnsicht.addAction(self.actionAnsicht_zur_cksetzen)
        self.menuBearbeiten.addAction(self.actionNeue_Kategorie_erstellen)
        self.menuBearbeiten.addAction(self.actionRegeltest_einrichten)
        self.menuBearbeiten.addAction(self.actionRegeltest_l_schen)
        self.menu_ber.addAction(self.actionAuf_Updates_pr_fen)
        self.menu_ber.addAction(self.action_ber)
        self.toolBar.addAction(self.actionSelftest)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNeue_Kategorie_erstellen.setText(
            QCoreApplication.translate("MainWindow", u"Neue Kategorie erstellen", None))
        self.actionAnsicht_zur_cksetzen.setText(
            QCoreApplication.translate("MainWindow", u"Ansicht zur\u00fccksetzen", None))
        self.actionRegeltest_l_schen.setText(QCoreApplication.translate("MainWindow", u"Regeltest l\u00f6schen", None))
        self.actionRegeldatensatz_einladen.setText(
            QCoreApplication.translate("MainWindow", u"Regeldatensatz einladen", None))
        self.actionRegeldatensatz_exportieren.setText(
            QCoreApplication.translate("MainWindow", u"Regeldatensatz exportieren", None))
        self.actionRegeltest_einrichten.setText(QCoreApplication.translate("MainWindow", u"Regeltest einrichten", None))
        self.actionAuf_Updates_pr_fen.setText(
            QCoreApplication.translate("MainWindow", u"Auf Updates pr\u00fcfen", None))
        self.action_ber.setText(QCoreApplication.translate("MainWindow", u"\u00dcber", None))
        self.actionSelftest.setText(QCoreApplication.translate("MainWindow", u"Selbsttest", None))
        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuAnsicht.setTitle(QCoreApplication.translate("MainWindow", u"Ansicht", None))
        self.menuBearbeiten.setTitle(QCoreApplication.translate("MainWindow", u"Bearbeiten", None))
        self.menu_ber.setTitle(QCoreApplication.translate("MainWindow", u"Hilfe", None))
        self.main_window_dockwidget.setWindowTitle("")
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

