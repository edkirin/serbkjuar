import glob
import logging
import pathlib
from dataclasses import dataclass
from typing import List

from PIL import Image, ImageFont, ImageDraw
from PIL.ImageFont import FreeTypeFont
from sqlalchemy.orm import Session

import app.conf as conf
from app.db import MachineModel

FONT_DIRECTORY = pathlib.Path(__file__).parent.joinpath("fonts")


@dataclass
class QRImageFile:
    image_filepath: pathlib.Path
    file_name: str
    machine_id: int

    def __repr__(self) -> str:
        return str(self.image_filepath)


def get_image_list(source_dir: pathlib.Path) -> List[QRImageFile]:
    logging.info(f"Reading *.png file list from {source_dir}")
    image_list = []
    for file in glob.glob(str(source_dir.joinpath("*.png"))):
        image_list.append(
            QRImageFile(
                image_filepath=pathlib.Path(file),
                file_name=pathlib.Path(file).name,
                machine_id=int(pathlib.Path(file).stem),
            )
        )
    return image_list


def attach_external_id_to_image(
    image_filepath: pathlib.Path, external_id: str, font: FreeTypeFont
) -> Image.Image:
    image = Image.open(image_filepath, mode="r").convert("RGBA")
    text = external_id

    draw = ImageDraw.Draw(image)
    text_width = draw.textsize(text, font)[0]
    x_pos = (image.width - text_width) / 2
    y_pos = conf.config.text_y_offset

    draw.text(
        (x_pos, y_pos),
        text=text,
        font=font,
        fill=conf.config.text_color,
    )

    return image


def process_image(machine: MachineModel, image_file: QRImageFile, font: FreeTypeFont):
    image = attach_external_id_to_image(
        image_file.image_filepath,
        external_id=str(machine.external_id),
        font=font,
    )
    # optimize image for size
    image = image.convert("P", palette=Image.ADAPTIVE)

    if not conf.config.out_dir:
        raise Exception("Output directory not defined")

    out_filepath = conf.config.out_dir.joinpath(image_file.file_name)
    logging.info(f"Writing image: '{out_filepath}'")

    image.save(
        out_filepath,
        format="png",
        optimize=True,
    )


def process_images(session: Session, image_files: List[QRImageFile]):
    font_file = FONT_DIRECTORY.joinpath(conf.config.font_filename)
    try:
        font = ImageFont.truetype(str(font_file), conf.config.text_height)
    except Exception as e:
        raise Exception(f"Error loading font file '{font_file}': {e}")

    files_count = len(image_files)
    for n, image_file in enumerate(image_files):
        logging.info(f"Processing file {n + 1}/{files_count}: '{image_file}'")

        machine = MachineModel.get_by_id(session=session, id=image_file.machine_id)
        if not machine:
            logging.error(
                f"Machine with id {image_file.machine_id} does not exists in database"
            )
            continue

        try:
            process_image(machine, image_file, font)
        except Exception as e:
            logging.error(e)
