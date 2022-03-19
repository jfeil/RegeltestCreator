from datetime import datetime
from typing import Dict, Tuple, Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLineEdit, QCheckBox, QDateEdit, QSpinBox

from src.datatypes import QuestionParameters, FilterOption
from src.ui_filter_editor import Ui_FilterEditor


class FilterEditor(QDialog, Ui_FilterEditor):
    def __init__(self, filter_configuration: Dict[str, QuestionParameters], current_filter=None, parent=None,
                 window_flags=Qt.Dialog):
        super(FilterEditor, self).__init__(parent, window_flags)
        self.ui = Ui_FilterEditor()
        self.ui.setupUi(self)
        self.filter = None

        if current_filter:
            self.setWindowTitle("Filter bearbeiten")
        else:
            self.setWindowTitle("Filter erstellen")

        self.filter_configuration = filter_configuration

        self.ui.combobox_column.addItems(
            [filterparams.table_header for filterparams in self.filter_configuration.values()])
        self.update_filteroptions(self.ui.combobox_column.currentIndex())

        self.ui.combobox_column.currentIndexChanged.connect(self.update_filteroptions)

    def update_filteroptions(self, index):
        self.ui.combobox_filteroption.clear()

        current_params = list(self.filter_configuration.values())[index]
        self.ui.combobox_filteroption.addItems([str(options) for options in current_params.filter_options])

        if self.filter:
            self.ui.gridLayout.removeWidget(self.filter)
            self.filter.deleteLater()
            self.filter = None

        if current_params.datatype == str:
            self.filter = QLineEdit()
        elif current_params.datatype == bool:
            self.filter = QCheckBox()
        elif current_params.datatype == datetime:
            self.filter = QDateEdit()
        elif current_params.datatype == int:
            self.filter = QSpinBox()
        else:
            return

        self.ui.gridLayout.addWidget(self.filter, 2, 1, 1, 1)

    def create_filter(self) -> Tuple[str, Callable]:
        # ('answer_text', lambda x: 'FaD' in x)
        index = self.ui.combobox_column.currentIndex()
        dict_key, parameters = list(self.filter_configuration.items())[index]
        parameters = parameters  # type: QuestionParameters

        filter_option = parameters.filter_options[self.ui.combobox_filteroption.currentIndex()]

        if parameters.datatype == str:
            value = self.filter.text()
        elif parameters.datatype == bool:
            value = self.filter.isChecked()
        elif parameters.datatype == datetime:
            value = self.filter.date()
        elif parameters.datatype == int:
            value = self.filter.value()
        else:
            raise ValueError('Invalid datatype!')

        if filter_option == FilterOption.smaller_equal:
            def filter_callable(x):
                return value <= x
        elif filter_option == FilterOption.smaller:
            def filter_callable(x):
                return value < x
        elif filter_option == FilterOption.larger_equal:
            def filter_callable(x):
                return value >= x
        elif filter_option == FilterOption.larger:
            def filter_callable(x):
                return value > x
        elif filter_option == FilterOption.equal:
            def filter_callable(x):
                return value == x
        elif filter_option == FilterOption.contains:
            def filter_callable(x):
                return value in x
        else:
            raise ValueError('Invalid FilterOption!')

        return dict_key, filter_callable
