import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from main import MNIST_reader

# Subclass for the main app window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Simple Neural Network GUI")
        main_layout = QHBoxLayout()

        reader = MNIST_reader("mnist_dataset/mnist_train_100.csv", "mnist_dataset/mnist_test_10.csv")
        reader.train()
        reader.query()
        pixmap = reader.get_plot_as_pixmap(2)

        # Create a button and connect it to layout
        label = QLabel()
        label.setPixmap(pixmap)
        label.setFixedSize(QSize(500, 500))

        main_layout.addWidget(label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.setFixedSize(QSize(960, 540))

    def the_button_was_clicked(self):
        print("Clicked!")

    def the_button_was_toggled(self, checked):
        print("Toggled!", checked)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()