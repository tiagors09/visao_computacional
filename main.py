import select

import cv2
import numpy as np
from cv2.typing import NumPyArrayNumeric

type Img = cv2.Mat | NumPyArrayNumeric | None

WHITE: list[int] = [255, 255, 255]
BLACK: list[int] = [0, 0, 0]

def show_and_print_image_channels(image: Img) -> None:
    """
    Displays an image and prints the BGR channel values of each pixel.

    Iterates over the image matrix and prints the Blue, Green, and Red
    values for every pixel.

    Args:
        image (cv2.Mat | NumPyArrayNumeric | None): Image loaded via OpenCV.

    Returns:
        None
    """

    # verify if image is not none
    if image is not None:
        cv2.imshow('image', image)
        cv2.waitKey(0)

        # run column by row
        # height, widht, chanels = image.shape
        for col in range(0, image.shape[0]):
            for row in range(0, image.shape[1]):
                for value in range(0, 3):
                    # show B, R or G value (channel)
                    print(image[col][row][value])
    else:
        raise Exception('image is invalid')

def invert_image(image: Img) -> Img:
    """
    Invert image color.

    Subtract value of each channel of 255
    finding inverted color.

    Args:
        image (Img): Image loaded via OpenCV to invert
    
    Returns:
        inverted_image (Img): Inverted image
    """
    if image is not None:
        return 255 - image

def invert_half_image(image: Img) -> Img:
    if image is None:
        raise Exception('image is invalid')

    width = image.shape[1]
    half_width = width // 2

    left = image[:, :half_width]
    right = image[:, half_width:]

    inverted_right = 255 - right

    result = np.concatenate((left, inverted_right), axis=1)

    return result

def blocks(image: Img, block_size: int = 20, is_invert: bool = False) -> Img:
    if image is None:
        raise Exception('image is invalid')
    
    height = image.shape[0]
    width = image.shape[1]

    blocks_per_row = height // block_size
    blocks_per_col = width // block_size

    for block_j in range(0, blocks_per_col):
        for block_i in range(0, blocks_per_row):
            factor = block_j + block_i
            is_odd = factor % 2 == 1

            selected_color = []

            selected_color = BLACK if is_odd else WHITE

            block = image[
                block_j * block_size: block_size + (block_j * block_size),
                block_i * block_size: block_size + (block_i * block_size)
            ]

            if not is_invert:
                block = selected_color
                
            else:
                block = 255 - block if is_odd else block
            
            image[
                block_j * block_size: block_size + (block_j * block_size),
                block_i * block_size: block_size + (block_i * block_size)
            ] = block

    return image

# Read image
plankton: cv2.Mat | NumPyArrayNumeric | None = cv2.imread('assets/plankton.jpeg')

if plankton is not None:
    inverted_plankton: Img = invert_image(plankton)

    if inverted_plankton is not None:
        cv2.imshow('inverted', inverted_plankton)
        cv2.waitKey(0)

    half_image_inverted = invert_half_image(plankton)
    
    if half_image_inverted is not None:
        cv2.imshow('half_inverted', half_image_inverted)
        cv2.waitKey(0)

    blocked_image = blocks(plankton, block_size=75, is_invert=True)

    if blocked_image is not None:
        cv2.imshow('blocked', blocked_image)
        cv2.waitKey(0)

# Show image array in BGR
# print(plankton)


