import argparse
import logging
import pathlib

import app.conf as conf
from app.db import create_db_session
from app.processing import get_image_list, process_images

CONFIG_FILENAME = "config.json"

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Add machine external ids to images.")
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
        help="Output directory",
    )
    return parser


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    script_dir = pathlib.Path(__file__).parent

    config_filename = pathlib.Path(script_dir).joinpath(CONFIG_FILENAME)
    try:
        conf.read_config(config_filename)
    except Exception as e:
        logging.error(e)
        return

    source_dir = pathlib.Path(script_dir).joinpath(args.source)
    conf.config.out_dir = pathlib.Path(script_dir).joinpath(args.out)

    session = create_db_session(
        db_user=conf.config.db_user,
        db_password=conf.config.db_password,
        db_host=conf.config.db_host,
        db_port=conf.config.db_port,
        db_name=conf.config.db_name,
    )

    image_files = get_image_list(source_dir)
    try:
        process_images(session, image_files)
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
