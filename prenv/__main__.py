import typer

from .cli import cmd_create, verbose


def main():
    app = typer.Typer(short_help="Utility to manage a pypy.org metadata cache")

    app.command()(cmd_create.create)
    app.callback()(verbose.verbose)
    app()


if __name__ == "__main__":
    main()
