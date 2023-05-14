from dataclasses import dataclass
from typing import Union

from .http import HTTPHandler
from .lxc import LXCHandler
from .url_parser import parse_image_url


@dataclass
class ImageHandler:
    """Image handler"""

    @staticmethod
    def get_handler(image_url: str) -> Union[LXCHandler, HTTPHandler]:
        """Return the handler for the given image"""
        image = parse_image_url(image_url)
        return image
