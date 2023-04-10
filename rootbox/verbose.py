from .cli import verbose as verbose_cli


def verbose(*args, **kwargs):
    if verbose_cli.is_verbose:
        print(*args, **kwargs)
