import time

import numpy as np
import matplotlib.pyplot as plt

from PyQt6.QtGui import QImage, QPixmap
from sympy.polys.polyconfig import query

from utils import *
from simpleNeuralNetwork import NeuralNetwork

input_nodes = 784
hidden_nodes = 100
output_nodes = 10
learning_rate = 0.2

class MNIST_reader:
    def __init__(self):
        self.total_answers = 0
        self.right_answers = 0
        self.data = []
        self.scorecard = []
        self.n = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

        plt.grid(True, linestyle=':', alpha=0.5)

    def get_dataset_size(self):
        return len(self.data)
        pass

    def get_accuracy(self):
        if self.right_answers == 0:
            return 0.0

        return self.right_answers / self.total_answers * 100
        pass

    def get_record_info(self, line_index: int = 0):
        return self.scorecard[line_index] if self.data else None

    def get_image_array(self, line_index: int = 0) -> np.ndarray:
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

    def get_plot_as_pixmap(self, line_index: int = 0) -> QPixmap:
        image_array = self.get_image_array(line_index)

        if image_array is None:
            print(MSG_EMPTY_IMAGE_ARRAY)
            return QPixmap()

        if len(image_array.shape) != 2:
            raise ValueError("Expected 2D grayscale image")

        if image_array.dtype != np.uint8:
            image_array = (255 * image_array / np.max(image_array)).astype(np.uint8)

        image_array = 255 - image_array
        height, width = image_array.shape

        qimage = QImage(
            image_array.data, width, height,
            image_array.strides[0],
            QImage.Format.Format_Grayscale8
        )

        qimage = qimage.copy()
        pixmap = QPixmap.fromImage(qimage)
        return pixmap

    def load_dataset(self, path: str, count: int = 0, start_pos: int = 0):
        self.data = FileUtils.get_data_from_file(path, count, start_pos)

        if not self.data:
            print(MSG_DATASET_IS_NOT_LOADED)
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

        self.scorecard.clear()
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

        self.total_answers += len(scorecard_array)
        self.right_answers += right_answers
        print(f"Efficiency = {self.get_accuracy():.2f}%")
        pass
