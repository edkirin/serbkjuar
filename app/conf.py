import json
from dataclasses import dataclass
import pathlib
from typing import Optional


@dataclass
class AppConfig:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    font_filename: str
    text_color: str = "#000000"
    text_height: int = 30
    text_y_offset: int = 0
    out_dir: Optional[pathlib.Path] = None


config: AppConfig


def read_config(filename: pathlib.Path):
    global config

    with open(filename) as f:
        try:
            cfg_data = json.loads(f.read())
        except Exception as e:
            raise Exception(f"Error parsing config file: {e}")

        try:
            config = AppConfig(**cfg_data)
        except Exception as e:
            raise Exception(f"Error loading configuration: {e}")
