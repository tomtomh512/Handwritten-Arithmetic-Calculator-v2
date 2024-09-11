import cv2
import numpy as np
from skimage.morphology import skeletonize
from model import process_image
from PIL import Image


def find_character(image, bottom, top, left, right):
    # Crop out the character image
    side_grab = 10  # grabs extra space from sides of character
    char_image = image[bottom-side_grab:top+side_grab, left-side_grab:right+side_grab]

    # Calculate padding to square image
    height, width = char_image.shape

    if height > width:
        top_padding = bottom_padding = 0
        left_padding = right_padding = (height - width) // 2
    else:
        left_padding = right_padding = 0
        top_padding = bottom_padding = (width - height) // 2

    squared_image = cv2.copyMakeBorder(char_image, top_padding, bottom_padding, left_padding, right_padding,
                                       cv2.BORDER_CONSTANT, value=255)

    pil_image = Image.fromarray(squared_image)
    return process_image(pil_image)


def get_bounds(projection):
    bounds = []
    in_character = False
    start = 0

    for i, value in enumerate(projection):
        # When encountering character, log start and set in_character to true
        if value > 0 and not in_character:
            start = i
            in_character = True

        # When leaving character, log end and set in_character to false
        elif value <= 0 and in_character:
            bounds.append((start, i))
            in_character = False

    # If the character continues until the end
    if in_character:
        bounds.append((start, len(projection)))

    return bounds


def parse(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Add padding to accommodate side_grab in find_character
    image = cv2.copyMakeBorder(image, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
    # Binary image
    threshold, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    # Thinning
    thinned_image = skeletonize(binary_image / 255)

    # Projections
    vertical_projection = np.sum(thinned_image, axis=0)
    horizontal_projection = np.sum(thinned_image, axis=1)

    # Bounds
    vertical_bounds = get_bounds(vertical_projection)
    horizontal_bounds = get_bounds(horizontal_projection)

    # These are inverted
    bottom = horizontal_bounds[0][0]
    top = horizontal_bounds[0][1]

    for bound in horizontal_bounds:
        bottom = min(bottom, bound[0])
        top = max(top, bound[1])

    # If there is an equal sign, continue
    expression_string = ""
    for (left, right) in vertical_bounds:
        expression_string += find_character(image, bottom, top, left, right)

    return {"expressionString": expression_string, "x": vertical_bounds[len(vertical_bounds) - 1][1], "y1": bottom, "y2": top}
