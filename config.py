from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class AppConfig:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str


def read_config(filename: Path) -> AppConfig:
    with open(filename) as f:
        try:
            cfg_data = json.loads(f.read())
        except Exception as e:
            raise Exception(f"Error parsing config file: {e}")

        try:
            config = AppConfig(**cfg_data)
        except Exception as e:
            raise Exception(f"Error loading configuration: {e}")

    return config
