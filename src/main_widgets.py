from __future__ import annotations

import datetime
from enum import Enum, auto
from typing import List, Tuple, Dict
from typing import TYPE_CHECKING, Optional

from PySide6.QtCore import Signal, QSortFilterProxyModel, QTimer
from PySide6.QtGui import QKeySequence, QShortcut, Qt
from PySide6.QtWidgets import QWidget, QListView, QMessageBox, QDialog, QDialogButtonBox, QListWidgetItem, \
    QTreeWidgetItem, QTableWidget, QGridLayout, QTableWidgetItem, QStyle
from sqlalchemy import func, nullsfirst, or_

from src import main_application
from src.database import db
from src.datatypes import Question, Statistics, SelfTestMode
from src.datatypes import QuestionGroup
from src.dock_widgets import SelfTestDockWidget
from src.filter_editor import FilterEditor
from src.question_table import RuleSortFilterProxyModel, QuestionGroupTableView, QuestionGroupDataModel
from src.ui_first_setup_widget import Ui_FirstSetupWidget
from src.ui_question_group_editor import Ui_QuestionGroupEditor
from src.ui_question_overview_widget import Ui_QuestionOverviewWidget
from src.ui_self_test_widget import Ui_SelfTestWidget

if TYPE_CHECKING:
    from src.main_application import MainWindow


class EditorResult(Enum):
    Success = auto()
    Invalid = auto()
    Canceled = auto()


class QuestionGroupEditor(QDialog, Ui_QuestionGroupEditor):
    def __init__(self, id: int = 1, name: str = "", parent=None):
        super(QuestionGroupEditor, self).__init__(parent=parent)
        self.ui = Ui_QuestionGroupEditor()
        self.ui.setupUi(self)
        self.id = id
        self.name = name

    @property
    def id(self):
        return self.ui.question_group_id.value()

    @id.setter
    def id(self, value):
        self.ui.question_group_id.setValue(value)

    @property
    def name(self):
        return self.ui.question_group_name.text()

    @name.setter
    def name(self, value):
        self.ui.question_group_name.setText(value)


