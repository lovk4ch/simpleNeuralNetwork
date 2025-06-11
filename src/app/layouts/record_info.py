from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt6.QtWidgets import QVBoxLayout, QLabel

from src.utils.gui_helpers import *
from src.utils.utils import *


def draw_grid_for_pixmap(pixmap: QPixmap, cell_size: int = 10) -> QPixmap:
    result = QPixmap(pixmap.size())
    result.fill(Qt.GlobalColor.white)

    painter = QPainter(result)
    painter.drawPixmap(0, 0, pixmap)

    pen = QPen(QColor(0, 0, 0, 128))
    pen.setStyle(Qt.PenStyle.DotLine)
    pen.setWidth(1)
    painter.setPen(pen)

    width = pixmap.width()
    height = pixmap.height()

    for y in range(0, height, cell_size):
        painter.drawLine(0, y, width, y)

    for x in range(0, width, cell_size):
        painter.drawLine(x, 0, x, height)

    painter.end()
    return result


class RecordInfoLayout(QVBoxLayout):
    def __init__(self, callbacks: dict = None):
        super(RecordInfoLayout, self).__init__()

        self.label_record_info = None
        self.image_with_digit = None

        self.setContentsMargins(25, 19, 25, 25)
        self.setSpacing(18)

        self.label_record_info = QLabel()
        set_widget_style(self.label_record_info, SIZE_FONT_H2, 0, Qt.AlignmentFlag.AlignLeft)
        self.label_record_info.setWordWrap(True)
        self.addWidget(self.label_record_info)

        self.image_with_digit = QLabel()
        self.image_with_digit.setFixedSize(QSize(IMAGE_WITH_DIGIT_SIZE, IMAGE_WITH_DIGIT_SIZE))
        self.image_with_digit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.image_with_digit)

        self.addStretch()
        pass

    # --- Main GUI methods

    def update_record_info(self, text: str):
        self.label_record_info.setText(text)
        pass

    def set_pixmap(self, pixmap: QPixmap):
        pixmap = pixmap.scaled(IMAGE_WITH_DIGIT_SIZE, IMAGE_WITH_DIGIT_SIZE, Qt.AspectRatioMode.KeepAspectRatio)
        pixmap = draw_grid_for_pixmap(pixmap, int(IMAGE_WITH_DIGIT_SIZE / 4))
        self.image_with_digit.setPixmap(pixmap)
        pass