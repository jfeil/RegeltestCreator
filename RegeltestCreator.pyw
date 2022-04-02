import logging
import sys

from PySide6.QtWidgets import QApplication

from src import db_abstraction
from src.basic_config import log_level
from src.main_application import MainWindow

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(log_level)
logging.getLogger().setLevel(log_level)


def run():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.create_ruletabs(db_abstraction.get_rulegroups())
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
    sys.exit(0)
