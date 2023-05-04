from PySide6.QtWidgets import QDialog, QTableWidgetItem, QHBoxLayout, QTableWidget, QAbstractItemView

from src.database import db
from src.datatypes import RegeltestQuestion
from src.ui_regeltest_archive import Ui_RegeltestArchiveDialog


class PreviousRegeltests(QDialog, Ui_RegeltestArchiveDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui = Ui_RegeltestArchiveDialog()
        self.ui.setupUi(self)

        self.ui.regeltestTable.removeRow(0)
        self.ui.regeltestTable.setSortingEnabled(False)

        self.ui.regeltestTable.itemDoubleClicked.connect(self.preview)

        self.regeltests = db.get_regeltests()
        for index, regeltest in enumerate(self.regeltests):
            self.ui.regeltestTable.insertRow(index)
            self.ui.regeltestTable.setItem(index, 0, QTableWidgetItem(str(regeltest.id)))
            self.ui.regeltestTable.setItem(index, 1, QTableWidgetItem(str(regeltest.title)))
            self.ui.regeltestTable.setItem(index, 2, QTableWidgetItem(str(len(regeltest.selected_questions))))
            self.ui.regeltestTable.setItem(index, 3, QTableWidgetItem(
                str(sum([x.available_points for x in regeltest.selected_questions]))))
            self.ui.regeltestTable.setItem(index, 4, QTableWidgetItem(regeltest.created.strftime("%d.%m.%Y (%H:%M)")))

    def preview(self, item: QTableWidgetItem):
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle("Fragenübersicht")
        preview_dialog.resize(500, 600)

        layout = QHBoxLayout(preview_dialog)
        preview_dialog.setLayout(layout)
        tableWidget = QTableWidget(0, 5, preview_dialog)

        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        tableWidget.horizontalHeader().setProperty("showSortIndicator", False)
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.verticalHeader().setVisible(False)
        tableWidget.verticalHeader().setStretchLastSection(False)

        tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Nr"))
        tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Frage"))
        tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Antwort"))
        tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Multiple Choice?"))
        tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Mögliche Punkte"))
        regeltest = self.regeltests[item.row()]

        for index, question in enumerate(regeltest.selected_questions):
            question = question  # type: RegeltestQuestion
            tableWidget.insertRow(index)

            questionWidget = QTableWidgetItem(question.question.question)
            questionWidget.setToolTip(question.question.question)
            answerWidget = QTableWidgetItem(question.question.answer_text)
            answerWidget.setToolTip(question.question.answer_text)

            tableWidget.setItem(index, 0, QTableWidgetItem(str(index + 1)))
            tableWidget.setItem(index, 1, questionWidget)
            tableWidget.setItem(index, 2, answerWidget)
            tableWidget.setItem(index, 3, QTableWidgetItem("Ja" if question.is_multiple_choice else "Nein"))
            tableWidget.setItem(index, 4, QTableWidgetItem(str(question.available_points)))

        layout.addWidget(tableWidget)

        preview_dialog.show()

    def get_selected_questions(self):
        items = self.ui.regeltestTable.selectedItems()
        if not items:
            return []
        else:
            regeltest = self.regeltests[items[0].row()]
        return [question.question for question in regeltest.selected_questions]
