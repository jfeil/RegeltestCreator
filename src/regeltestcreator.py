import random
from typing import Dict, List, Tuple

import markdown2
from PySide6.QtCore import Qt, QCoreApplication, Signal, QPoint
from PySide6.QtGui import QDrag, QShortcut, QKeySequence, QAction
from PySide6.QtWidgets import QListWidget, QTreeWidgetItem, QTreeWidget, QVBoxLayout, QDialog, QFileDialog, QWidget, \
    QSpacerItem, QSizePolicy, QMenu, QMessageBox
from PySide6.QtWidgets import QListWidgetItem

from src import controller
from src.datatypes import Question, Rulegroup
from src.question_editor import QuestionEditor
from src.ui_regeltest_save import Ui_RegeltestSave
from src.ui_regeltest_setup import Ui_RegeltestSetup
from src.ui_regeltest_setup_widget import Ui_RegeltestSetup_Rulegroup
from src.ui_update_checker import Ui_UpdateChecker


class RegeltestCreator(QListWidget):
    def __init__(self, *args):
        super(RegeltestCreator, self).__init__(*args)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.MultiSelection)
        self.questions = []  # type: List[str]
        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self)
        delete_shortcut.activated.connect(self.remove_selected_items)

    def add_question(self, question: Question):
        if question.signature in self.questions:
            return
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole, question.signature)
        item.setText(question.question)
        self.questions.append(question.signature)

    def remove_selected_items(self):
        rows = [index.row() for index in self.selectedIndexes()[::-1]]
        if not rows:
            return
        for index in rows:
            self.questions.pop(index)
            item = self.takeItem(index)
            del item

    def dropEvent(self, event):
        event.accept()
        if event.mimeData().hasFormat('application/questionitems'):
            data = event.mimeData().data('application/questionitems')
            signatures = data.data().decode()
            n = 32
            signatures = [signatures[i:i + n] for i in range(0, len(signatures), n)]
            for signature in signatures:
                self.add_question(controller.get_question(signature))


