import argparse
import glob
import logging
import pathlib
from typing import List

from serbkjuar.common import QRImageFile
from serbkjuar.config import read_config
from serbkjuar.process_image import process_image

CONFIG_FILENAME = "config.json"

logging.basicConfig(level=logging.INFO)


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


def get_image_list(source_dir: pathlib.Path) -> List[QRImageFile]:
    logging.info(f"Reading *.png file list from {source_dir}")
    image_list = []
    for f in glob.glob(str(source_dir.joinpath("*.png"))):
        image_list.append(
            QRImageFile(
                image_filepath=pathlib.Path(f),
                file_name=pathlib.Path(f).name,
                external_id=pathlib.Path(f).stem,
            )
        )
    return image_list


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    script_dir = pathlib.Path(__file__).parent

    source_dir = pathlib.Path(script_dir).joinpath(args.source)
    out_dir = pathlib.Path(script_dir).joinpath(args.out)

    config_filename = pathlib.Path(script_dir).joinpath(CONFIG_FILENAME)
    try:
        config = read_config(config_filename)
    except Exception as e:
        logging.error(e)
        return

    image_files = get_image_list(source_dir)

    for image_file in image_files[:1]:
        process_image(image_file)


if __name__ == "__main__":
    main()
