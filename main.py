import time

import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO
from PyQt6.QtGui import QImage, QPixmap
from sympy.polys.polyconfig import query

from fileUtils import FileUtils
from simpleNeuralNetwork import NeuralNetwork

input_nodes = 784
hidden_nodes = 100
output_nodes = 10
learning_rate = 0.2

class MNIST_reader:
    def __init__(self):
        self.accuracy = 0.0
        self.data = []
        self.scorecard = []
        self.n = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    def get_dataset_size(self):
        return len(self.data)
        pass

    def get_image(self, line_index: int = 0):
        try:
            if self.data is None:
                raise IndexError("Data not loaded")

            if len(self.data) <= line_index:
                raise ValueError("Line does not exist or index out of range")

            # remove extra spaces and newlines
            line = self.data[line_index].strip()

            # skip the first value (label)
            parts = line.split(",")[1:]
            if len(parts) != input_nodes:
                raise ValueError(f"Expected 784 values, got {len(parts)}.")

            input_image = np.asfarray(parts).reshape((28, 28))
            return input_image

        except Exception as e:
            raise ValueError(f"An error occurred while processing the data for image: {e}")

    def get_plot_as_pixmap(self, line_index: int = 0):
        image_array = self.get_image(line_index)
        if image_array is None:
            print("Data not loaded or image array is None.")
            return QPixmap()

        plt.title(f"Input dataset, #{line_index + 1}", fontname='Brush Script MT',
            fontsize=30, fontweight="light", color="black", loc="center", pad=15)
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

    def load_dataset(self, path: str, count: int = 0, start_pos: int = 0):
        self.data = FileUtils.get_data_from_file(path, count, start_pos)

        if not self.data:
            print("No data loaded. Please check the file path and parameters.")
            return False

        print(f"Dataset loaded with {len(self.data)} records")
        return True

    def train(self, epochs: int = 1):
        print("Train started with epochs:", epochs)
        init_time = time.perf_counter()

        for e in range(epochs):
            for record in self.data:
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
        print("Query started")
        init_time = time.perf_counter()

        for record in self.data:
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
        scorecard_array = np.asarray(self.scorecard)
        right_answers = sum(1 for i in scorecard_array if i[0] == i[1])
        print(f"Right answers: {right_answers}")
        print(f"Efficiency = {right_answers / len(scorecard_array) * 100:.2f}%")
        pass