class QuestionOverviewWidget(QWidget, Ui_QuestionOverviewWidget):
    def __init__(self, main_window: MainWindow):
        super(QuestionOverviewWidget, self).__init__(main_window)
        self.ui = Ui_QuestionOverviewWidget()
        self.ui.setupUi(self)
        self.main_window = main_window

        self.ui.tabWidget.clear()
        self.ui.tabWidget.setTabsClosable(True)
        self.ui.tabWidget.tabCloseRequested.connect(self.delete_question_group)
        self.ui.tabWidget.tabBarDoubleClicked.connect(self.rename_question_group)

        self.ui.filter_list.clear()
        left_shortcut = QShortcut(QKeySequence(QKeySequence.MoveToPreviousChar), self, None, None,
                                  Qt.WidgetWithChildrenShortcut)
        left_shortcut.activated.connect(self.last_question_group)

        right_shortcut = QShortcut(QKeySequence(QKeySequence.MoveToNextChar), self, None, None,
                                   Qt.WidgetWithChildrenShortcut)
        right_shortcut.activated.connect(self.next_question_group)

        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self.ui.filter_list, None, None, Qt.WidgetShortcut)
        delete_shortcut.activated.connect(self.delete_selected_filter)
        self.ui.filter_list.setSelectionMode(QListView.ExtendedSelection)
        self.ui.filter_list.itemDoubleClicked.connect(self.add_filter)
        self.ui.add_filter.clicked.connect(self.add_filter)

        self.question_group_tabs = []  # type: List[Tuple[QuestionGroup, QSortFilterProxyModel, QuestionGroupDataModel]]
        self.questions = {}  # type: Dict[QTreeWidgetItem, str]

    def next_question_group(self):
        if self.ui.tabWidget.currentIndex() < self.ui.tabWidget.count() - 1:
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.currentIndex() + 1)

    def last_question_group(self):
        if self.ui.tabWidget.currentIndex() > 0:
            self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.currentIndex() - 1)

    def delete_selected_filter(self):
        selection_model = self.ui.filter_list.selectionModel()
        if not selection_model.hasSelection():
            return
        selected_rows = sorted([index.row() for index in selection_model.selectedRows()], reverse=True)
        for index in selected_rows:
            self.__delete_filter(index)
        self.refresh_column_filter()

    def __delete_filter(self, index):
        RuleSortFilterProxyModel.filters.pop(index)
        filter_item = self.ui.filter_list.takeItem(index)
        del filter_item

    def delete_question_group(self, index_tabwidget: int):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Fragengruppe löschen.")
        msgBox.setText("Möchtest du diese Fragengruppe wirklich löschen?<br>"
                       "Dies lässt sich nicht umkehren!")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel)
        ret = msgBox.exec()
        if ret == QMessageBox.Yes:
            question_group, _, _ = self.question_group_tabs[index_tabwidget]
            self.question_group_tabs.pop(index_tabwidget)
            db.delete(question_group)
            self.ui.tabWidget.removeTab(index_tabwidget)

        if not self.question_group_tabs:
            self.main_window.initialize()

    def create_question_group_tab(self, question_group: QuestionGroup):
        tab = QWidget()
        view = QuestionGroupTableView(tab)
        model = QuestionGroupDataModel(question_group, view)
        filter_model = RuleSortFilterProxyModel()
        filter_model.setSourceModel(model)
        view.setModel(filter_model)
        view.sortByColumn(0, Qt.AscendingOrder)
        self.question_group_tabs.append((question_group, filter_model, model))
        self.ui.tabWidget.addTab(tab, "")
        self._update_tabtitle(self.ui.tabWidget.indexOf(tab))

    def _question_group_editor(self, question_group: QuestionGroup | None,
                               editor: QuestionGroupEditor) -> EditorResult:
        if editor.exec() == QDialog.Accepted:
            if question_group and question_group.id == editor.id:
                # ID was not changed -> update of title
                return EditorResult.Success
            if db.get_question_group(editor.id):
                QMessageBox(QMessageBox.Icon.Critical, "Fehler", "Fragengruppennummer existiert bereits!",
                            parent=self, ).exec()
                return EditorResult.Invalid
            return EditorResult.Success
        else:
            return EditorResult.Canceled

    def rename_question_group(self, index):
        if not self.question_group_tabs:
            return
        question_group, _, _ = self.question_group_tabs[index]
        editor = QuestionGroupEditor(id=question_group.id, name=question_group.name)
        result = self._question_group_editor(question_group, editor)
        while result == EditorResult.Invalid:
            result = self._question_group_editor(question_group, editor)
        if result == EditorResult.Success:
            question_group.id = editor.id
            question_group.name = editor.name
            self._update_tabtitle(index)
            db.commit()

    def add_question_group(self):
        editor = QuestionGroupEditor(id=db.get_new_question_group_id())
        result = self._question_group_editor(None, editor)
        while result == EditorResult.Invalid:
            result = self._question_group_editor(None, editor)
        if result == EditorResult.Success:
            if not self.question_group_tabs:
                self.ui.tabWidget.setTabsClosable(True)
                self.ui.add_filter.setDisabled(False)
                self.ui.tabWidget.clear()

            question_group = QuestionGroup(id=editor.id, name=editor.name)
            db.add_object(question_group)
            self.create_question_group_tab(question_group)

    def _update_tabtitle(self, index):
        question_group, _, _ = self.question_group_tabs[index]
        self.ui.tabWidget.setTabText(index, f"{question_group.id:02d} {question_group.name}")

    def add_filter(self, list_entry: QListWidgetItem | bool = False):
        if not list_entry or type(list_entry) == bool:
            # Add filter mode -> no list entry double_clicked
            current_configuration = None
            edit_mode = False
        else:
            # Edit mode -> Doubleclick on existing entry!
            index = self.ui.filter_list.indexFromItem(list_entry).row()
            current_configuration = RuleSortFilterProxyModel.filters[index][1]
            edit_mode = True
        properties = {}
        for name, visible in QuestionGroupDataModel.headers:
            if not visible:
                continue
            properties.update({name: Question.parameters[name]})
        editor = FilterEditor(filter_configuration=properties, current_filter=current_configuration)
        editor.exec()
        if editor.result == QDialogButtonBox.ButtonRole.DestructiveRole:
            # Closed via Discard
            if not edit_mode:
                return
            else:
                self.__delete_filter(index)
        elif editor.result == QDialogButtonBox.ButtonRole.AcceptRole:
            # Closed via Save
            dict_key, filter_option, filter_value = editor.current_configuration()
            if not edit_mode:
                RuleSortFilterProxyModel.filters += [(editor.create_filter(), (dict_key, filter_option, filter_value))]
                self.ui.filter_list.addItem(
                    QListWidgetItem(f"{properties[dict_key].table_header} {filter_option} '{filter_value}'"))
            else:
                RuleSortFilterProxyModel.filters[index] = (
                    editor.create_filter(), (dict_key, filter_option, filter_value))
                list_entry.setText(f"{properties[dict_key].table_header} {filter_option} '{filter_value}'")
        elif editor.result == QDialogButtonBox.ButtonRole.RejectRole:
            # Closed via Cancel
            return
        elif editor.result is None:
            # Closed via X
            return
        else:
            raise ValueError(f"Invalid response {editor.result}")
        self.refresh_column_filter()

    def refresh_column_filter(self):
        for (_, filter_model, _) in self.question_group_tabs:
            filter_model = filter_model  # type: RuleSortFilterProxyModel
            filter_model.invalidateFilter()

    def create_ruletabs(self, question_groups: List[QuestionGroup]):
        self.ui.tabWidget.setTabsClosable(True)
        self.ui.add_filter.setDisabled(False)
        for question_group in question_groups:
            self.create_question_group_tab(question_group)

    def reset(self):
        for (_, _, model) in self.question_group_tabs:
            model.reset()


