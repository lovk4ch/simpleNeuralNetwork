import sys

from PyQt5.QtWidgets import QLayout
from PyQt6.QtCore import QSize, QDir, Qt
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap, QColor, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog, \
    QVBoxLayout, QSlider, QSpinBox, QMessageBox, QSpacerItem, QSizePolicy, QFrame

from utils import *
from mnistReader import MnistReader



def set_label_style(element: QFrame, font_size: int, height: int = 0, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter):
    element.setFont(QFont("TT Supermolot Neue Trl Exp", font_size, QFont.Weight.Bold))
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



# noinspection PyTypeChecker,PyUnresolvedReferences
class MainToolsLayout(QVBoxLayout):

    # --- Constructor
    # --- This class represents the main tools layout of the application

    def __init__(self, callbacks: dict = None):
        super(MainToolsLayout, self).__init__()

        self.setContentsMargins(25, 25, 25, 25)
        self.setSpacing(10)

        self.layout_header = QLabel("MNIST Neural Network")
        set_label_style(self.layout_header, 30, 45, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.layout_header)

        self.add_line(25)



        # --- Training dataset section

        self.train_dataset_header = QLabel("Train dataset")
        set_label_style(self.train_dataset_header, 24, 36, Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.train_dataset_header)

        self.layout_training_params = QHBoxLayout()

        self.label_max_records_training = QLabel("Max. records:")
        set_label_style(self.label_max_records_training, 18, 27, Qt.AlignmentFlag.AlignLeft)
        self.layout_training_params.addWidget(self.label_max_records_training)

        self.spinbox_max_records_training = QSpinBox()
        self.spinbox_max_records_training.setRange(0, 10000)
        self.layout_training_params.addWidget(self.spinbox_max_records_training)

        self.button_select_training_dataset = QPushButton("Select")
        self.button_select_training_dataset.setFixedWidth(200)
        self.button_select_training_dataset.clicked.connect(callbacks["on_select_training_dataset"])
        self.layout_training_params.addWidget(self.button_select_training_dataset)

        self.addLayout(self.layout_training_params)

        self.label_training_info = QLabel()
        set_label_style(self.label_training_info, 16, 24, Qt.AlignmentFlag.AlignLeft)
        self.label_training_info.setWordWrap(True)
        self.addWidget(self.label_training_info)

        self.addSpacing(20)
        pass



        # --- Test dataset section

        self.test_dataset_header = QLabel("Test dataset")
        set_label_style(self.test_dataset_header, 24, 36, Qt.AlignmentFlag.AlignLeft)
        self.test_dataset_header.setVisible(False)
        self.addWidget(self.test_dataset_header)

        self.layout_test_params = QHBoxLayout()

        self.label_max_records_test = QLabel("Max. records:")
        set_label_style(self.label_max_records_test, 18, 27, Qt.AlignmentFlag.AlignLeft)
        self.layout_test_params.addWidget(self.label_max_records_test)

        self.spinbox_max_records_test = QSpinBox()
        self.spinbox_max_records_test.setRange(0, 10000)
        self.layout_test_params.addWidget(self.spinbox_max_records_test)

        self.button_select_test_dataset = QPushButton("Select")
        self.button_select_test_dataset.setFixedWidth(200)
        self.button_select_test_dataset.clicked.connect(callbacks["on_select_test_dataset"])
        self.layout_test_params.addWidget(self.button_select_test_dataset)

        set_layout_visible(self.layout_test_params, False)
        self.addLayout(self.layout_test_params)
        pass



        # --- Efficiency section

        self.slider_selection_range = QSlider(Qt.Orientation.Horizontal)
        self.slider_selection_range.setVisible(False)
        self.slider_selection_range.setMinimum(1)
        self.slider_selection_range.setMaximum(1)
        self.slider_selection_range.setSingleStep(1)
        self.slider_selection_range.setTickInterval(1)
        self.slider_selection_range.valueChanged.connect(lambda value: callbacks["on_record_update"](value - 1))
        self.addWidget(self.slider_selection_range)

        self.label_test_info = QLabel()
        set_label_style(self.label_test_info, 16, 24, Qt.AlignmentFlag.AlignCenter)
        self.label_test_info.setWordWrap(True)
        self.addWidget(self.label_test_info)

        self.label_accuracy = QLabel()
        set_label_style(self.label_accuracy, 48, 0, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.label_accuracy)

        self.addStretch()
        self.add_line()
        pass



    # --- Main GUI methods

    def add_line(self, indent: int = 0):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.addWidget(line)

        spacer = QSpacerItem(0, indent, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.addSpacerItem(spacer)
        pass

    def get_max_records_for_training(self):
        return self.spinbox_max_records_training.value()

    def get_max_records_for_test(self):
        return self.spinbox_max_records_test.value()

    def update_training_info(self, text: str):
        self.label_training_info.setText(text)
        pass

    def update_test_info(self, text: str, accuracy: str):
        self.label_test_info.setText(text)
        self.label_accuracy.setText(accuracy)
        pass

    def enable_gui_for_test_dataset(self):
        if not self.test_dataset_header.isVisible():
            self.test_dataset_header.setVisible(True)
            set_layout_visible(self.layout_test_params, True)
        pass

    def enable_gui_for_statistics(self, dataset_size: int):
        self.slider_selection_range.setRange(1, dataset_size)
        self.slider_selection_range.setVisible(True)
        self.slider_selection_range.valueChanged.emit(self.slider_selection_range.value())
        pass



class RecordInfoLayout(QVBoxLayout):
    def __init__(self, callbacks: dict = None):
        super(RecordInfoLayout, self).__init__()

        self.label_record_info = None
        self.image_with_digit = None

        self.setContentsMargins(25, 25, 25, 25)
        self.setSpacing(10)

        self.label_record_info = QLabel()
        set_label_style(self.label_record_info, 24, 0, Qt.AlignmentFlag.AlignLeft)
        self.label_record_info.setWordWrap(True)
        self.addWidget(self.label_record_info)

        self.image_with_digit = QLabel()
        self.image_with_digit.setFixedSize(QSize(344, 344))
        self.image_with_digit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.image_with_digit)

        self.addStretch()

        pass

    # --- Main GUI methods

    def update_record_info(self, text: str):
        self.label_record_info.setText(text)
        pass

    def draw_grid_for_pixmap(self, pixmap: QPixmap, cell_size: int = 10) -> QPixmap:
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

    def set_pixmap(self, pixmap: QPixmap):
        pixmap = pixmap.scaled(344, 344, Qt.AspectRatioMode.KeepAspectRatio)
        pixmap = self.draw_grid_for_pixmap(pixmap, int(344 / 4))
        self.image_with_digit.setPixmap(pixmap)
        pass



