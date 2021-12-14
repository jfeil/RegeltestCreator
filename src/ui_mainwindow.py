# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            Qt)
from PySide6.QtGui import (QAction)
from PySide6.QtWidgets import (QDockWidget, QLabel,
                               QMenu, QMenuBar,
                               QPushButton, QStatusBar, QTabWidget,
                               QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

from .regeltestcreator import RegeltestCreator


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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.Test = QWidget()
        self.Test.setObjectName(u"Test")
        self.verticalLayout_2 = QVBoxLayout(self.Test)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.treeWidget = QTreeWidget(self.Test)
        QTreeWidgetItem(self.treeWidget)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout_2.addWidget(self.treeWidget)

        self.tabWidget.addTab(self.Test, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

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
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.regeltest_creator = QDockWidget(MainWindow)
        self.regeltest_creator.setObjectName(u"regeltest_creator")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.regeltest_list = RegeltestCreator(self.dockWidgetContents)
        self.regeltest_list.setObjectName(u"regeltest_list")

        self.verticalLayout_3.addWidget(self.regeltest_list)

        self.regeltest_stats = QLabel(self.dockWidgetContents)
        self.regeltest_stats.setObjectName(u"regeltest_stats")

        self.verticalLayout_3.addWidget(self.regeltest_stats)

        self.create_regeltest = QPushButton(self.dockWidgetContents)
        self.create_regeltest.setObjectName(u"create_regeltest")

        self.verticalLayout_3.addWidget(self.create_regeltest)

        self.regeltest_creator.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.regeltest_creator)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuBearbeiten.menuAction())
        self.menubar.addAction(self.menuAnsicht.menuAction())
        self.menuDatei.addAction(self.actionRegeldatensatz_einladen)
        self.menuDatei.addAction(self.actionRegeldatensatz_exportieren)
        self.menuAnsicht.addAction(self.actionAnsicht_zur_cksetzen)
        self.menuBearbeiten.addAction(self.actionNeue_Kategorie_erstellen)
        self.menuBearbeiten.addAction(self.actionRegeltest_einrichten)
        self.menuBearbeiten.addAction(self.actionRegeltest_l_schen)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)

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
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"\u00c4nderungsdatum", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"Antwort", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Multiple choice?", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Frage", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Regelnummer", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("MainWindow", u"2020-06-22", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("MainWindow",
                                                                  u"Ja. Alle Hilfsflaggen m\u00fcssen 1m au\u00dferhalb der Seitenlinie stehen.",
                                                                  None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("MainWindow", u"Ja", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("MainWindow",
                                                                  u"Die Hilfsflaggen werden vom Platzwart auf die Seitenlinie gesteckt. Hat der SR Grund zur Beanstandung?",
                                                                  None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"01", None));
        # if QT_CONFIG(tooltip)
        ___qtreewidgetitem1.setToolTip(1, QCoreApplication.translate("MainWindow",
                                                                     u"Die Hilfsflaggen werden vom Platzwart auf die Seitenlinie gesteckt. Hat der SR Grund zur Beanstandung?",
                                                                     None));
        # endif // QT_CONFIG(tooltip)
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Test),
                                  QCoreApplication.translate("MainWindow", u"01 Das Spielfeld", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  QCoreApplication.translate("MainWindow", u"02 Der Ball", None))
        self.menuDatei.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuAnsicht.setTitle(QCoreApplication.translate("MainWindow", u"Ansicht", None))
        self.menuBearbeiten.setTitle(QCoreApplication.translate("MainWindow", u"Bearbeiten", None))
        self.regeltest_creator.setWindowTitle(QCoreApplication.translate("MainWindow", u"Regeltest-Creator", None))
        self.regeltest_stats.setText(
            QCoreApplication.translate("MainWindow", u"0 Fragen ausgew\u00e4hlt (0 Punkte)", None))
        self.create_regeltest.setText(QCoreApplication.translate("MainWindow", u"Regeltest erstellen", None))
    # retranslateUi
