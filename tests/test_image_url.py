from pathlib import Path

import click
import pytest

from rootbox.images.url_parser import parse_image_url


def test_handler_errors():
    with pytest.raises(click.exceptions.BadParameter, match="with an empty url"):
        parse_image_url("xpto:")

    with pytest.raises(click.exceptions.BadParameter, match="Supported handlers:"):
        parse_image_url("xpto:abc")


def test_local_url():
    result = parse_image_url("/path/to/file.tar.gz")
    assert isinstance(result, Path)
