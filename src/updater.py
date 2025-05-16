import os
import shutil
import stat
import subprocess
import sys
from typing import Optional

import markdown2
import requests
from PySide6.QtCore import Signal, QThread, Qt
from PySide6.QtWidgets import QDialog, QMessageBox

from src.basic_config import app_dirs, current_platform, is_bundled
from src.ui_update_checker import Ui_UpdateChecker


class UpdateChecker(QDialog, Ui_UpdateChecker):
    def __init__(self, parent, versions, display_dev=False):
        super(UpdateChecker, self).__init__(parent)
        self.ui = Ui_UpdateChecker()
        self.ui.setupUi(self)
        self.setWindowTitle("Update-Check")
        self.versions = versions

        self.ui.comboBox.currentIndexChanged.connect(self.display)

        if display_dev:
            self.ui.comboBox.setCurrentIndex(1)

        self.ui.text.setTextFormat(Qt.RichText)
        self.ui.text.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.ui.text.setOpenExternalLinks(True)

        self.download_link = None  # type: Optional[str]
        self.ui.install_update_button.clicked.connect(self.update)
        self.ui.install_update_button.setDisabled(True)
        self.ui.download_progress.setVisible(False)
        if not is_bundled:
            self.ui.install_update_button.setText("Auto-Update ist nur mit der kompilierten Version möglich!")
        if current_platform == 'Darwin':
            self.ui.install_update_button.setVisible(False)
        self.display()

    def display(self):
        release = self.versions[self.ui.comboBox.currentIndex()]
        if not release:
            self.ui.text.setText("<h1>Kein Update verfügbar!</h1>Die aktuellste Version ist bereits installiert.")
            self.download_link = None
            if is_bundled:
                self.ui.install_update_button.setDisabled(True)
            return
        if release[3]:
            download_link = f'<a href="{release[3]}">Neueste Version jetzt herunterladen</a>'
            self.download_link = release[3]
            if is_bundled:
                self.ui.install_update_button.setDisabled(False)
        else:
            download_link = 'Noch kein Download für die aktuelle Plattform verfügbar.<br>' \
                            'Bitte versuche es später erneut.'
            self.download_link = None
            if is_bundled:
                self.ui.install_update_button.setDisabled(True)
        release_notes = markdown2.markdown(release[1]).replace("h3>", "h4>").replace("h2>", "h3>").replace("h1>", "h2>")
        self.ui.text.setText(f'<h1>Update <a href="{release[2]}">{release[0]}</a> verfügbar!</h1>'
                             f'{release_notes}{download_link}')

    def update(self) -> None:
        def progressbar_tracking(value):
            self.ui.download_progress.setValue(value)
            if value != 100:
                return

            info_box = QMessageBox(self)
            info_box.setWindowTitle("Update erfolgreich heruntergeladen!")
            info_box.setText("Die Installation dauert ca. 15 Sekunden.")
            info_box.setInformativeText("Dabei wird die Applikation beendet und nach "
                                        "erfolgreichem Update erneut gestartet.")
            info_box.exec()
            if current_platform == 'Darwin':
                st = os.stat(download_path)
                os.chmod(download_path, st.st_mode | stat.S_IEXEC)
            subprocess.Popen([download_path, sys.executable, str(os.getpid())])
            sys.exit(0)

        if not self.download_link:
            return

        self.ui.download_progress.setVisible(True)

        if os.path.isdir(app_dirs.user_cache_dir):
            shutil.rmtree(app_dirs.user_cache_dir, ignore_errors=True)
        if not os.path.isdir(app_dirs.user_cache_dir):
            os.makedirs(app_dirs.user_cache_dir)

        executable_name = "RegeltestCreator"

        if current_platform == 'Darwin':
            executable_name += ".app.zip"
        elif current_platform == 'Windows':
            executable_name += ".exe"

        download_path = os.path.join(app_dirs.user_cache_dir, executable_name)

        request = requests.get(self.download_link, stream=True)
        filesize = request.headers['Content-Length']

        file_handle = open(download_path, 'wb+')
        downloadThread = DownloadThread(request, filesize, file_handle, buffer=10240)
        downloadThread.download_progress.connect(progressbar_tracking)
        downloadThread.run()


class DownloadThread(QThread):
    download_progress = Signal(int)

    def __init__(self, request, filesize, fileobj, buffer):
        super(DownloadThread, self).__init__()
        self.request = request
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer

    def run(self):
        try:
            offset = 0
            for chunk in self.request.iter_content(chunk_size=self.buffer):
                if not chunk:
                    break
                self.fileobj.seek(offset)
                self.fileobj.write(chunk)
                offset = offset + len(chunk)
                download_progress = offset / int(self.filesize) * 100
                if download_progress != 100:
                    self.download_progress.emit(int(download_progress))

            self.fileobj.close()
            self.download_progress.emit(100)
            self.exit(0)

        except Exception as e:
            print(e)
