from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLayout, QProgressBar


# --- Messages for the GUI

MSG_EMPTY_IMAGE_ARRAY = "Image array is empty or not loaded."
MSG_DATASET_IS_NOT_LOADED = "Failed to load dataset. Check the selected file exists and is not empty."
MSG_TRAINING_COMPLETED = "The neural network has been trained on {} records.\nNow please select test dataset."
MSG_UNKNOWN_NET_MODE = "Unknown net mode. Please select TRAIN or QUERY mode."
MSG_QUERY_COMPLETED = "{} records from dataset have been processed.\nAccuracy - {:.2f}%\nNow you can select a record to view its image and processed data."

# --- Constants for the GUI

SIZE_FONT_HEADER = 36
SIZE_FONT_H2 = 24
SIZE_FONT_H3 = 18
SIZE_FONT_PROGRESS = 10
SIZE_FONT_ACCURACY = 54
IMAGE_WITH_DIGIT_SIZE = 345


def set_progress_bar_style(element: QProgressBar, font_size: int, height: int = 0, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter):
    element.setFont(QFont("TT Supermolot Neue Trl Db", font_size, QFont.Weight.Bold))
    element.setAlignment(alignment)
    if height != 0:
        element.setFixedHeight(height)
    element.setStyleSheet("""
        QProgressBar {
            background-color: #7f7f7f;
            border: solid #ffffff;
            color: white;
        }
        
        QProgressBar::chunk {
            width: 1px;
            background-color: #00ff88;
        }
        """)
    pass

def set_widget_style(element: QWidget, font_size: int, height: int = 0, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter):
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