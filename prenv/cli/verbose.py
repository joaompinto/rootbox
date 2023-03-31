import typer
from metadict import MetaDict

state = MetaDict({"verbose": False})


def verbose(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose mode")
):
    if verbose:
        state["verbose"] = True
