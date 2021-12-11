import logging
import sys

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication, QFileDialog
from bs4 import BeautifulSoup
import logging

from src.basic_config import log_level
from src import controller
from src.database import db
from src.datatypes import create_rulegroups, create_questions_and_mchoice
from src.main_application import MainWindow, load_dataset

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(log_level)
logging.getLogger().setLevel(log_level)


def run():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    if not db:
        if not load_dataset(main_window):
            sys.exit(1)
    controller.populate_tabwidget(main_window)
    controller.populate_questions(main_window)
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
    sys.exit(0)
