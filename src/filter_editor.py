from datetime import datetime
from typing import Dict, Tuple, Callable, Union, Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLineEdit, QCheckBox, QDateEdit, QSpinBox, QPushButton, QDialogButtonBox

from src.datatypes import QuestionParameters, FilterOption
from src.ui_filter_editor import Ui_FilterEditor


class FilterEditor(QDialog, Ui_FilterEditor):
    def __init__(self, filter_configuration: Dict[str, QuestionParameters],
                 current_filter: Union[None, Tuple[str, FilterOption, Any]] = None,
                 # dict_key, FilterOption, filter_data
                 parent=None, window_flags=Qt.Dialog):
        super(FilterEditor, self).__init__(parent, window_flags)
        self.ui = Ui_FilterEditor()
        self.ui.setupUi(self)

        self.ui.buttonBox.clicked.connect(self.__handle_buttonbox)

        self.filter = None

        self.filter_configuration = filter_configuration

        self.ui.combobox_column.addItems(
            [filterparams.table_header for filterparams in self.filter_configuration.values()])

        self.ui.combobox_column.currentIndexChanged.connect(self.__update_filteroptions)

        if current_filter:
            self.setWindowTitle("Filter bearbeiten")
            dict_key, filter_option, filter_value = current_filter
            index = list(self.filter_configuration).index(dict_key)
            self.ui.combobox_column.setCurrentIndex(index)
            index = self.filter_configuration[dict_key].filter_options.index(filter_option)
            self.ui.combobox_filteroption.setCurrentIndex(index)
            self.__set_filter_data(filter_value)
        else:
            self.setWindowTitle("Filter erstellen")
            self.__update_filteroptions(self.ui.combobox_column.currentIndex())

    def __handle_buttonbox(self, button: QPushButton):
        button_role = self.ui.buttonBox.buttonRole(button)
        if button_role == QDialogButtonBox.ButtonRole.DestructiveRole:
            self.reject()
        elif button_role == QDialogButtonBox.ButtonRole.AcceptRole:
            self.accept()

    def __set_filter_data(self, data) -> None:
        _, parameters, _ = self.__current_selection_state()

        if parameters.datatype == str:
            self.filter.setText(data)
        elif parameters.datatype == bool:
            self.filter.setCheckState(data * 2)
        elif parameters.datatype == datetime:
            self.filter.setDate(data)
        elif parameters.datatype == int:
            self.filter.setValue(data)
        else:
            raise ValueError('Invalid datatype!')

    def __get_filter_data(self) -> Any:
        _, parameters, _ = self.__current_selection_state()

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

        return value

    def __update_filteroptions(self, index):
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
            raise ValueError('Invalid FilterOption!')

        self.ui.gridLayout.addWidget(self.filter, 2, 1, 1, 1)

    def __current_selection_state(self):
        index = self.ui.combobox_column.currentIndex()
        dict_key, parameters = list(self.filter_configuration.items())[index]
        filter_option = parameters.filter_options[self.ui.combobox_filteroption.currentIndex()]

        return dict_key, parameters, filter_option

    def current_configuration(self) -> Tuple[str, FilterOption, Any]:
        dict_key, _, filter_option = self.__current_selection_state()
        return dict_key, filter_option, self.__get_filter_data()

    def create_filter(self) -> Tuple[str, Callable]:
        # ('answer_text', lambda x: 'FaD' in x)
        dict_key, parameters, filter_option = self.__current_selection_state()

        value = self.__get_filter_data()

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