class QuestionTree(QTreeWidget):
    def __init__(self, parent, rulegroup_id):
        super(QuestionTree, self).__init__(parent)
        self.rulegroup_id = rulegroup_id
        self.questions = {}  # type: Dict[QTreeWidgetItem, str]
        self.setDragEnabled(True)
        self.setSelectionMode(QTreeWidget.MultiSelection)
        self.setDefaultDropAction(Qt.CopyAction)
        self.itemDoubleClicked.connect(self._handle_double_click)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.prepare_menu)
        self.setObjectName("tree_widget")
        vertical_layout = QVBoxLayout(parent)
        ___qtreewidgetitem = self.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"\u00c4nderungsdatum", None))
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"Antwort", None))
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Multiple choice?", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Frage", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Regelnummer", None))
        vertical_layout.addWidget(self)

    def _handle_double_click(self, item):
        editor = QuestionEditor(controller.get_question(self.questions[item]))
        if editor.exec() == QDialog.Accepted:
            # was updated
            signature = controller.update_question_set(editor.question, editor.mchoice)
            self._set_question(item, controller.get_question(signature))

    def add_new_question(self):
        new_question = Question()
        new_question.rulegroup = controller.get_rulegroup(self.rulegroup_id)
        new_question.rule_id = controller.get_new_question_id(self.rulegroup_id)
        editor = QuestionEditor(new_question)
        if editor.exec() == QDialog.Accepted:
            signature = controller.update_question_set(editor.question, editor.mchoice)
            self.add_question(controller.get_question(signature))

    def refresh_questions(self):
        for item, question_signature in self.questions.items():
            self._set_question(item, controller.get_question(question_signature))

    def add_question(self, question: Question):
        item = QTreeWidgetItem(self)
        self._set_question(item, question)

    def prepare_menu(self, pos: QPoint):
        def delete_selection(selected_items):
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Fragen löschen.")
            msgBox.setText("Fragen löschen.")
            if len(selected_items) == 1:
                text = f"Möchtest du wirklich diese Frage löschen? Dies lässt sich nicht umkehren!"
            else:
                text = f"Möchtest du wirklich diese {len(selected_items)} Fragen löschen? Dies lässt sich nicht umkehren!"
            msgBox.setInformativeText(text)
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Cancel)
            ret = msgBox.exec()
            if ret == QMessageBox.Yes:
                for item in selected_items:
                    controller.delete(controller.get_question(self.questions[item]))
                    self.questions.pop(item)
                    self.takeTopLevelItem(self.indexOfTopLevelItem(item))

        delete_bool = True
        items = self.selectedItems()
        actions = []
        if not items:
            items = [self.itemAt(pos)]
            text = "Diese Frage löschen"
            if items[0] is None:
                delete_bool = False
        else:
            clearSelAct = QAction(self)
            clearSelAct.setText("Auswahl zurücksetzen")
            clearSelAct.triggered.connect(lambda: self.clearSelection())
            actions += [clearSelAct]
            text = "Aktuelle Auswahl löschen"

        if delete_bool:
            deleteAct = QAction(self)
            deleteAct.setText(text)
            deleteAct.triggered.connect(lambda: delete_selection(items))
            actions += [deleteAct]

        create_action = QAction(self)
        create_action.setText("Neue Frage erstellen")
        create_action.triggered.connect(self.add_new_question)
        actions += [create_action]

        menu = QMenu(self)
        menu.addActions(actions)
        menu.exec(self.mapToGlobal(pos))

    def _set_question(self, item: QTreeWidgetItem, question: Question):
        def bool_to_char(value: bool):
            if value:
                return "✔"
            return "🗙"

        self.questions[item] = question.signature
        item.setText(0, str(question.rule_id))
        item.setText(1, question.question)
        item.setText(2, bool_to_char(question.answer_index != -1))
        item.setText(3, question.answer_text)
        item.setText(4, str(question.last_edited))
        item.setToolTip(1, question.question)
        item.setToolTip(3, question.answer_text)

    def startDrag(self, supportedActions: Qt.DropActions) -> None:
        super(QuestionTree, self).startDrag(supportedActions)
        indexes = self.selectionModel().selectedRows()
        signatures = [list(self.questions.values())[index.row()] for index in indexes]
        signatures = "".join(signatures).encode()
        if not indexes:
            return
        mimeData = self.model().mimeData(indexes)
        if not mimeData:
            return
        mimeData.setData('application/questionitems', bytearray(signatures))
        drag = QDrag(self)
        drag.setMimeData(mimeData)

        result = drag.exec_(supportedActions, Qt.CopyAction)
        if result == Qt.CopyAction:
            self.clearSelection()


class RegeltestSaveDialog(QDialog, Ui_RegeltestSave):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_RegeltestSave()
        self.ui.setupUi(self)
        self.ui.icon_edit_button.clicked.connect(self.open_icon)
        self.ui.output_edit_button.clicked.connect(self.create_save)

    def open_icon(self):
        file_name = QFileDialog.getOpenFileName(self, caption="Icon auswählen", filter="Icon file (*.jpg;*.png)")
        if len(file_name) == 0 or file_name[0] == "":
            return
        self.ui.icon_path_edit.setText(file_name[0])

    def create_save(self):
        file_name = QFileDialog.getSaveFileName(self, caption="Regeltest speichern", filter="Regeltest (*.pdf)")
        if len(file_name) == 0 or file_name[0] == "":
            return
        self.ui.output_edit.setText(file_name[0])


