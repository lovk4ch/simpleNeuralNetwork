import sys

from PyQt6.QtCore import QSize, QDir, Qt
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog, \
    QVBoxLayout, QSpinBox, QMessageBox, QSpacerItem, QSizePolicy, QFrame
from main import MNIST_reader

MSG_DATASET_IS_NOT_LOADED = "Failed to load dataset. Check the selected file exists and is not empty."
MSG_TRAINING_COMPLETED = "The neural network has been trained on {} records.\nNow please select test dataset."
MSG_QUERY_COMPLETED = "{} records from dataset have been processed.\nAccuracy - {:.2f}%\nNow you can select a record to view its image and processed data."



def set_label_style(element: QFrame, font_size: int, height: int = 0, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter):
    element.setFont(QFont("Astron Boy Video", font_size, QFont.Weight.Bold))
    element.setAlignment(alignment)
    if height != 0:
        element.setFixedHeight(height)
    element.setStyleSheet("color: #ffffff")



# noinspection PyTypeChecker,PyUnresolvedReferences
class MainToolsLayout(QVBoxLayout):
    def __init__(self, callbacks: dict = None):
        super(MainToolsLayout, self).__init__()

        self.button_select_training_dataset = None
        self.spinbox_selection_range = None

        self.setContentsMargins(45, 25, 45, 25)
        self.setSpacing(10)

        self.layout_header = QLabel("MNIST Neural Network")
        set_label_style(self.layout_header, 30, 45, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.layout_header)

        self.add_line(25)

        self.train_dataset_header = QLabel("Train dataset")
        set_label_style(self.train_dataset_header, 24, 36, Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.train_dataset_header)

        self.button_select_training_dataset = QPushButton("Select")
        self.button_select_training_dataset.clicked.connect(callbacks["on_select_training_dataset"])
        self.addWidget(self.button_select_training_dataset)

        self.addSpacing(20)

        self.test_dataset_header = QLabel("Test dataset")
        set_label_style(self.test_dataset_header, 24, 36, Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.test_dataset_header)

        self.button_select_test_dataset = QPushButton("Select")
        self.button_select_test_dataset.clicked.connect(callbacks["on_select_test_dataset"])
        self.button_select_test_dataset.setEnabled(False)
        self.addWidget(self.button_select_test_dataset)

        self.spinbox_selection_range = QSpinBox()
        self.spinbox_selection_range.setEnabled(False)
        self.spinbox_selection_range.valueChanged.connect(lambda value: callbacks["on_update_info"](value))
        self.addWidget(self.spinbox_selection_range)

        self.label_record_info = QLabel()
        set_label_style(self.label_record_info, 24, 0, Qt.AlignmentFlag.AlignLeft)
        self.label_record_info.setWordWrap(True)
        self.addWidget(self.label_record_info)

        self.addStretch()
        self.add_line()

        pass

    def add_line(self, indent: int = 0):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.addWidget(line)

        spacer = QSpacerItem(0, indent, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.addSpacerItem(spacer)

    def enable_gui_for_test_dataset(self):
        self.button_select_test_dataset.setEnabled(True)
        pass

    def enable_gui_for_statistics(self, dataset_size: int):
        self.spinbox_selection_range.setRange(1, dataset_size)
        self.spinbox_selection_range.setEnabled(True)
        pass

    def update_record_info(self, text: str):
        self.label_record_info.setText(text)



# Subclass for the main app window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        callbacks = {
            "on_select_training_dataset": lambda: self.open_file_dialog(self.train),
            "on_select_test_dataset": lambda: self.open_file_dialog(self.query),
            "on_update_info": self.update_view
        }

        self.setWindowTitle("Simple Neural Network GUI")
        self.last_dir = QDir.currentPath()
        self.reader = MNIST_reader()

        # === Left layout ===
        self.main_tools_layout = MainToolsLayout(callbacks)

        # === Right layout ===
        self.graphics_layout = QVBoxLayout()
        self.image_with_digit = None

        # === Main Window Layout ===
        self.main_layout = QHBoxLayout()



        # Create a button and connect it to layout
        self.image_with_digit = QLabel()
        self.image_with_digit.setFixedSize(QSize(500, 500))
        self.image_with_digit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graphics_layout.addWidget(self.image_with_digit)

        self.main_layout.addLayout(self.main_tools_layout)
        self.main_layout.addLayout(self.graphics_layout)

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
        records = 500
        if not self.load_dataset(path, records, 1):
            return

        self.reader.train(1)
        self.show_info_message(MSG_TRAINING_COMPLETED.format(self.reader.get_dataset_size()))
        self.main_tools_layout.enable_gui_for_test_dataset()
        pass

    def query(self, path):
        records = 500
        if not self.load_dataset(path, records, 1):
            return

        self.reader.query()
        self.show_info_message(MSG_QUERY_COMPLETED.format(self.reader.get_dataset_size(), self.reader.get_accuracy()))
        self.main_tools_layout.enable_gui_for_statistics(self.reader.get_dataset_size())
        pass

    def update_view(self, index: int):
        self.set_pixmap(index)
        info_text = self.get_current_record_info(index)
        self.main_tools_layout.update_record_info(info_text)

    def get_current_record_info(self, index: int) -> str:
        label = self.reader.get_record_info(index)
        if label is None:
            return "No record found for the given index."

        return f"Record {index}:\nActual value = {label[1]}\nPredicted value = {label[0]}"

    def set_pixmap(self, index: int):
        if self.reader.get_dataset_size() == 0:
            self.show_error_message(MSG_DATASET_IS_NOT_LOADED)
            return

        pixmap = self.reader.get_plot_as_pixmap(index)
        self.image_with_digit.setPixmap(pixmap)
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
QFontDatabase.addApplicationFont("resources/fonts/astron_boy_video.ttf")

window = MainWindow()
window.show()

app.exec()