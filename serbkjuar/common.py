import pathlib
from dataclasses import dataclass


@dataclass
class QRImageFile:
    image_filepath: pathlib.Path
    file_name: str
    external_id: str

    def __repr__(self) -> str:
        return str(self.image_filepath)
