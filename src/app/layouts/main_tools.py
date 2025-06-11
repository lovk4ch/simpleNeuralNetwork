from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSpinBox, QPushButton, QSpacerItem, QSizePolicy, QSlider, QFrame

from src.app.widgets.glitch_label import *
from src.utils.gui_helpers import *


class MainToolsLayout(QVBoxLayout):

    # --- Constructor
    # --- This class represents the main tools layout of the application

    def __init__(self, callbacks: dict = None):
        super(MainToolsLayout, self).__init__()

        self.setContentsMargins(25, 15, 25, 25)
        self.setSpacing(10)

        self.layout_header = QGlitchLabel("MNIST Neural Network")
        set_widget_style(self.layout_header, SIZE_FONT_HEADER, int(SIZE_FONT_HEADER * 1.5), Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.layout_header)

        self.add_line(25)

        # --- Training dataset section

        self.train_dataset_header = QLabel("Train dataset")
        set_widget_style(self.train_dataset_header, SIZE_FONT_H2, int(SIZE_FONT_H2 * 1.5), Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.train_dataset_header)

        self.layout_training_params = QHBoxLayout()

        self.label_max_records_training = QLabel("Max. records:")
        set_widget_style(self.label_max_records_training, SIZE_FONT_H3, int(SIZE_FONT_H3 * 1.5), Qt.AlignmentFlag.AlignLeft)
        self.layout_training_params.addWidget(self.label_max_records_training)

        self.spinbox_max_records_training = QSpinBox()
        self.spinbox_max_records_training.setRange(0, 1000000)
        self.layout_training_params.addWidget(self.spinbox_max_records_training)

        self.button_select_training_dataset = QPushButton("Select")
        self.button_select_training_dataset.setFixedWidth(200)
        self.button_select_training_dataset.clicked.connect(callbacks["on_select_training_dataset"])
        self.layout_training_params.addWidget(self.button_select_training_dataset)

        self.addLayout(self.layout_training_params)

        self.addSpacing(20)

        # --- Test dataset section

        self.test_dataset_header = QLabel("Test dataset")
        set_widget_style(self.test_dataset_header, SIZE_FONT_H2, int(SIZE_FONT_H2 * 1.5), Qt.AlignmentFlag.AlignLeft)
        self.test_dataset_header.setVisible(False)
        self.addWidget(self.test_dataset_header)

        self.layout_test_params = QHBoxLayout()

        self.label_max_records_test = QLabel("Max. records:")
        set_widget_style(self.label_max_records_test, SIZE_FONT_H3, int(SIZE_FONT_H3 * 1.5), Qt.AlignmentFlag.AlignLeft)
        self.layout_test_params.addWidget(self.label_max_records_test)

        self.spinbox_max_records_test = QSpinBox()
        self.spinbox_max_records_test.setRange(0, 1000000)
        self.layout_test_params.addWidget(self.spinbox_max_records_test)

        self.button_select_test_dataset = QPushButton("Select")
        self.button_select_test_dataset.setFixedWidth(200)
        self.button_select_test_dataset.clicked.connect(callbacks["on_select_test_dataset"])
        self.layout_test_params.addWidget(self.button_select_test_dataset)

        set_layout_visible(self.layout_test_params, False)
        self.addLayout(self.layout_test_params)

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
        set_widget_style(self.label_test_info, SIZE_FONT_H3, int(SIZE_FONT_H3 * 1.5), Qt.AlignmentFlag.AlignCenter)
        self.label_test_info.setWordWrap(True)
        self.addWidget(self.label_test_info)

        self.label_accuracy = QLabel()
        set_widget_style(self.label_accuracy, SIZE_FONT_ACCURACY, 0, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.label_accuracy)

        self.addStretch()
        self.add_line()

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

    def set_buttons_enabled(self, enabled: bool):
        self.button_select_training_dataset.setEnabled(enabled)
        self.button_select_test_dataset.setEnabled(enabled)
        pass

    def update_test_info(self, text: str, accuracy: str):
        self.label_test_info.setText(text)
        self.label_accuracy.setText(accuracy)
        pass

    def show_gui_for_test_dataset(self):
        if not self.test_dataset_header.isVisible():
            self.test_dataset_header.setVisible(True)
            set_layout_visible(self.layout_test_params, True)
        pass

    def show_gui_for_statistics(self, dataset_size: int):
        self.slider_selection_range.setRange(1, dataset_size)
        self.slider_selection_range.setVisible(True)
        self.slider_selection_range.valueChanged.emit(self.slider_selection_range.value())
        pass