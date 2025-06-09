from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QLayout


def set_label_style(element: QFrame, font_size: int, height: int = 0, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter):
    element.setFont(QFont("TT Supermolot Neue Trl Db", font_size, QFont.Weight.Bold))
    element.setAlignment(alignment)
    if height != 0:
        element.setFixedHeight(height)
    element.setStyleSheet("color: #ffffff")
    pass

def set_layout_visible(layout: QLayout, visible: bool):
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if widget is not None:
            widget.setVisible(visible)
    pass