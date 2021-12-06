import logging
import sys

from PySide6.QtWidgets import QApplication, QFileDialog
from bs4 import BeautifulSoup
import logging

from src.basic_config import log_level
from src import controller
from src.database import db
from src.datatypes import create_rulegroups, create_questions_and_mchoice
from src.main_application import MainWindow

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(log_level)
logging.getLogger().setLevel(log_level)


def read_in(file_name):
    with open(file_name, 'r+') as file:
        soup = BeautifulSoup(file, "lxml")
    rulegroups = create_rulegroups(soup.find("gruppen"))
    questions, mchoice = create_questions_and_mchoice(soup("regelsatz"))
    return rulegroups, questions, mchoice


def run():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    if not db:
        file_name = QFileDialog.getOpenFileName(main_window, caption="Open Questionfile", filter="DFB Regeldaten (*.xml)")
        if len(file_name) == 0 or file_name[0] == "":
            sys.exit(1)
        datasets = read_in(file_name[0])
        for dataset in datasets:
            db.fill_database(dataset)
    controller.populate_tabwidget(main_window)
    controller.populate_questions(main_window)
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()

    sys.exit(0)
    args = sys.argv
    if not db:
        datasets = read_in(args[1])
        for dataset in datasets:
            db.fill_database(dataset)
    logging.info("Successfully started!")
