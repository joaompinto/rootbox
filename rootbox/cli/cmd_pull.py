"""  pull an image from a remote repository  """
import typer

from ..images import pull as image_pull


def pull(
    image_name: str = typer.Argument(...),
    ignore_cache: bool = typer.Option(
        False, "--ignore-cache", help="Ignore cached images"
    ),
):
    image_pull(image_name, verbose_cache_info=True, ignore_cache=ignore_cache)
