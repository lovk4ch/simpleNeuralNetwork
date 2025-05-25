import sys

from PyQt5.QtWidgets import QSpinBox
from PyQt6.QtCore import QSize, QDir, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton, QFileDialog, \
    QVBoxLayout, QSpinBox, QMessageBox
from main import MNIST_reader

# Subclass for the main app window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Simple Neural Network GUI")
        self.last_dir = QDir.currentPath()
        self.reader = MNIST_reader()

        self.right_layout = QVBoxLayout()
        self.left_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()

        self.button_select_file = QPushButton("Select train dataset")
        self.spinbox_dataset_selected = QSpinBox()
        self.image_with_digit = None



        # === Left layout ===

        self.button_select_file.clicked.connect(lambda: self.open_file_dialog(self.perform_data))
        self.left_layout.addWidget(self.button_select_file)

        self.spinbox_dataset_selected.setEnabled(False)
        self.spinbox_dataset_selected.valueChanged.connect(lambda value: self.set_pixmap())
        self.left_layout.addWidget(self.spinbox_dataset_selected)



        # === Right layout ===

        # Create a button and connect it to layout
        self.image_with_digit = QLabel()
        self.image_with_digit.setFixedSize(QSize(500, 500))
        self.image_with_digit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(self.image_with_digit)



        # === Main layout ===

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)
        self.setFixedSize(QSize(960, 540))
        pass

    def load_dataset(self, path: str, count: int = 0, start_pos: int = 0):
        if self.reader.load_dataset(path, count, start_pos) is False:
            self.show_error_message("Failed to load dataset. Check the selected file exists and is not empty.")
            return False
        return True

    def perform_data(self, path):
        if not self.load_dataset(path, 500, 1):
            return

        self.reader.train(1)
        self.spinbox_dataset_selected.setEnabled(True)
        self.spinbox_dataset_selected.setRange(1, self.reader.get_dataset_size())
        self.set_pixmap()
        pass

    def set_pixmap(self):
        pixmap = self.reader.get_plot_as_pixmap(self.spinbox_dataset_selected.value() - 1)
        self.image_with_digit.setPixmap(pixmap)
        pass

    def open_file_dialog(self, callback):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select file",
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

window = MainWindow()
window.show()

app.exec()