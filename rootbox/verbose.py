from .cli import main as rootbox


def verbose(*args, **kwargs):
    if rootbox.is_verbose:
        print(*args, **kwargs)
