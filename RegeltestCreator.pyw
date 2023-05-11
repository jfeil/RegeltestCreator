import logging
import os
import shutil
import sys
import time

import psutil
from PySide6.QtCore import Signal, QThread
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel

from src.basic_config import log_level
from src.database import db
from src.main_application import MainWindow

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(log_level)
logging.getLogger().setLevel(log_level)


class UpdateWorker(QThread):
    finished = Signal()

    def __init__(self, original_path: str, old_pid: int):
        self.original_path = original_path
        self.old_pid = old_pid

        super().__init__()

    def run(self):
        time.sleep(0.5)
        while psutil.pid_exists(self.old_pid):
            time.sleep(0.2)
        os.remove(self.original_path)
        shutil.copy(sys.executable, self.original_path)
        self.finished.emit()


class UpdateFinishDialog(QDialog):
    def __init__(self, original_path: str, old_pid: str):
        super().__init__()
        self.setWindowTitle("Update abschließen")
        self.setModal(True)
        self.setFixedSize(300, 100)

        layout = QVBoxLayout(self)
        self.label = QLabel("Letzte Update-Schritte durchführen...", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.worker = UpdateWorker(original_path, int(old_pid))
        self.worker.finished.connect(self.close)
        self.worker.start()

    def closeEvent(self, event):
        # Prevent closing the dialog while the background task is running
        if self.worker.isRunning():
            event.ignore()
        else:
            event.accept()


def run():
    app = QApplication(sys.argv)
    if len(sys.argv) == 3:
        test = UpdateFinishDialog(sys.argv[1], sys.argv[2])
        test.exec()
        pass
    main_window = MainWindow()
    main_window.initialize()
    main_window.show()
    exit_code = app.exec()
    db.close_connection()
    sys.exit(exit_code)


if __name__ == '__main__':
    run()
    sys.exit(0)
