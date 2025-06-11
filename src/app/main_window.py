from PyQt6.QtCore import QSize, QDir, QTimer, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QFileDialog, \
    QMessageBox

from concurrent.futures import ThreadPoolExecutor
from src.utils.gui_helpers import *
from src.core.mnist_reader import NetMode, MnistReader
from src.app.layouts.main_tools import MainToolsLayout
from src.app.layouts.record_info import RecordInfoLayout


# Subclass for the main app window
# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    on_update_progress = pyqtSignal(int)

    def __init__(self, executor: ThreadPoolExecutor):
        super(MainWindow, self).__init__()

        callbacks = {
            "on_select_training_dataset": lambda: self.open_file_dialog(self.start_train),
            "on_select_test_dataset": lambda: self.open_file_dialog(self.start_query),
            "on_record_update": self.update_record_info,
            "on_progress_update": lambda value: self.update_training_info(value)
        }

        self.setWindowTitle("Simple Neural Network for MNIST")
        self.last_dir = QDir.currentPath() + "/mnist_dataset"
        self.executor = executor
        self.reader = MnistReader()
        self.on_update_progress.connect(callbacks["on_progress_update"])

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

    # --- Main GUI methods

    def update_training_info(self, count: int):
        self.main_tools_layout.update_training_info(
            count / self.reader.get_dataset_size()
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

    # --- Business logic methods

    def load_dataset(self, path: str, count: int = 0, start_pos: int = 0, net_mode: NetMode = NetMode.TRAIN):
        if self.reader.load_dataset(path, count, start_pos, net_mode) is False:
            self.show_error_message(MSG_DATASET_IS_NOT_LOADED)
            return False
        return True

    def train(self, path, on_progress_callback):
        records = self.main_tools_layout.get_max_records_for_training()
        if not self.load_dataset(path, records, 1, NetMode.TRAIN):
            return

        self.reader.train(1, on_progress_callback)
        pass

    def start_train(self, path: str):
        def on_progress_callback(value):
            self.on_update_progress.emit(value)
            pass

        def done_callback(_):
            QTimer.singleShot(0, self.on_finish_train)

        future = self.executor.submit(self.train, path, on_progress_callback)
        future.add_done_callback(done_callback)
        self.main_tools_layout.set_buttons_enabled(False)
        pass

    def on_finish_train(self):
        self.show_info_message(MSG_TRAINING_COMPLETED.format(self.reader.get_dataset_size()))
        self.main_tools_layout.show_gui_for_test_dataset()
        self.main_tools_layout.set_buttons_enabled(True)
        pass

    def query(self, path, on_progress_callback):
        records = self.main_tools_layout.get_max_records_for_test()
        if not self.load_dataset(path, records, 1, NetMode.QUERY):
            return

        self.reader.query()
        pass

    def start_query(self, path: str):
        def on_progress_callback(value):
            self.on_update_progress.emit(value)
            pass

        def done_callback(_):
            QTimer.singleShot(0, self.on_finish_query)

        future = self.executor.submit(self.query, path, on_progress_callback)
        future.add_done_callback(done_callback)
        self.main_tools_layout.set_buttons_enabled(False)
        pass

    def on_finish_query(self):
        self.show_info_message(MSG_QUERY_COMPLETED.format(self.reader.get_dataset_size(NetMode.QUERY), self.reader.get_accuracy()))
        self.main_tools_layout.show_gui_for_statistics(self.reader.get_dataset_size(NetMode.QUERY))
        self.update_test_info()
        self.main_tools_layout.set_buttons_enabled(True)
        pass

    def get_current_record_info(self, index: int) -> str:
        label = self.reader.get_record_info(index)
        if label is None:
            return "No record found for the given index."

        return (f"Record {index + 1}:\n"
                f"Actual value = {label[1]}\n"
                f"Network answer = {label[0]}")
        pass