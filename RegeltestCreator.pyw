import logging
import sys

from PySide6.QtWidgets import QApplication

from src.basic_config import log_level
from src.database import db
from src.main_application import MainWindow

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(log_level)
logging.getLogger().setLevel(log_level)


def run():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.initialize()
    main_window.show()
    exit_code = app.exec()
    db.close_connection()
    sys.exit(exit_code)


if __name__ == '__main__':
    run()
    sys.exit(0)
