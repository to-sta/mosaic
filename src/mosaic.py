""" mosaic module"""

import os
import random
import uuid
from typing import Optional
from pathlib import Path
from math import ceil
import cv2 as cv
import numpy as np


FILE_TYPES = ["png", "jpg", "tiff"]


def SizeError(Exception):
    "Raised when the mosaic image is larger in size than the base image"
    pass


def generate_mosaic(
    base_image_path: str,
    mosaic_images_path: str,
    desired_height: int,
    desired_width: int,
    filetyp: Optional[str] = "png",
) -> None:
    """
    Generate a mosaic picture.
    --------------------------

    This function generates a mosaic image out of a base image and images used as mosaic pieces.
    The base image will be split by into mosaic pieces with the desired height and width. The mosaic images
    will be resized to the desired height and width. A random image is retrieved as the mosaic piece and then it
    will be blended with the average color of the current frame of the base image. Till the image is completed.

    Parameters
    ----------
    base_image_path: str
        relativ or absolute path to the base image
    mosaic_images_path: str
        relativ or absolute path to the folder of the mosaic images
    desired height: int
        desired height of the mosaic image
    desired width: int
        desired width of the mosaic image
    filetype: str (default: png)
        support file typs are png, jpg, tiff

    Returns
    -------
    This function returns None, but will save the mosaic image as a png in the current directory.

    Raises
    -----
    SizeError
        Is raised if the mosaic image dimensions are larger than the base image dimensions

    """
    mosaic_images_path = Path(mosaic_images_path)
    base_img = cv.imread(base_image_path)

    if filetyp not in FILE_TYPES:
        raise TypeError(f"This {filetyp} is not supported.")

    if base_img.shape[0] < desired_height or base_img.shape[1] < desired_width:
        raise SizeError

    mosaic_image_files = os.listdir(mosaic_images_path)

    x = y = 0
    end_height = ceil(base_img.shape[0] / desired_height)
    end_width = ceil(base_img.shape[1] / desired_width)

    for _ in range(end_height):
        for _ in range(end_width):
            frame = base_img[y : y + desired_height, x : x + desired_width]
            random_mosaic_img_file = random.choice(mosaic_image_files)
            mosaic_img = cv.imread(str(mosaic_images_path / random_mosaic_img_file))
            mosaic_img_resized = cv.resize(mosaic_img, (desired_width, desired_height))

            average_color_per_row = np.average(frame, axis=0)
            average_color_frame = np.average(average_color_per_row, axis=0)
            overlay = np.zeros(mosaic_img_resized.shape, np.uint8)
            overlay[:] = average_color_frame

            replacement_frame = cv.addWeighted(mosaic_img_resized, 0.5, overlay, 0.7, 0)

            if (
                base_img.shape[1] < x + desired_width
                or base_img.shape[0] < y + desired_height
            ):
                h, w, _ = base_img[y : y + desired_height, x : x + desired_width].shape
                replacement_frame = replacement_frame[0:h, 0:w]

            base_img[y : y + desired_height, x : x + desired_width] = replacement_frame
            x += desired_width

        x = 0
        y += desired_height

    cv.imwrite(
        f"img_h{desired_height}w{desired_width}_{uuid.uuid4()}.{filetyp}", base_img
    )