class FirstSetupWidget(QWidget, Ui_FirstSetupWidget):
    action_done = Signal()

    def __init__(self, main_window: MainWindow):
        super(FirstSetupWidget, self).__init__(main_window)
        self.ui = Ui_FirstSetupWidget()
        self.ui.setupUi(self)

        self.ui.create_button.clicked.connect(main_window.add_question_group)
        self.ui.import_button.clicked.connect(self.load_dataset)

    def load_dataset(self):
        main_application.load_dataset(self.parent())
        self.action_done.emit()


class Timer:
    def __init__(self, value: int):
        self.init_value = value
        self.current_value = value

    def __sub__(self, other):
        self.current_value = max(0, self.current_value - other)
        return self

    def __add__(self, other):
        self.init_value = other
        self.current_value = other
        return self

    def __int__(self):
        return int(self.current_value)

    def __bool__(self):
        return self.current_value > 0

    def __eq__(self, other):
        return self.init_value == other

    def __ne__(self, other):
        return self.init_value != other

    def reset(self):
        self.current_value = self.init_value


class SelfTestWidget(QWidget, Ui_SelfTestWidget):
    def __init__(self, main_window: MainWindow, dock_widget: SelfTestDockWidget):
        super(SelfTestWidget, self).__init__(main_window)
        self.ui = Ui_SelfTestWidget()
        self.ui.setupUi(self)

        self.ui.time_label.setMinimumSize(self.ui.time_label.sizeHint())

        self.main_window = main_window
        self.dock_widget = dock_widget
        self.ui.stackedWidget.setCurrentIndex(0)

        self._next_questions = []  # type: List[Question]
        self._previous_questions = []  # type: List[Question]
        self._current_question = None  # type: Optional[Question]

        self.timer_question = QTimer(self)
        self.timer_question.setInterval(1000)
        self.timer_question.timeout.connect(lambda: self.update_timer(self.timer_question))
        self.timer_answer = QTimer(self)
        self.timer_answer.setInterval(1000)
        self.timer_answer.timeout.connect(lambda: self.update_timer(self.timer_answer))

        self.time_question = Timer(0)  # type: Timer
        self.time_answer = Timer(0)  # type: Timer

        self.current_question = None  # type: Optional[Question]
        self.previous_questions = []
        self.next_questions = []

        self.dock_widget.changed.connect(self.selected_groups_changed)
        self.dock_widget.timer_question.connect(self.update_timer_question)
        self.dock_widget.timer_answer.connect(self.update_timer_answer)
        self.dock_widget.ui.question_overview_button.clicked.connect(self.display_overview)

        self.ui.next_button.pressed.connect(self.next_question)
        self.ui.previous_button.pressed.connect(self.previous_question)
        self.ui.switch_eval_button.pressed.connect(self.evaluate_question)
        self.ui.correct_button.pressed.connect(self.correct_answered)
        self.ui.incorrect_button.pressed.connect(self.incorrect_answered)

        self.ui.statistics_button.set_content(self.ui.statistics_frame)
        self.update_progressbar(0, 0)
        self.init_timer_display()

    def create_statistics(self):
        if not self.current_question:
            return ""
        if not self.current_question.statistics:
            return "Keine Statistiken bisher verfügbar."
        else:
            statistics = f"Korrekt beantwortet {self._current_question.statistics.correct_solved}\n" \
                         f"Inkorrekt beantwortet {self._current_question.statistics.wrong_solved}\n" \
                         f"Konsekutiv korrekt beantwortet {self._current_question.statistics.continous_solved_count}\n" \
                         f"Zuletzt beantwortet {self._current_question.statistics.last_tested.date()}"
            if self.dock_widget.mode == SelfTestMode.level:
                statistics = f"Level {self._current_question.statistics.level}\n" + statistics
        return statistics

    @property
    def current_question(self):
        return self._current_question

    @current_question.setter
    def current_question(self, value):
        self._current_question = value
        self.ui.switch_eval_button.setDisabled(not value)
        self.ui.user_answer_test.setDisabled(not value)
        self.ui.statistics_button.setDisabled(not value)
        self.dock_widget.ui.question_overview_button.setDisabled(not value)
        if not value:
            self.stop_timer()
            self.ui.user_answer_test.setText("")
            self.ui.question_label_test.setText("Keine Frage verfügbar.")
            self.ui.statistics_button.setChecked(False)
            self.update_progressbar(0, 0)
        else:
            self.start_timer()
            self.ui.question_label_test.setText(self._current_question.question)
            self.ui.question_label_test.setToolTip(self.create_statistics())
            self.ui.statistics_label.setText(self.create_statistics())
        self.ui.statistics_button.update_animation()
        self.update_timer_display()

    @property
    def previous_questions(self):
        return self._previous_questions

    @previous_questions.setter
    def previous_questions(self, value):
        self.ui.previous_button.setDisabled(not value)
        self._previous_questions = value

    @property
    def next_questions(self):
        return self._next_questions

    @next_questions.setter
    def next_questions(self, value):
        self._next_questions = value
        self.ui.next_button.setDisabled(not self._next_questions)
        self.ui.user_answer_test.setText("")

    def next_question(self):
        if not self.next_questions:
            if not self.previous_questions:
                return
            else:
                self.previous_question()
                return
        if self.current_question:
            self.previous_questions += [self.current_question]
        self.current_question = self.next_questions[0]
        self.next_questions = self.next_questions[1:]

        self.update_progressbar(len(self.previous_questions),
                                len(self.previous_questions) + 1 + len(self.next_questions))

    def previous_question(self):
        if not self.previous_questions:
            if not self.next_questions:
                return
            else:
                self.next_question()
                return
        if self.current_question:
            self.next_questions = [self.current_question] + self.next_questions
        self.current_question = self.previous_questions[-1]
        self.previous_questions = self.previous_questions[:-1]

        self.update_progressbar(len(self.previous_questions),
                                len(self.previous_questions) + 1 + len(self.next_questions))

    def evaluate_question(self):
        self.dock_widget.lock()
        self.ui.question_label_eval.setText(self.current_question.question)
        self.ui.correct_answer_eval.setText(self.current_question.answer_text)
        self.ui.user_answer_eval.setText(self.ui.user_answer_test.toPlainText())
        self.ui.stackedWidget.setCurrentIndex(1)

    def correct_answered(self):
        if not self.current_question.statistics:
            self.current_question.statistics = Statistics()
            db.commit()
        self.current_question.statistics.correct_solved += 1
        self.current_question.statistics.continous_solved_count += 1
        self.current_question.statistics.last_tested = datetime.datetime.now()
        if self.dock_widget.mode == SelfTestMode.random:
            pass
        elif self.dock_widget.mode == SelfTestMode.level:
            # if level is 7 -> never re-asked!
            self.current_question.statistics.level += 1
        elif self.dock_widget.mode == SelfTestMode.prioritize_new:
            pass
        else:
            raise ValueError("Not supported mode.")

        if self.current_question.statistics.level == 0:
            self.current_question.statistics.level = 1

        db.commit()

        self.dock_widget.unlock()
        # remove correct question from stack
        self.current_question = None
        self.next_question()
        self.ui.stackedWidget.setCurrentIndex(0)

    def incorrect_answered(self):
        if not self.current_question.statistics:
            self.current_question.statistics = Statistics()
            db.commit()
        self.current_question.statistics.wrong_solved += 1
        self.current_question.statistics.continous_solved_count = 0
        self.current_question.statistics.last_tested = datetime.datetime.now()
        if self.dock_widget.mode == SelfTestMode.random:
            pass
        elif self.dock_widget.mode == SelfTestMode.level:
            self.current_question.statistics.level = max(self.current_question.statistics.level - 1, 0)
        elif self.dock_widget.mode == SelfTestMode.prioritize_new:
            pass
        else:
            raise ValueError("Not supported mode.")
        db.commit()

        self.dock_widget.unlock()
        # move wrong question to the end
        self.next_questions += [self.current_question]
        self.current_question = None
        self.next_question()
        self.ui.stackedWidget.setCurrentIndex(0)

    def selected_groups_changed(self):
        questions = db.get_questions_by_foreignkey(self.dock_widget.get_question_groups(), as_query=True)

        if self.dock_widget.mode == SelfTestMode.random:
            questions = self.prepare_random_mode(questions)
        elif self.dock_widget.mode == SelfTestMode.level:
            questions = self.prepare_level_mode(questions)
        elif self.dock_widget.mode == SelfTestMode.prioritize_new:
            questions = self.prepare_prioritize_new(questions)
        else:
            raise ValueError("Not supported mode.")

        self.update_progressbar(0, len(questions))

        self.previous_questions = []
        if not questions:
            self.current_question = None
            self.next_questions = []
        else:
            self.current_question = questions[0]
            self.next_questions = questions[1:]

    def update_progressbar(self, current_index: int, question_count: int):
        if question_count <= 1:
            self.ui.progressbar_bar.setMaximum(1)
            self.ui.progressbar_bar.setValue(0)
            self.ui.progressbar_label.setText(f"{question_count} / {question_count}")
        else:
            self.ui.progressbar_bar.setMaximum(question_count - 1)
            self.ui.progressbar_bar.setValue(current_index)
            self.ui.progressbar_label.setText(f"{current_index + 1} / {question_count}")

    def init_timer_display(self):
        time = self.time_question.init_value + self.time_answer.init_value
        if time == 0:
            time = 1
            self.ui.time_progressbar.setValue(0)
        else:
            self.ui.time_progressbar.setValue(time)
        self.ui.time_progressbar.setMaximum(time)
        self.update_timer_display()

    def update_timer_display(self):
        time = int(self.time_question) + int(self.time_answer)
        self.ui.time_label.setText(f"{time}s")
        self.ui.time_progressbar.setValue(time)

    def update_timer_question(self, value: int):
        if value == 0:
            self.timer_question.stop()
        self.current_question = self.current_question
        self.time_question += value
        if value != 0:
            self.start_timer()
        self.init_timer_display()

    def update_timer_answer(self, value: int):
        if value == 0:
            self.timer_answer.stop()
        self.time_answer += value
        if value != 0:
            self.start_timer()
        self.init_timer_display()

    @staticmethod
    def prepare_random_mode(dataset) -> List[Question]:
        dataset = dataset.order_by(func.random())
        return dataset.all()

    @staticmethod
    def prepare_level_mode(dataset) -> List[Question]:
        levels_to_days = [0, 1, 3, 9, 29, 90]
        today = datetime.datetime.now()
        # randomize and outerjoin with statistics (outerjoin -> nones and statistic objects available)
        dataset = dataset.outerjoin(Question.statistics)
        dataset = dataset.filter((Question.statistics == None) | or_(
            ((Statistics.level == level) & (Statistics.last_tested < today - datetime.timedelta(days)))
            for (level, days) in enumerate(levels_to_days)))
        # order the last_tested_date ascending and put the nones before them (already randomized in step 1)
        dataset = dataset.order_by(nullsfirst(Statistics.level.asc()))
        return dataset.all()

    @staticmethod
    def prepare_prioritize_new(dataset) -> List[Question]:
        # randomize and outerjoin with statistics (outerjoin -> nones and statistic objects available)
        dataset = dataset.outerjoin(Question.statistics)
        # order the last_tested_date ascending and put the nones before them (already randomized in step 1)
        dataset = dataset.order_by(Statistics.last_tested.asc().nulls_first())
        return dataset.all()

    def start_timer(self):
        self.timer_question.stop()
        self.timer_answer.stop()
        self.time_question.reset()
        self.time_answer.reset()
        self.update_timer_display()
        if self.current_question is None:
            return
        if self.time_question and self.time_question != 0:
            self.timer_question.start()
        elif self.time_answer and self.time_answer != 0:
            self.timer_answer.start()

    def update_timer(self, timer_type: QTimer):
        if timer_type == self.timer_question:
            self.time_question -= self.timer_question.interval() / 1000
            if not self.time_question:
                if self.time_question != 0:
                    self.ui.question_label_test.setText("")
                self.timer_question.stop()
                if self.time_answer != 0:
                    self.timer_answer.start()
        elif timer_type == self.timer_answer:
            self.time_answer -= self.timer_answer.interval() / 1000
            if not self.time_answer:
                self.evaluate_question()
                self.timer_answer.stop()
        else:
            raise ValueError("Wrong timer")
        self.update_timer_display()

    def stop_timer(self):
        self.timer_question.stop()
        self.time_question.reset()
        self.timer_answer.stop()
        self.time_answer.reset()
        self.ui.time_progressbar.setDisabled(True)

    def reset(self):
        self.dock_widget.reset()
        self.dock_widget.unlock()
        self.ui.stackedWidget.setCurrentIndex(0)

    def display_overview(self):
        if not self.current_question:
            return
        questions = self.previous_questions + [self.current_question] + self.next_questions

        dialog = QDialog(self)
        dialog.setWindowTitle("Übersicht der Fragen")
        layout = QGridLayout(dialog)
        layout.setSizeConstraint(QGridLayout.SetFixedSize)
        table = QTableWidget(len(questions), 4, dialog)
        layout.addWidget(table)

        table.setHorizontalHeaderLabels(["Regelgruppe", "Frage", "Level", "Zuletzt getestet"])

        for index, question in enumerate(questions):
            question_text = question.question
            if question.statistics:
                level = question.statistics.level
                last_tested = question.statistics.last_tested.date()
            else:
                level = 0
                last_tested = "Niemals"

            rulegroup_item = QTableWidgetItem(str(question.question_group.name))
            rulegroup_item.setToolTip(str(question.question_group.name))
            table.setItem(index, 0, rulegroup_item)

            question_item = QTableWidgetItem(question_text)
            question_item.setToolTip(question_text)
            table.setItem(index, 1, question_item)

            level_item = QTableWidgetItem(str(level))
            table.setItem(index, 2, level_item)

            last_tested_item = QTableWidgetItem(str(last_tested))
            table.setItem(index, 3, last_tested_item)

        width = table.verticalHeader().width()
        width += table.horizontalHeader().length()
        width += table.frameWidth() * 2

        height = table.verticalHeader().length()
        height += table.horizontalHeader().height()
        height += table.frameWidth() * 2

        if height > self.height():
            # scrolling required
            width += table.style().pixelMetric(QStyle.PM_ScrollBarExtent)
            height = self.height()

        table.setFixedHeight(height)
        table.setFixedWidth(width)

        dialog.exec()
