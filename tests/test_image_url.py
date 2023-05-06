from pathlib import Path

import click
import pytest

from rootbox.images import _parse_image_url


def test_handler_errors():
    with pytest.raises(click.exceptions.BadParameter, match="with an empty url"):
        _parse_image_url("xpto:")

    with pytest.raises(click.exceptions.BadParameter, match="Supported handlers:"):
        _parse_image_url("xpto:abc")


def test_local_url():
    result = _parse_image_url("/path/to/file.tar.gz")
    assert isinstance(result, Path)
