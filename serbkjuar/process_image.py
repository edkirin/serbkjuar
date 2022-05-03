import logging

from serbkjuar.common import QRImageFile


def process_image(image_file: QRImageFile):
    logging.info(f"Processing file {image_file}")
