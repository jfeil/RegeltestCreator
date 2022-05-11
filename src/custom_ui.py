from typing import Optional

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QToolButton, QWidget


class CollapseButton(QToolButton):
    """
    Based on https://stackoverflow.com/a/68141638
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.animation = None  # type: Optional[QPropertyAnimation]
        self.content = None  # type: Optional[QWidget]
        self.toggled.connect(self.toggle_function)

    def setText(self, text: str) -> None:
        super().setText(" " + text)

    def set_content(self, content: QWidget):
        self.content = content
        self.animation = QPropertyAnimation(content, b"maximumHeight")
        self.animation.setStartValue(0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setDuration(300)
        self.animation.setEndValue(self.content.sizeHint().height())
        if not self.isChecked():
            content.setMaximumHeight(0)

    def update_animation(self):
        new_end_value = self.content.sizeHint().height()
        self.animation.setEndValue(new_end_value)
        if self.isChecked():
            self.content.setMaximumHeight(new_end_value)

    def toggle_function(self, checked: bool):
        self.setArrowType(Qt.DownArrow if checked else Qt.RightArrow)
        if checked:
            self.show_content()
        else:
            self.hide_content()

    def hide_content(self):
        self.animation.setDirection(QAbstractAnimation.Backward)
        self.animation.start()

    def show_content(self):
        self.animation.setDirection(QAbstractAnimation.Forward)
        self.animation.start()
