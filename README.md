# <p align="center">MNIST Neural Network Demo with GUI</p>

![MNIST GUI Demo](resources/example.jpg)

> A simple Python demo project with a GUI for handwritten digit recognition ([MNIST](https://www.kaggle.com/datasets/hojjatk/mnist-dataset) dataset), with training and visualization of results

---

## 🛠 Stack:

Python, PyQt6, NumPy, multithreading (ThreadPoolExecutor), MVC, custom neural network engine.

---

## 🧩 Features

- Visual interface on PyQt6
- Training the neural network on the MNIST training dataset
- Testing and displaying recognition accuracy
- Viewing individual images and predictions
- Separate threads for analysis and training (`ThreadPoolExecutor`)

---

## ⚡️ Quick start

```bash
# 1. Clone the project
git clone https://github.com/lovk4ch/simpleNeuralNetwork.git
cd simpleNeuralNetwork

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python -m src.main
```

---

## 🚄 Further update plan:

- Number of epochs for training in GUI
- Graphs of the dependence of the training efficiency on the number
- Setting the number of layers, number of neurons, activation type (ReLU, tanh, sigmoid)
- Possibility to draw your own numbers
- Loss/accuracy graph by epochs
- Possibility to save and load the trained model
