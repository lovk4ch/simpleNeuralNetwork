import time

import numpy as np
import matplotlib.pyplot as plt

from enum import Enum
from PyQt6.QtGui import QImage, QPixmap
from sympy.polys.polyconfig import query

from src.utils.utils import *
from src.core.simple_neural_network import NeuralNetwork



class NetMode(Enum):
    TRAIN = 0
    QUERY = 1

input_nodes = 784
hidden_nodes = 100
output_nodes = 10
learning_rate = 0.2

class MnistReader:
    def __init__(self):
        self.total_trained = 0
        self.total_answers = 0
        self.right_answers = 0
        self.train_data = []
        self.query_data = []
        self.scorecard = []
        self.net_mode = NetMode.TRAIN
        self.n = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

        plt.grid(True, linestyle=':', alpha=0.5)
        pass

    def get_dataset_size(self):
        match self.net_mode.value:
            case NetMode.TRAIN.value:
                return len(self.train_data)
            case NetMode.QUERY.value:
                return len(self.query_data)
            case _:
                print(MSG_UNKNOWN_NET_MODE)
                return 0

    def get_accuracy(self):
        if self.right_answers == 0:
            return 0.0

        return self.right_answers / self.total_answers * 100

    def get_total_trained(self):
        return self.total_trained

    def get_total_answers(self):
        return self.total_answers

    def get_record_info(self, line_index: int = 0):
        return self.scorecard[line_index] if self.query_data else None

    def get_image_array(self, line_index: int = 0) -> np.ndarray:
        try:
            if self.query_data is None:
                raise IndexError("Data not loaded")

            if len(self.query_data) <= line_index:
                raise ValueError("Line does not exist or index out of range")

            # remove extra spaces and newlines
            line = self.query_data[line_index].strip()

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

    def train(self, epochs: int = 1, callback = None):
        print("Train started with epochs:", epochs)
        init_time = time.perf_counter()
        step_time = init_time
        count = 0

        for e in range(epochs):
            for record in self.train_data:
                all_values = record.split(",")
                inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01

                # output with 10 digits
                targets = np.zeros(output_nodes) + 0.01

                # set marker for the correct digit
                targets[int(all_values[0])] = 0.99

                self.n.train(inputs, targets)

                count += 1
                if (time.perf_counter() - step_time) > 0.03:
                    callback(count) if callback else None
                    step_time = time.perf_counter()
            pass

        callback(count) if callback else None

        self.total_trained += len(self.train_data) * epochs
        print(f"Time for train: {time.perf_counter() - init_time:.2f} sec")
        print(f"Total training data: {self.get_total_trained()}, last dataset: {self.get_dataset_size()}.\n")

        # self.train_data.clear()

    def query(self, callback = None):
        print("Query started")
        init_time = time.perf_counter()
        step_time = init_time
        count = 0

        self.scorecard.clear()
        for record in self.query_data:
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

            count += 1
            if (time.perf_counter() - step_time) > 0.03:
                callback(count) if callback else None
                step_time = time.perf_counter()
            pass

        callback(count) if callback else None

        print(f"Time for query: {time.perf_counter() - init_time:.2f} sec")
        scorecard_array = np.asarray(self.scorecard)
        right_answers = sum(1 for i in scorecard_array if i[0] == i[1])
        print(f"Right answers: {right_answers}")

        self.total_answers += len(scorecard_array)
        self.right_answers += right_answers
        print(f"Efficiency = {self.get_accuracy():.2f}%")
        pass

    def load_dataset(self, path: str, count: int = 0, start_pos: int = 0, net_mode: NetMode = NetMode.TRAIN):
        data = get_data_from_file(path, count, start_pos)

        if not data:
            print(MSG_DATASET_IS_NOT_LOADED)
            return False

        self.net_mode = net_mode
        match self.net_mode.value:
            case NetMode.TRAIN.value:
                self.train_data = data
            case NetMode.QUERY.value:
                self.query_data = data
            case _:
                print(MSG_UNKNOWN_NET_MODE)
                return False

        print(f"Dataset loaded with {len(data)} records")
        return True