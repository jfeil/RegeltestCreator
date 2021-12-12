from PySide6.QtCore import Qt, QModelIndex, QMimeData, QCoreApplication
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QListWidget, QTreeWidgetItem, QTreeWidget, QVBoxLayout

from src import controller
from src.datatypes import Question
from src.question_editor import QuestionEditor


class RegeltestCreator(QListWidget):
    def __init__(self, *args):
        super(RegeltestCreator, self).__init__(*args)

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            data = event.mimeData()
            source_item = QStandardItemModel()
            source_item.dropMimeData(data, Qt.CopyAction, 0, 0, QModelIndex())
            print(source_item.item(0, 0).text())


class QuestionTree(QTreeWidget):
    def __init__(self, parent):
        super(QuestionTree, self).__init__(parent)
        self.questions = {}
        self.setDragEnabled(True)
        self.itemDoubleClicked.connect(self._handle_double_click)
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
        if editor.exec() == 1:
            # was updated
            self._set_question(item, controller.get_question(self.questions[item]))

    def refresh_questions(self):
        for item, question_signature in self.questions.items():
            self._set_question(item, controller.get_question(question_signature))

    def add_question(self, question: Question):
        item = QTreeWidgetItem(self)
        self._set_question(item, question)

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

    def startDrag(self, supportedActions:Qt.DropActions) -> None:
        item = self.currentItem()
        mimeData = QMimeData()
        """
        QByteArray ba;
        ba = item->text().toLatin1().data();
        mimeData.setData("application/x-item", ba);
        QDrag * drag = new
        QDrag(this);
        drag->setMimeData(mimeData);
        if (drag->exec(Qt::MoveAction) == Qt: :
            MoveAction) {
            delete
        takeItem(row(item));
        emit
        itemDroped();
        }"""