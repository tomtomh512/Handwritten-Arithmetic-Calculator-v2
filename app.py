from flask import Flask, render_template, jsonify, request
from ocr import parse
from PIL import Image
from io import BytesIO
import tempfile
import base64
import re
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/upload', methods=['POST'])
# def upload():
#     image_base64 = request.get_json().get('imageBase64', '')
#
#     # Clean base64 string
#     image_data = re.sub('^data:image/.+;base64,', '', image_base64)
#     # Decode and open image
#     image = Image.open(BytesIO(base64.b64decode(image_data)))
#
#     # Save as temporary, must be PNG don't know why
#     with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
#         image_path = temp_file.name
#         image.save(image_path)
#
#     result = process_image(image_path)
#
#     # Remove
#     os.remove(image_path)
#
#     return jsonify({"output": result}), 200


if __name__ == '__main__':
    app.run()