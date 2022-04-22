from __future__ import annotations

import webbrowser
from typing import TYPE_CHECKING

from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog, QApplication

from src import document_builder
from src.database import db
from src.datatypes import Regeltest
from src.regeltestcreator import RegeltestSetup, RegeltestSaveDialog
from src.ui_regeltest_creator_dockwidget import Ui_regeltest_creator_dockwidget
from src.ui_self_test_dockwidget import Ui_self_test_dockwidget

if TYPE_CHECKING:
    from src.main_application import MainWindow


class RegeltestCreatorDockwidget(QWidget, Ui_regeltest_creator_dockwidget):
    def __init__(self, main_window: MainWindow):
        super(RegeltestCreatorDockwidget, self).__init__(main_window)
        self.ui = Ui_regeltest_creator_dockwidget()
        self.ui.setupUi(self)

        self.ui.regeltest_list.setAcceptDrops(True)
        self.ui.regeltest_list.model().rowsInserted.connect(self.regeltest_list_updated)
        self.ui.regeltest_list.model().rowsRemoved.connect(self.regeltest_list_updated)

        self.ui.add_questionlist.clicked.connect(self.setup_regeltest)
        self.ui.clear_questionlist.clicked.connect(self.clear_questionlist)

        self.ui.create_regeltest.clicked.connect(self.create_regeltest)

    def clear_questionlist(self):
        self.ui.regeltest_list.clear()
        self.ui.regeltest_list.questions.clear()
        self.regeltest_list_updated()

    def regeltest_list_updated(self):
        self.ui.regeltest_stats.setText(
            f"{self.ui.regeltest_list.count()} Fragen selektiert ({self.ui.regeltest_list.count() * 2} Punkte)")

    def setup_regeltest(self):
        regeltest_setup = RegeltestSetup(self)
        if regeltest_setup.exec():
            for question in regeltest_setup.collect_questions():
                self.ui.regeltest_list.add_question(question)

    def create_regeltest(self):
        questions = []
        for signature in self.ui.regeltest_list.questions:
            questions += [db.get_question(signature)]
        settings = RegeltestSaveDialog(self)
        settings.ui.title_edit.setFocus()
        result = settings.exec()
        output_path = settings.ui.output_edit.text()
        if result == QDialog.Accepted:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            if settings.ui.icon_path_edit.text():
                icon = Image.open(settings.ui.icon_path_edit.text())
            else:
                icon = None
            db.add_object(Regeltest(title=settings.ui.title_edit.text(), description="", icon=icon.tobytes(),
                                    questions=questions))
            document_builder.create_document(questions, output_path, settings.ui.title_edit.text(),
                                             icon=icon)
            QApplication.restoreOverrideCursor()
            webbrowser.open_new(output_path)


class SelfTestDockWidget(QWidget, Ui_self_test_dockwidget):
    def __init__(self, main_window: MainWindow):
        super(SelfTestDockWidget, self).__init__(main_window)
        self.ui = Ui_self_test_dockwidget()
        self.ui.setupUi(self)
