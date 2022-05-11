from typing import Optional

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QToolButton, QApplication, QWidget

"""
class CollapseButton : public QToolButton {
public:
  CollapseButton(QWidget *parent) : QToolButton(parent), content_(nullptr) {
    setCheckable(true);
    setStyleSheet("background:none");
    setIconSize(QSize(8, 8));
    setFont(QApplication::font());
    connect(this, &QToolButton::toggled, [=](bool checked) {
      setArrowType(checked ? Qt::ArrowType::DownArrow : Qt::ArrowType::RightArrow);
      content_ != nullptr && checked ? showContent() : hideContent();
    });
  }

  void setText(const QString &text) {
    QToolButton::setText(" " + text);
  }

  void setContent(QWidget *content) {
  }

  void hideContent() {
    animator_.setDirection(QAbstractAnimation::Backward);
    animator_.start();
  }

  void showContent() {
    animator_.setDirection(QAbstractAnimation::Forward);
    animator_.start();
  }
"""


class CollapseButton(QToolButton):
    """
    Based on https://stackoverflow.com/a/68141638
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.animation = None  # type: Optional[QPropertyAnimation]
        self.content = None  # type: Optional[QWidget]
        self.setFont(QApplication.font())
        self.toggled.connect(self.toggle_function)

    def setText(self, text: str) -> None:
        super().setText(" " + text)

    def set_content(self, content: QWidget):
        """
        assert(content != nullptr);
        content_ = content;
        auto animation_ = new QPropertyAnimation(content_, "maximumHeight"); // QObject with auto delete
        animation_->setStartValue(0);
        animation_->setEasingCurve(QEasingCurve::InOutQuad);
        animation_->setDuration(300);
        animation_->setEndValue(content->geometry().height() + 10);
        animator_.addAnimation(animation_);
        if (!isChecked()) {
          content->setMaximumHeight(0);
        }

        :param content: 
        :return: 
        """
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
        """
        setArrowType(checked ? Qt::ArrowType::DownArrow : Qt::ArrowType::RightArrow);
        content_ != nullptr && checked ? showContent() : hideContent();

        :param checked:
        :return:
        """
        self.setArrowType(Qt.DownArrow if checked else Qt.RightArrow)
        if checked:
            self.show_content()
        else:
            self.hide_content()

    def hide_content(self):
        """
        animator_.setDirection(QAbstractAnimation::Backward);
        animator_.start();
        """
        self.animation.setDirection(QAbstractAnimation.Backward)
        self.animation.start()

    def show_content(self):
        """
        animator_.setDirection(QAbstractAnimation::Forward);
        animator_.start();
        """
        self.animation.setDirection(QAbstractAnimation.Forward)
        self.animation.start()
