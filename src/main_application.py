import webbrowser
from typing import List, Dict

import markdown2
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QTreeWidgetItem, QFileDialog, QApplication, QMessageBox, QDialog
from bs4 import BeautifulSoup

from . import controller, document_builder
from .basic_config import app_version, check_for_update, display_name, is_bundled
from .datatypes import Rulegroup, create_rulegroups, create_questions_and_mchoice
from .question_tree import RulegroupView, RuleDataModel, RuleSortFilterProxyModel
from .regeltestcreator import RegeltestSaveDialog, RegeltestSetup
from .ui_mainwindow import Ui_MainWindow
from .ui_update_checker import Ui_UpdateChecker


def load_dataset(parent: QWidget, reset_cursor=True) -> bool:
    def read_in(file_path: str):
        with open(file_path, 'r+', encoding='iso-8859-1') as file:
            soup = BeautifulSoup(file, "lxml")
        rulegroups = create_rulegroups(soup.find("gruppen"))
        questions, mchoice = create_questions_and_mchoice(soup("regelsatz"))
        return rulegroups, questions, mchoice

    file_name = QFileDialog.getOpenFileName(parent, caption="Fragendatei öffnen", filter="DFB Regeldaten (*.xml)")
    if len(file_name) == 0 or file_name[0] == "":
        return False
    QApplication.setOverrideCursor(Qt.WaitCursor)
    datasets = read_in(file_name[0])
    controller.clear_database()
    for dataset in datasets:
        controller.fill_database(dataset)
    if reset_cursor:
        QApplication.restoreOverrideCursor()
    return True


def save_dataset(parent: QWidget):
    file_name = QFileDialog.getSaveFileName(parent, caption="Fragendatei speichern", filter="DFB Regeldaten (*.xml)")
    if len(file_name) == 0 or file_name[0] == "":
        return
    QApplication.setOverrideCursor(Qt.WaitCursor)
    dataset = "<?xml version=\"1.0\" encoding=\"iso-8859-1\" ?>\n\
<REGELTEST>\n<GRUPPEN>\n"
    for rulegroup in controller.get_all_rulegroups():
        dataset += rulegroup.export()
    dataset += "</GRUPPEN>\n"
    for question in controller.get_all_questions():
        question_set = question[0].export()
        dataset += question_set[0]
        if question[1]:
            for mchoice in question[1]:
                dataset += mchoice.export()
        dataset += question_set[1]
    dataset += "</REGELTEST>"
    with open(file_name[0], "w+", encoding='iso-8859-1') as file:
        file.writelines(dataset)
    QApplication.restoreOverrideCursor()


def display_update_dialog(parent, releases):
    # new_version, description, url, download_url
    dialog = UpdateChecker(parent, releases, app_version.is_devrelease)
    dialog.exec()


