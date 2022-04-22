# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'self_test_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtWidgets import (QGridLayout, QLabel, QPushButton,
                               QStackedWidget, QTextEdit, QVBoxLayout,
                               QWidget)


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

        self.gridLayout.addWidget(self.next_button, 2, 3, 1, 1)

        self.question_label_test = QLabel(self.test_page)
        self.question_label_test.setObjectName(u"question_label_test")
        self.question_label_test.setWordWrap(True)
        self.question_label_test.setMargin(20)

        self.gridLayout.addWidget(self.question_label_test, 0, 0, 1, 4)

        self.switch_eval_button = QPushButton(self.test_page)
        self.switch_eval_button.setObjectName(u"switch_eval_button")

        self.gridLayout.addWidget(self.switch_eval_button, 2, 1, 1, 2)

        self.previous_button = QPushButton(self.test_page)
        self.previous_button.setObjectName(u"previous_button")

        self.gridLayout.addWidget(self.previous_button, 2, 0, 1, 1)

        self.user_answer_test = QTextEdit(self.test_page)
        self.user_answer_test.setObjectName(u"user_answer_test")

        self.gridLayout.addWidget(self.user_answer_test, 1, 0, 1, 4)

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
        self.question_label_test.setText(QCoreApplication.translate("SelfTestWidget",
                                                                    u"Ein angreifender Spieler wird von einem Verteidiger genau auf der Strafraumlinie durch Beinstellen zu Fall gebracht.  Welche Entscheidung muss der SR treffen?",
                                                                    None))
        self.switch_eval_button.setText(QCoreApplication.translate("SelfTestWidget", u"Evaluieren", None))
        self.previous_button.setText(QCoreApplication.translate("SelfTestWidget", u"Vorherige Frage", None))
        self.user_answer_test.setHtml(QCoreApplication.translate("SelfTestWidget",
                                                                 u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                                 "p, li { white-space: pre-wrap; }\n"
                                                                 "</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Strafsto\u00df, Linie geh\u00f6rt zum Strafraum</p></body></html>",
                                                                 None))
        self.incorrect_button.setText(QCoreApplication.translate("SelfTestWidget", u"Falsch", None))
        self.correct_button.setText(QCoreApplication.translate("SelfTestWidget", u"Richtig", None))
        self.correct_answer_eval.setHtml(QCoreApplication.translate("SelfTestWidget",
                                                                    u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                                    "p, li { white-space: pre-wrap; }\n"
                                                                    "</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Der SR muss auf Strafsto\u00df entscheiden. Die Begrenzungslinien geh\u00f6ren zu dem Raum, den sie umschlie\u00dfen. (Hier: Strafraumlinie zum Strafraum)</p></body></html>",
                                                                    None))
        self.user_answer_eval.setHtml(QCoreApplication.translate("SelfTestWidget",
                                                                 u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                                 "p, li { white-space: pre-wrap; }\n"
                                                                 "</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Strafsto\u00df, Linie geh\u00f6rt zum Strafraum</p></body></html>",
                                                                 None))
        self.question_label_eval.setText(QCoreApplication.translate("SelfTestWidget",
                                                                    u"Ein angreifender Spieler wird von einem Verteidiger genau auf der Strafraumlinie durch Beinstellen zu Fall gebracht.  Welche Entscheidung muss der SR treffen?",
                                                                    None))
    # retranslateUi
