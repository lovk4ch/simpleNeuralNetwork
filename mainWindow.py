import sys

from PyQt6.QtCore import QSize, QDir, Qt
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog, \
    QVBoxLayout, QSpinBox, QMessageBox, QSpacerItem, QSizePolicy, QFrame
from main import MNIST_reader



def set_label_style(element: QFrame, font_size: int, height: int, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter):
    element.setFont(QFont("Astron Boy Video", font_size, QFont.Weight.Bold))
    element.setAlignment(alignment)
    element.setFixedHeight(height)
    element.setStyleSheet("color: #ffffff")


# noinspection PyTypeChecker
class MainToolsLayout(QVBoxLayout):
    def __init__(self, callbacks: dict = None):
        super(MainToolsLayout, self).__init__()

        self.button_select_file = None
        self.spinbox_selection_range = None

        self.setContentsMargins(45, 15, 45, 15)
        self.setSpacing(5)

        self.layout_header = QLabel("MNIST Neural Network")
        set_label_style(self.layout_header, 30, 45, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.layout_header)

        self.add_line(300)

        self.train_dataset_header = QLabel("Train dataset")
        set_label_style(self.train_dataset_header, 24, 36, Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.train_dataset_header)

        self.button_select_file = QPushButton("Select")
        self.button_select_file.clicked.connect(callbacks["on_select_file"])
        self.addWidget(self.button_select_file)

        self.spinbox_selection_range = QSpinBox()
        self.spinbox_selection_range.setEnabled(False)
        self.spinbox_selection_range.valueChanged.connect(callbacks["on_change_selected_value"])
        self.addWidget(self.spinbox_selection_range)

        # self.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        pass

    def add_line(self, indent: int = 0):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.addWidget(line)

        spacer = QSpacerItem(0, indent, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.addSpacerItem(spacer)

    def set_spinbox_selection_range(self, min_value: int, max_value: int):
        self.spinbox_selection_range.setRange(min_value, max_value)
        self.spinbox_selection_range.setEnabled(True)
        pass

# Subclass for the main app window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        callbacks = {
            "on_select_file": lambda: self.open_file_dialog(self.perform_data),
            "on_change_selected_value": self.set_pixmap,
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
            self.show_error_message("Failed to load dataset. Check the selected file exists and is not empty.")
            return False
        return True

    def perform_data(self, path):
        if not self.load_dataset(path, 500, 1):
            return

        self.reader.train(1)
        self.main_tools_layout.set_spinbox_selection_range(1, self.reader.get_dataset_size())
        self.set_pixmap()
        pass

    def set_pixmap(self):
        pixmap = self.reader.get_plot_as_pixmap(self.main_tools_layout.spinbox_selection_range.value() - 1)
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

app = QApplication(sys.argv)
QFontDatabase.addApplicationFont("resources/fonts/astron_boy_video.ttf")

window = MainWindow()
window.show()

app.exec()