import os

from .cli import main as rootbox


def verbose(*args, **kwargs):
    if rootbox.is_verbose or os.getenv("ROOTBOX_VERBOSE"):
        print(*args, **kwargs)
