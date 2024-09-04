import cv2
import numpy as np
from skimage.morphology import skeletonize
from model import process_image
from PIL import Image


def parse(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    threshold, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    thinned_image = skeletonize(binary_image / 255)

    vertical_projection = np.sum(thinned_image, axis=0)
    horizontal_projection = np.sum(thinned_image, axis=1)

    vertical_bounds = []
    in_character = False
    start = 0

    for i, value in enumerate(vertical_projection):
        # when encountering character, log start and set in_character to true
        if value > 0 and not in_character:
            start = i
            in_character = True

        # when leaving character, log end and set in_character to false
        elif value <= 0 and in_character:
            vertical_bounds.append((start, i))
            in_character = False

    # if the character continues until the end
    if in_character:
        vertical_bounds.append((start, len(vertical_projection)))

    horizontal_bounds = []
    in_character = False
    start = 0

    for i, value in enumerate(horizontal_projection):
        # when encountering character, log start and set in_character to true
        if value > 0 and not in_character:
            start = i
            in_character = True

        # when leaving character, log end and set in_character to false
        elif value <= 0 and in_character:
            horizontal_bounds.append((start, i))
            in_character = False

    # if the character continues until the end
    if in_character:
        horizontal_bounds.append((start, len(horizontal_projection)))

    bottom = horizontal_bounds[0][0]
    top = horizontal_bounds[0][1]

    expression_string = ""

    for i, (left, right) in enumerate(vertical_bounds):
        # crop out the character image
        char_image = image[bottom:top, left:right]

        # calculate padding to square image
        height, width = char_image.shape

        if height > width:
            top_padding = 0
            bottom_padding = 0
            left_padding = right_padding = (height - width) // 2
        else:
            left_padding = 0
            right_padding = 0
            top_padding = bottom_padding = (width - height) // 2

        squared_image = cv2.copyMakeBorder(char_image, top_padding, bottom_padding, left_padding, right_padding,
                                           cv2.BORDER_CONSTANT, value=255)
        pil_image = Image.fromarray(squared_image)
        expression_string += process_image(pil_image)

    return expression_string


# print(parse("test_images/equation.png"))