# Subclass for the main app window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        callbacks = {
            "on_select_training_dataset": lambda: self.open_file_dialog(self.train),
            "on_select_test_dataset": lambda: self.open_file_dialog(self.query),
            "on_record_update": self.update_record_info,
        }

        self.setWindowTitle("Simple Neural Network for MNIST")
        self.last_dir = QDir.currentPath() + "/mnist_dataset"
        self.reader = MnistReader()

        # === Left layout ===
        self.main_tools_layout = MainToolsLayout(callbacks)

        # === Right layout ===
        self.record_info_layout = RecordInfoLayout(callbacks)

        # === Main Window Layout ===
        self.main_layout = QHBoxLayout()

        self.main_layout.addLayout(self.main_tools_layout)
        self.main_layout.addLayout(self.record_info_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)
        self.setFixedSize(QSize(960, 540))
        self.setStyleSheet("""
            QMainWindow {
                background-image: url("resources/back.jpg");
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
                background-origin: content;
            }
        """)

    def load_dataset(self, path: str, count: int = 0, start_pos: int = 0):
        if self.reader.load_dataset(path, count, start_pos) is False:
            self.show_error_message(MSG_DATASET_IS_NOT_LOADED)
            return False
        return True

    def train(self, path):
        records = self.main_tools_layout.get_max_records_for_training()
        if not self.load_dataset(path, records, 1):
            return

        self.reader.train(1)
        self.show_info_message(MSG_TRAINING_COMPLETED.format(self.reader.get_dataset_size()))
        self.main_tools_layout.enable_gui_for_test_dataset()
        self.update_training_info()
        pass

    def query(self, path):
        records = self.main_tools_layout.get_max_records_for_test()
        if not self.load_dataset(path, records, 1):
            return

        self.reader.query()
        self.show_info_message(MSG_QUERY_COMPLETED.format(self.reader.get_dataset_size(), self.reader.get_accuracy()))
        self.main_tools_layout.enable_gui_for_statistics(self.reader.get_dataset_size())
        self.update_test_info()
        pass

    def update_training_info(self):
        self.main_tools_layout.update_training_info(
            f"Total training data: {self.reader.get_total_trained()}, last dataset: {self.reader.get_dataset_size()}.\n"
        )
        pass

    def update_test_info(self):
        self.main_tools_layout.update_test_info(
            f"Overall net accuracy is:",
            f"{self.reader.get_accuracy():.2f}%"
        )
        pass

    def update_record_info(self, index: int):
        self.set_pixmap(index)
        info_text = self.get_current_record_info(index)
        self.record_info_layout.update_record_info(info_text)
        pass

    def get_current_record_info(self, index: int) -> str:
        label = self.reader.get_record_info(index)
        if label is None:
            return "No record found for the given index."

        return (f"Record {index + 1}:\n"
                f"Actual value = {label[1]}\n"
                f"Network answer = {label[0]}")

    def set_pixmap(self, index: int):
        if self.reader.get_dataset_size() == 0:
            self.show_error_message(MSG_DATASET_IS_NOT_LOADED)
            return

        pixmap = self.reader.get_plot_as_pixmap(index)
        if pixmap.isNull():
            self.show_error_message(MSG_EMPTY_IMAGE_ARRAY)
            return

        self.record_info_layout.set_pixmap(pixmap)
        pass

    def open_file_dialog(self, callback):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select dataset",
            self.last_dir,
            "CSV files (*.csv);;Text files (*.txt);;All files (*.*)"
        )

        if file_path:
            print(f"Selected file: {file_path}")
            from pathlib import Path
            self.last_dir = str(Path(file_path).parent)
            callback(file_path)
        pass

    @staticmethod
    def show_error_message(text: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.exec()
        pass

    @staticmethod
    def show_info_message(text: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Information")
        msg.setText(text)
        msg.exec()
        pass

app = QApplication(sys.argv)
QFontDatabase.addApplicationFont("resources/fonts/TT Supermolot Neue Trial Expanded Regular.ttf")

window = MainWindow()
window.show()

app.exec()