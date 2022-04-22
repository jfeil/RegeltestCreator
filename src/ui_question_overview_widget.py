# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'question_overview_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QListView, QListWidget, QPushButton,
                               QSizePolicy, QTabWidget, QTreeWidget, QTreeWidgetItem,
                               QVBoxLayout, QWidget)


class Ui_QuestionOverviewWidget(object):
    def setupUi(self, QuestionOverviewWidget):
        if not QuestionOverviewWidget.objectName():
            QuestionOverviewWidget.setObjectName(u"QuestionOverviewWidget")
        QuestionOverviewWidget.resize(529, 291)
        self.verticalLayout = QVBoxLayout(QuestionOverviewWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.filterWidget = QWidget(QuestionOverviewWidget)
        self.filterWidget.setObjectName(u"filterWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterWidget.sizePolicy().hasHeightForWidth())
        self.filterWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.filterWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.filter_list = QListWidget(self.filterWidget)
        self.filter_list.setObjectName(u"filter_list")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.filter_list.sizePolicy().hasHeightForWidth())
        self.filter_list.setSizePolicy(sizePolicy1)
        self.filter_list.setFrameShape(QFrame.StyledPanel)
        self.filter_list.setFrameShadow(QFrame.Sunken)
        self.filter_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.filter_list.setMovement(QListView.Free)
        self.filter_list.setFlow(QListView.LeftToRight)
        self.filter_list.setLayoutMode(QListView.SinglePass)
        self.filter_list.setSpacing(2)
        self.filter_list.setViewMode(QListView.IconMode)
        self.filter_list.setUniformItemSizes(False)
        self.filter_list.setWordWrap(False)

        self.horizontalLayout_2.addWidget(self.filter_list)

        self.widget_3 = QWidget(self.filterWidget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_4 = QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.add_filter = QPushButton(self.widget_3)
        self.add_filter.setObjectName(u"add_filter")

        self.verticalLayout_4.addWidget(self.add_filter)

        self.horizontalLayout_2.addWidget(self.widget_3)

        self.verticalLayout.addWidget(self.filterWidget)

        self.tabWidget = QTabWidget(QuestionOverviewWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy2)
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

        self.retranslateUi(QuestionOverviewWidget)

        self.filter_list.setCurrentRow(-1)
        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(QuestionOverviewWidget)

    # setupUi

    def retranslateUi(self, QuestionOverviewWidget):
        QuestionOverviewWidget.setWindowTitle(QCoreApplication.translate("QuestionOverviewWidget", u"Form", None))
        self.add_filter.setText(QCoreApplication.translate("QuestionOverviewWidget", u"Neuer Filter", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(4,
                                   QCoreApplication.translate("QuestionOverviewWidget", u"\u00c4nderungsdatum", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("QuestionOverviewWidget", u"Antwort", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("QuestionOverviewWidget", u"Multiple choice?", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("QuestionOverviewWidget", u"Frage", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("QuestionOverviewWidget", u"Regelnummer", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("QuestionOverviewWidget", u"2020-06-22", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("QuestionOverviewWidget",
                                                                  u"Ja. Alle Hilfsflaggen m\u00fcssen 1m au\u00dferhalb der Seitenlinie stehen.",
                                                                  None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("QuestionOverviewWidget", u"Ja", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("QuestionOverviewWidget",
                                                                  u"Die Hilfsflaggen werden vom Platzwart auf die Seitenlinie gesteckt. Hat der SR Grund zur Beanstandung?",
                                                                  None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("QuestionOverviewWidget", u"01", None));
        # if QT_CONFIG(tooltip)
        ___qtreewidgetitem1.setToolTip(1, QCoreApplication.translate("QuestionOverviewWidget",
                                                                     u"Die Hilfsflaggen werden vom Platzwart auf die Seitenlinie gesteckt. Hat der SR Grund zur Beanstandung?",
                                                                     None));
        # endif // QT_CONFIG(tooltip)
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Test),
                                  QCoreApplication.translate("QuestionOverviewWidget", u"01 Das Spielfeld", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  QCoreApplication.translate("QuestionOverviewWidget", u"02 Der Ball", None))
    # retranslateUi
