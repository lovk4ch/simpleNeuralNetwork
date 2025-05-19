import numpy as np
import scipy.special as ssp
import matplotlib.pyplot as plt
from io import BytesIO
from PyQt6.QtGui import QImage, QPixmap

class NeuralNetwork:
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        
        self.wih = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))
        
        # коэффициент обучения
        self.lr = learningrate
        
        # использование сигмоиды в качестве функции активации
        self.activation_function = lambda x: ssp.expit(x)
        pass
    
    def train(self, inputs_list, targets_list):
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T
        
        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        
        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        
        output_errors = targets - final_outputs
        hidden_errors = np.dot(self.who.T, output_errors)
        
        self.who += self.lr * np.dot(output_errors * final_outputs * (1 - final_outputs), np.transpose(hidden_outputs))
        self.wih += self.lr * np.dot(hidden_errors * hidden_outputs * (1 - hidden_outputs), np.transpose(inputs))
        pass
    
    def query(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T
        
        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        
        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        
        return final_outputs

class MNIST_reader:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.data = self.get_data_from_csv()

    def get_data_from_csv(self):
        with open(self.csv_path, "r") as file:
            csv_array = file.readlines()
        return csv_array

    def get_image(self, line_index: int = 5):
        image_array = np.asfarray(self.data[line_index].strip().split(",")[1:]).reshape(28, 28)
        return image_array

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

input_nodes = 784
hidden_nodes = 100
output_nodes = 10
learning_rate = 0.2

n = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

'''
training_data_file = open("mnist_dataset/mnist_train.csv", "r")
training_data_list = training_data_file.readlines()
training_data_file.close()

epochs = 3
for e in range(epochs):
    for record in training_data_list[1:]:
        all_values = record.split(",")
        inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        targets = np.zeros(output_nodes) + 0.01
        targets[int(all_values[0])] = 0.99
        n.train(inputs, targets)
    pass

test_data_file = open("mnist_dataset/mnist_test.csv", "r")
test_data_list = test_data_file.readlines()
test_data_file.close()

scorecard = []

for record in test_data_list[1:]:
    all_values = record.split(",")
    correct_label = int(all_values[0])
    inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
    outputs = n.query(inputs)
    label = np.argmax(outputs)
    scorecard.append(int(label == correct_label))
    pass

print(scorecard)
scorecard_array = np.asarray(scorecard)
print("Эффективность = ", scorecard_array.sum() / scorecard_array.size)
'''