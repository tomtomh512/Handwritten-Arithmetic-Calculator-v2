# Handwritten Arithmetic Calculator
A calculator that automatically solves a handwritten arithmetic expression

<img src="demo_1.gif">

## Features

- Users can write out an expression on a canvas element
- To solve the expression, users can write an equal sign, and the solution will appear next to it
- Users also have the ability to erase and clear the canvas
- Changes to the expression are reflected in real time

## Technologies & Implementation

- Convolutional Neural Network created with PyTorch
- OCR segmentation done with CV2
- Dataset provided by [Handwritten Math Symbols - Sagyam Thapa](https://www.kaggle.com/datasets/sagyamthapa/handwritten-math-symbols)


## Local Development

### Train the neural network
To generate the `.pt` model file used for character recognition:
- Open `arithmetic_model.ipynb` in Jupyter Notebook or Google Colab
- Run all cells to train the model
- After training, the `.pt` file will be saved locally

### Run the Flask app
```
flask run
```
