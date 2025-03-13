<h1> Handwritten Arithmetic Calculator </h1>
A calculator that automatically solves a handwritten arithmetic expression

<h2>Technologies Used</h2>
<ul>
  <li> Convolutional Neural Network created with PyTorch </li>
  <li> OCR segmentation done with CV2 </li>
  <li> Dataset provided by <a href="https://www.kaggle.com/datasets/sagyamthapa/handwritten-math-symbols">Handwritten Math Symbols - Sagyam Thapa</a> </li>
</ul>

<img src="demo_1.gif">

<h2>Features</h2>
<ul>
  <li> Users can write out an expression on a canvas element </li>
  <li> To solve the expression, users can write an equal sign, and the solution will appear next to it </li>
  <li> Users also have the ability to erase and clear the canvas </li>
  <li> Changes to the expression are reflected in real time </li>
</ul>

<h2>How to run</h2>
<ul>
  <li> Run the Flask application using: <pre><code>flask run</code></pre> </li>
  <li> Navigate to http://localhost:5000 in your browser </li>
</ul>

<h2>Future Implementation Goals</h2>
<ul>
  <li> Ability to handle multiple lines of input </li>
</ul>

<h2>Note</h2>
  <li> The current version does not support mobile view </li>
  <li> The answer will not appear next to the equal sign if the window width is smaller than the canvas </li>
  <li> For demonstration purposes, eval() is used to compute the solution, which may result in inaccuracies </li>
