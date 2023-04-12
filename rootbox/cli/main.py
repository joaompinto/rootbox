import typer

is_verbose = False


def rootbox(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose mode")
):
    if verbose:
        print("Running in verbose mode")
        global is_verbose
        is_verbose = True
