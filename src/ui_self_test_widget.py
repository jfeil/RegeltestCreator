# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'self_test_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            QSize, Qt)
from PySide6.QtWidgets import (QFrame, QGridLayout, QLabel,
                               QProgressBar, QPushButton, QScrollArea, QSizePolicy,
                               QStackedWidget, QTextEdit, QToolButton, QVBoxLayout,
                               QWidget)

from src.custom_ui import CollapseButton


class Ui_SelfTestWidget(object):
    def setupUi(self, SelfTestWidget):
        if not SelfTestWidget.objectName():
            SelfTestWidget.setObjectName(u"SelfTestWidget")
        SelfTestWidget.resize(722, 421)
        self.verticalLayout = QVBoxLayout(SelfTestWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stackedWidget = QStackedWidget(SelfTestWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.test_page = QWidget()
        self.test_page.setObjectName(u"test_page")
        self.gridLayout = QGridLayout(self.test_page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.next_button = QPushButton(self.test_page)
        self.next_button.setObjectName(u"next_button")

        self.gridLayout.addWidget(self.next_button, 7, 3, 1, 1)

        self.switch_eval_button = QPushButton(self.test_page)
        self.switch_eval_button.setObjectName(u"switch_eval_button")

        self.gridLayout.addWidget(self.switch_eval_button, 7, 1, 1, 2)

        self.user_answer_test = QTextEdit(self.test_page)
        self.user_answer_test.setObjectName(u"user_answer_test")

        self.gridLayout.addWidget(self.user_answer_test, 4, 0, 1, 4)

        self.statistics_button = CollapseButton(self.test_page)
        self.statistics_button.setObjectName(u"statistics_button")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statistics_button.sizePolicy().hasHeightForWidth())
        self.statistics_button.setSizePolicy(sizePolicy)
        self.statistics_button.setStyleSheet(u"")
        self.statistics_button.setIconSize(QSize(8, 8))
        self.statistics_button.setCheckable(True)
        self.statistics_button.setPopupMode(QToolButton.DelayedPopup)
        self.statistics_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.statistics_button.setAutoRaise(True)
        self.statistics_button.setArrowType(Qt.RightArrow)

        self.gridLayout.addWidget(self.statistics_button, 2, 0, 1, 4)

        self.progressbar_widget = QWidget(self.test_page)
        self.progressbar_widget.setObjectName(u"progressbar_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progressbar_widget.sizePolicy().hasHeightForWidth())
        self.progressbar_widget.setSizePolicy(sizePolicy1)
        self.gridLayout_3 = QGridLayout(self.progressbar_widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.progressbar_bar = QProgressBar(self.progressbar_widget)
        self.progressbar_bar.setObjectName(u"progressbar_bar")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.progressbar_bar.sizePolicy().hasHeightForWidth())
        self.progressbar_bar.setSizePolicy(sizePolicy2)
        self.progressbar_bar.setMaximumSize(QSize(16777215, 1))
        self.progressbar_bar.setStyleSheet(u"QProgressBar::chunk {\n"
                                           "                                                        background-color: #06b025;\n"
                                           "                                                        }\n"
                                           "\n"
                                           "                                                        QProgressBar {\n"
                                           "                                                        text-align: right;\n"
                                           "                                                        max-height: 1px;\n"
                                           "                                                        }\n"
                                           "                                                    ")
        self.progressbar_bar.setMaximum(255)
        self.progressbar_bar.setValue(30)
        self.progressbar_bar.setTextVisible(False)
        self.progressbar_bar.setOrientation(Qt.Horizontal)
        self.progressbar_bar.setInvertedAppearance(False)

        self.gridLayout_3.addWidget(self.progressbar_bar, 0, 0, 1, 1)

        self.progressbar_label = QLabel(self.progressbar_widget)
        self.progressbar_label.setObjectName(u"progressbar_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.progressbar_label.sizePolicy().hasHeightForWidth())
        self.progressbar_label.setSizePolicy(sizePolicy3)

        self.gridLayout_3.addWidget(self.progressbar_label, 0, 1, 1, 1)

        self.gridLayout.addWidget(self.progressbar_widget, 6, 0, 1, 4)

        self.previous_button = QPushButton(self.test_page)
        self.previous_button.setObjectName(u"previous_button")

        self.gridLayout.addWidget(self.previous_button, 7, 0, 1, 1)

        self.statistics_frame = QFrame(self.test_page)
        self.statistics_frame.setObjectName(u"statistics_frame")
        self.statistics_frame.setFrameShape(QFrame.StyledPanel)
        self.statistics_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.statistics_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.statistics_label = QLabel(self.statistics_frame)
        self.statistics_label.setObjectName(u"statistics_label")

        self.verticalLayout_3.addWidget(self.statistics_label)

        self.gridLayout.addWidget(self.statistics_frame, 3, 0, 1, 4)

        self.widget = QWidget(self.test_page)
        self.widget.setObjectName(u"widget")
        self.gridLayout_4 = QGridLayout(self.widget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy4)
        self.verticalLayout_4 = QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.time_progressbar = QProgressBar(self.widget_2)
        self.time_progressbar.setObjectName(u"time_progressbar")
        self.time_progressbar.setStyleSheet(u"QProgressBar::chunk {\n"
                                            "background-color: #06b025;\n"
                                            "                                                        }\n"
                                            "\n"
                                            "                                                        QProgressBar {\n"
                                            "                                                        max-width: 10px;\n"
                                            "                                                        }\n"
                                            "                                                    ")
        self.time_progressbar.setValue(24)
        self.time_progressbar.setAlignment(Qt.AlignCenter)
        self.time_progressbar.setTextVisible(False)
        self.time_progressbar.setOrientation(Qt.Vertical)
        self.time_progressbar.setInvertedAppearance(False)

        self.verticalLayout_4.addWidget(self.time_progressbar, 0, Qt.AlignHCenter)

        self.time_label = QLabel(self.widget_2)
        self.time_label.setObjectName(u"time_label")
        self.time_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.time_label, 0, Qt.AlignHCenter)

        self.gridLayout_4.addWidget(self.widget_2, 0, 1, 2, 1)

        self.scrollArea = QScrollArea(self.widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 636, 274))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.question_label_test = QLabel(self.scrollAreaWidgetContents)
        self.question_label_test.setObjectName(u"question_label_test")
        self.question_label_test.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.question_label_test.setWordWrap(True)
        self.question_label_test.setMargin(0)

        self.verticalLayout_5.addWidget(self.question_label_test)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_4.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.widget, 0, 0, 1, 4)

        self.stackedWidget.addWidget(self.test_page)
        self.eval_widget = QWidget()
        self.eval_widget.setObjectName(u"eval_widget")
        self.gridLayout_2 = QGridLayout(self.eval_widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.eval_button_widget = QWidget(self.eval_widget)
        self.eval_button_widget.setObjectName(u"eval_button_widget")
        self.verticalLayout_2 = QVBoxLayout(self.eval_button_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.incorrect_button = QPushButton(self.eval_button_widget)
        self.incorrect_button.setObjectName(u"incorrect_button")

        self.verticalLayout_2.addWidget(self.incorrect_button)

        self.correct_button = QPushButton(self.eval_button_widget)
        self.correct_button.setObjectName(u"correct_button")

        self.verticalLayout_2.addWidget(self.correct_button)


        self.gridLayout_2.addWidget(self.eval_button_widget, 2, 3, 1, 1)

        self.correct_answer_eval = QTextEdit(self.eval_widget)
        self.correct_answer_eval.setObjectName(u"correct_answer_eval")
        self.correct_answer_eval.setTextInteractionFlags(Qt.NoTextInteraction)

        self.gridLayout_2.addWidget(self.correct_answer_eval, 2, 2, 1, 1)

        self.user_answer_eval = QTextEdit(self.eval_widget)
        self.user_answer_eval.setObjectName(u"user_answer_eval")
        self.user_answer_eval.setTextInteractionFlags(Qt.NoTextInteraction)

        self.gridLayout_2.addWidget(self.user_answer_eval, 2, 0, 1, 2)

        self.question_label_eval = QLabel(self.eval_widget)
        self.question_label_eval.setObjectName(u"question_label_eval")
        self.question_label_eval.setWordWrap(True)
        self.question_label_eval.setMargin(20)

        self.gridLayout_2.addWidget(self.question_label_eval, 0, 0, 1, 4)

        self.stackedWidget.addWidget(self.eval_widget)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(SelfTestWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SelfTestWidget)
    # setupUi

    def retranslateUi(self, SelfTestWidget):
        SelfTestWidget.setWindowTitle(QCoreApplication.translate("SelfTestWidget", u"Form", None))
        self.next_button.setText(QCoreApplication.translate("SelfTestWidget", u"N\u00e4chste Frage", None))
        self.switch_eval_button.setText(QCoreApplication.translate("SelfTestWidget", u"Evaluieren", None))
        self.user_answer_test.setHtml(QCoreApplication.translate("SelfTestWidget",
                                                                 u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                                 "p, li { white-space: pre-wrap; }\n"
                                                                 "</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                                            </p>\n"
                                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                                             </p>\n"
                                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Strafsto\u00df,                                            Linie geh\u00f6rt zum Strafraum                                         </p></body></html>",
                                                                 None))
        self.statistics_button.setText(QCoreApplication.translate("SelfTestWidget", u"Statistiken", None))
        self.progressbar_bar.setFormat(QCoreApplication.translate("SelfTestWidget", u"%v/%m", None))
        self.progressbar_label.setText(QCoreApplication.translate("SelfTestWidget", u"20 / 255", None))
        self.previous_button.setText(QCoreApplication.translate("SelfTestWidget", u"Vorherige Frage", None))
        self.statistics_label.setText(QCoreApplication.translate("SelfTestWidget", u"Das ist\n"
                                                                                   "                                                        ein\n"
                                                                                   "                                                        Test\n"
                                                                                   "                                                    ",
                                                                 None))
        self.time_label.setText(QCoreApplication.translate("SelfTestWidget", u"300s", None))
        self.question_label_test.setText(QCoreApplication.translate("SelfTestWidget",
                                                                    u"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus rhoncus massa quis turpis congue interdum. Suspendisse interdum ipsum sit amet enim cursus vehicula. Praesent non mauris augue. Cras est nisl, sagittis in tempor ac, laoreet ac ex. Etiam dolor sapien, ullamcorper a pellentesque vitae, ultrices nec felis. Maecenas a justo a neque vehicula posuere a vitae urna. Aliquam maximus lectus ut sapien suscipit sagittis. Cras mauris lectus, molestie ac auctor quis, hendrerit quis nisi. Pellentesque porta justo nisi. Cras elementum turpis et convallis ultrices. Proin ut tristique tellus, ut faucibus est. Etiam convallis in ipsum ac efficitur. Curabitur ultricies metus at lorem pretium, at lobortis velit aliquet. Duis pretium nec est sed luctus. Maecenas viverra felis eu ex vestibulum gravida.\n"
                                                                    "\n"
                                                                    "Morbi id dui dui. Pellentesque sit amet ante ut ligula euismod sollicitudin. Mauris lobortis consequat accumsan. Praesent rutrum consectetur diam, non viverra urna volutpat sit amet. Etiam sit amet elit odio."
                                                                    " Aliquam erat volutpat. Integer semper justo nec arcu consequat commodo. In egestas egestas orci at gravida. Integer iaculis malesuada posuere. Aliquam turpis nunc, eleifend sit amet sodales ac, luctus nec metus.\n"
                                                                    "\n"
                                                                    "Phasellus ultricies congue rutrum. In egestas odio velit. Integer eget mi a dui egestas tempus vitae eget mauris. Etiam lacinia, tellus nec eleifend feugiat, nisl orci facilisis urna, at vehicula felis sapien sit amet turpis. Vestibulum dapibus, augue facilisis pharetra gravida, ante metus consequat tortor, sollicitudin ultrices ipsum. ",
                                                                    None))
        self.incorrect_button.setText(QCoreApplication.translate("SelfTestWidget", u"Falsch", None))
        self.correct_button.setText(QCoreApplication.translate("SelfTestWidget", u"Richtig", None))
        self.correct_answer_eval.setHtml(QCoreApplication.translate("SelfTestWidget",
                                                                    u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                                    "p, li { white-space: pre-wrap; }\n"
                                                                    "</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                                            </p>\n"
                                                                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                                             </p>\n"
                                                                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">In dieser                                            Situation ist es erforderlich auf Strafsto\u00df zu entschieden. Die jeweiligen                                            Begrenzungslinien "
                                                                    "geh\u00f6ren zum Raum, den sie umschlie\u00dfen (Der Strafraum wird                                            von der Strafraumlinie umschlossen).                                         </p></body></html>",
                                                                    None))
        self.user_answer_eval.setHtml(QCoreApplication.translate("SelfTestWidget",
                                                                 u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                                 "p, li { white-space: pre-wrap; }\n"
                                                                 "</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                                            </p>\n"
                                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                                             </p>\n"
                                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Strafsto\u00df,                                            Linie geh\u00f6rt zum Strafraum                                         </p></body></html>",
                                                                 None))
        self.question_label_eval.setText(QCoreApplication.translate("SelfTestWidget",
                                                                    u"Bei einem Angriff foult der Verteidiger den St\u00fcrmer direkt auf der\n"
                                                                    "                                            Strafraumlinie: Wie hat der Schiedsrichter zu entscheiden?\n"
                                                                    "                                        ", None))
    # retranslateUi

