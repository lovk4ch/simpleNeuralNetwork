import time

import matplotlib.pyplot as plt
import numpy as np

from itertools import islice
from io import BytesIO
from PyQt6.QtGui import QImage, QPixmap
from sympy.polys.polyconfig import query

from simpleNeuralNetwork import NeuralNetwork

input_nodes = 784
hidden_nodes = 100
output_nodes = 10
learning_rate = 0.2

class MNIST_reader:
    def __init__(self, csv_train: str, csv_test: str):
        self.csv_train = csv_train
        self.csv_test = csv_test
        self.accuracy = 0.0
        self.data = None
        self.scorecard = []
        self.n = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    def get_data_from_file(self, path: str, n: int = None, start_line: int = 0):
        with open(path, "r") as file:
            lines = list(islice(file, start_line, n))
            print("Read", len(lines), "lines from " + path)
        return lines

    def get_image(self, line_index: int = 5):
        input_image = np.asfarray(self.data[line_index].strip().split(",")[1:]).reshape(28, 28)
        return input_image

    def get_plot_as_pixmap(self, line_index: int = 0):
        image_array = self.get_image(line_index)
        plt.title("Input image", fontname='Brush Script MT', fontsize=30,
            fontweight="light", color="black", loc="center", pad=15)
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.imshow(image_array, cmap='Greys', interpolation='None')

        # Save the plot to a BytesIO object
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.15)
        buf.seek(0)

        # Create QImage from the BytesIO object
        qimage = QImage.fromData(buf.getvalue())

        # Convert QImage to QPixmap
        pixmap = QPixmap.fromImage(qimage)

        return pixmap

    def train(self, epochs: int = 1):
        self.data = self.get_data_from_file(self.csv_train, n=10000, start_line=1)
        print("Train started with epochs:", epochs)
        init_time = time.perf_counter()

        for e in range(epochs):
            for record in self.data[1:]:
                all_values = record.split(",")
                inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
                
                # output with 10 digits
                targets = np.zeros(output_nodes) + 0.01
                
                # set marker for the correct digit
                targets[int(all_values[0])] = 0.99
                
                self.n.train(inputs, targets)
            pass

        print(f"Time for train: {time.perf_counter() - init_time:.2f} sec")

    def query(self):
        self.data = self.get_data_from_file(self.csv_test)
        print("Query started")
        init_time = time.perf_counter()

        for record in self.data[1:]:
            query(record)
            all_values = record.split(",")

            # first value is the label
            correct_label = int(all_values[0])

            # normalize the rest of the values
            inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01

            # query the result from the neural network
            outputs = self.n.query(inputs)

            # get the label with the highest value
            label = np.argmax(outputs)

            self.scorecard.append([label, correct_label])
            pass

        print(f"Time for query: {time.perf_counter() - init_time:.2f} sec")
        print(self.scorecard)
        scorecard_array = np.asarray(self.scorecard)
        self.accuracy = sum(1 for i in scorecard_array if i[0] == i[1]) / len(scorecard_array) * 100
        print(f"Efficiency = {self.accuracy:.2f}%")
        pass