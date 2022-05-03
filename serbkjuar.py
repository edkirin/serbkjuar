import argparse
import logging
import os
import glob
from pathlib import Path
import pathlib
from typing import List
from config import read_config
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

CONFIG_FILENAME = "config.json"

logging.basicConfig(level=logging.INFO)


@dataclass
class QRImageFile:
    image_filepath: Path
    file_name: str
    external_id: str


def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Add machine external ids to images")
    parser.add_argument(
        "--source",
        type=str,
        default=".",
        help="Source directory containing QR images in PNG format",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="./out",
        help="Destination directory",
    )
    return parser


def get_image_list(source_dir: Path) -> List[QRImageFile]:
    logging.info(f"Reading *.png file list from {source_dir}")
    image_list = []
    for f in glob.glob(str(source_dir.joinpath("*.png"))):
        image_list.append(QRImageFile(
            image_filepath=Path(f),
            file_name=Path(f).name,
            external_id=Path(f).stem,
        ))
    return image_list


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    script_dir = Path(__file__).parent

    source_dir = pathlib.Path(script_dir).joinpath(args.source)
    out_dir = pathlib.Path(script_dir).joinpath(args.out)

    config_filename = Path(script_dir).joinpath(CONFIG_FILENAME)
    try:
        config = read_config(config_filename)
    except Exception as e:
        logging.error(e)
        return

    source_files = get_image_list(source_dir)

    for c in source_files:
        print(c)

if __name__ == "__main__":
    main()
