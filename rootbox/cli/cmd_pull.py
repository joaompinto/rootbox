"""  pull an image from a remote repository  """
import typer

from ..images import download_image


def pull(
    image_name: str = typer.Argument(...),
    ignore_cache: bool = typer.Option(
        False, "--ignore-cache", help="Ignore cached images"
    ),
):
    download_image(image_name, verbose_cache_info=True, ignore_cache=ignore_cache)