class RegeltestSetupRulegroup(QWidget, Ui_RegeltestSetup_Rulegroup):
    changed = Signal()

    def __init__(self, parent, rulegroup_parameters: Tuple[Rulegroup, int, int]):
        super(RegeltestSetupRulegroup, self).__init__(parent)
        self.ui = Ui_RegeltestSetup_Rulegroup()
        self.ui.setupUi(self)

        suffix = " von %d"
        self.rulegroup = rulegroup_parameters[0]
        self.ui.label_rulegroup.setText(f"{rulegroup_parameters[0].id:02d} - {rulegroup_parameters[0].name}")
        if rulegroup_parameters[1] == 0:
            # No Textquestion
            self.ui.spinBox_textquestion.setHidden(True)
            self.ui.label_2.setHidden(True)
            self.ui.horizontalLayout.removeItem(self.ui.right_spacer)
        self.ui.spinBox_textquestion.setRange(0, rulegroup_parameters[1])
        self.ui.spinBox_textquestion.setSuffix(suffix % rulegroup_parameters[1])
        if rulegroup_parameters[2] == 0:
            # No mchoice question
            self.ui.spinBox_mchoice.setHidden(True)
            self.ui.label_3.setHidden(True)
            self.ui.horizontalLayout.removeItem(self.ui.left_spacer)
        self.ui.spinBox_mchoice.setRange(0, rulegroup_parameters[2])
        self.ui.spinBox_mchoice.setSuffix(suffix % rulegroup_parameters[2])

        self.ui.spinBox_textquestion.valueChanged.connect(self.changed)
        self.ui.spinBox_mchoice.valueChanged.connect(self.changed)

    def get_parameters(self) -> Tuple[Rulegroup, int, int]:
        return self.rulegroup, self.ui.spinBox_textquestion.value(), self.ui.spinBox_mchoice.value()


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


class RegeltestSetup(QDialog, Ui_RegeltestSetup):
    def __init__(self, parent):
        super(RegeltestSetup, self).__init__(parent)
        self.ui = Ui_RegeltestSetup()
        self.ui.setupUi(self)
        self.ui.tabWidget.clear()

        self.rulegroup_widgets = []  # type: List[RegeltestSetupRulegroup]

        parameters = controller.get_rulegroup_config()
        divisor = 5
        for i in range(len(parameters) // divisor):
            self.create_tab(f"{parameters[i*divisor + 1][0].id:02d} - {parameters[(i+1)*divisor-1][0].id:02d}", parameters[i*divisor:(i+1)*divisor])
        if len(parameters) // divisor != len(parameters) / divisor:
            len_rest = len(parameters) % divisor
            if len_rest == 1:
                text = f"{parameters[-1][0].id:02d}"
            else:
                text = f"{parameters[len(parameters)-len_rest][0].id:02d} - {parameters[-1][0].id:02d}"
            self.create_tab(text, parameters[len(parameters) - len_rest:])
        self.updated()

    def updated(self):
        question_count = 0
        for rulegroup_widget in self.rulegroup_widgets:
            _, text, mchoice = rulegroup_widget.get_parameters()
            question_count += text + mchoice
        self.ui.statistics.setText(f"{question_count} Fragen aktuell ausgewählt ({question_count * 2} Punkte)")

    def create_tab(self, title: str, parameters: List[Tuple[Rulegroup, int, int]]):
        tab_widget = QWidget()
        self.ui.tabWidget.addTab(tab_widget, title)
        layout = QVBoxLayout(tab_widget)
        for parameter in parameters:
            rulegroup = RegeltestSetupRulegroup(tab_widget, parameter)
            rulegroup.changed.connect(self.updated)
            layout.addWidget(rulegroup)
            self.rulegroup_widgets += [rulegroup]
        layout.addItem(QSpacerItem(20, 257, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def collect_questions(self):
        questions = []
        for rulegroup_widget in self.rulegroup_widgets:
            rulegroup, text, mchoice = rulegroup_widget.get_parameters()
            text_questions = []
            mchoice_questions = []
            if text:
                text_questions = controller.get_questions_by_foreignkey(rulegroup.id, mchoice=False, randomize=True)[0:text]
            if mchoice:
                mchoice_questions = controller.get_questions_by_foreignkey(rulegroup.id, mchoice=True, randomize=True)[0:mchoice]
            text_questions += mchoice_questions
            if self.ui.checkbox_textmchoice.isChecked():
                random.shuffle(text_questions)
            questions += text_questions
        if self.ui.checkbox_rulegroups.isChecked():
            random.shuffle(questions)
        return questions