def about_dialog():
    msg_box = QMessageBox()
    msg_box.setWindowTitle(f"Über {display_name}")
    msg_box.setText(f"<center><b>Regeltest-Creator</b></center>"
                    f"<center>v{app_version}</center><br>"
                    "<center>entwickelt von Jan Feil</center><br>"
                    "<a href=https://github.com/jfeil/RegeltestCreator>Weitere Informationen und Programmcode</a>")
    msg_box.exec()


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(QCoreApplication.translate("MainWindow", f"{display_name} - {app_version}"
                                                       , None))
        self.ui.actionRegeldatensatz_einladen.triggered.connect(self.load_dataset)
        self.ui.actionAuf_Updates_pr_fen.triggered.connect(lambda: display_update_dialog(self, check_for_update()))
        self.ui.action_ber.triggered.connect(about_dialog)

        self.ui.menuBearbeiten.setEnabled(False)
        self.ui.actionRegeltest_einrichten.setEnabled(False)
        self.ui.actionNeue_Kategorie_erstellen.setEnabled(False)
        self.ui.actionRegeltest_l_schen.setEnabled(False)

        self.ui.tabWidget.clear()
        self.ui.tabWidget.setTabsClosable(True)
        self.ui.tabWidget.tabCloseRequested.connect(self.delete_rulegroup)

        self.ui.regeltest_list.setAcceptDrops(True)
        self.ui.actionAnsicht_zur_cksetzen.triggered.connect(lambda: self.ui.regeltest_creator.show())
        self.ui.actionRegeldatensatz_exportieren.triggered.connect(lambda: save_dataset(self))

        self.ui.regeltest_list.model().rowsInserted.connect(self.rows_changed)
        self.ui.regeltest_list.model().rowsRemoved.connect(self.rows_changed)

        self.ui.add_questionlist.clicked.connect(self.setup_regeltest)
        self.ui.clear_questionlist.clicked.connect(self.clear_questionlist)

        self.ui.create_regeltest.clicked.connect(self.create_regeltest)

        self.ruletabs = {}  # type: Dict[int, RulegroupView]
        self.questions = {}  # type: Dict[QTreeWidgetItem, str]

    def show(self) -> None:
        super(MainWindow, self).show()
        if not is_bundled:
            return
        releases = check_for_update()
        update_available = False
        if (app_version.is_devrelease and releases[1]) or (not app_version.is_devrelease and releases[0]):
            update_available = True
        if update_available:
            display_update_dialog(self, releases)

    def clear_questionlist(self):
        self.ui.regeltest_list.clear()
        self.ui.regeltest_list.questions.clear()
        self.rows_changed()

    def delete_rulegroup(self, index_tabwidget: int):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Regelgruppe löschen.")
        msgBox.setText("Regelgruppe löschen.<br>"
                       "Möchtest du wirklich diese Fragengruppe löschen? Dies lässt sich nicht umkehren!")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel)
        ret = msgBox.exec()
        if ret == QMessageBox.Yes:
            index_rulegroup = list(self.ruletabs.keys())[index_tabwidget]
            self.ruletabs.pop(index_rulegroup)
            controller.delete(controller.get_rulegroup(index_rulegroup))
            self.ui.tabWidget.removeTab(index_tabwidget)

    def rows_changed(self):
        self.ui.regeltest_stats.setText(
            f"{self.ui.regeltest_list.count()} Fragen selektiert ({self.ui.regeltest_list.count() * 2} Punkte)")

    def load_dataset(self):
        load_dataset(self, reset_cursor=False)
        for question_tree in self.ruletabs.values():
            question_tree.refresh_questions()
        QApplication.restoreOverrideCursor()

    def create_ruletabs(self, rulegroups: List[Rulegroup]):
        for rulegroup in rulegroups:
            tab = QWidget()
            view = RulegroupView(tab, rulegroup_id=rulegroup.id)
            model = RuleDataModel(rulegroup.id, view)
            filter_model = RuleSortFilterProxyModel()
            filter_model.setSourceModel(model)
            view.setModel(filter_model)
            self.ruletabs[rulegroup.id] = view
            self.ui.tabWidget.addTab(tab, "")
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(tab), f"{rulegroup.id:02d} {rulegroup.name}")

    def setup_regeltest(self):
        regeltest_setup = RegeltestSetup(self)
        if regeltest_setup.exec():
            for question in regeltest_setup.collect_questions():
                self.ui.regeltest_list.add_question(question)

    def create_regeltest(self):
        question_set = []
        for signature in self.ui.regeltest_list.questions:
            question_set += [
                (controller.get_question(signature), controller.get_multiplechoice_by_foreignkey(signature))]
        settings = RegeltestSaveDialog(self)
        settings.ui.title_edit.setFocus()
        result = settings.exec()
        output_path = settings.ui.output_edit.text()
        if result:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            document_builder.create_document(question_set, output_path, settings.ui.title_edit.text()
                                             , icon_path=settings.ui.icon_path_edit.text())
            QApplication.restoreOverrideCursor()
            webbrowser.open_new(output_path)


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

        self.display()

    def display(self):
        release = self.versions[self.ui.comboBox.currentIndex()]
        if not release:
            self.ui.text.setText("<h1>Kein Update verfügbar!</h1>Die aktuellste Version ist bereits installiert.")
            return
        if release[3]:
            download_link = f'<a href="{release[3]}">Neueste Version jetzt herunterladen</a>'
        else:
            download_link = 'Noch kein Download für die aktuelle Plattform verfügbar.<br>' \
                            'Bitte versuche es später erneut.'
        self.ui.text.setText(f'<h1>Update <a href="{release[2]}">{release[0]}</a> verfügbar!</h1>'
                             f'{markdown2.markdown(release[1]).replace("h3>", "h4>").replace("h2>", "h3>").replace("h1>", "h2>")}{download_link}')
