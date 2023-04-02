import typer

from .cli import cmd_create, cmd_join, cmd_lxc, verbose


def main():
    app = typer.Typer(short_help="Utility to manage a pypy.org metadata cache")

    app.command(help="Create a container instance")(cmd_create.create)
    app.command(help="Join command into an existing instance")(cmd_join.join)
    app.add_typer(
        cmd_lxc.app, name="lxc", help="Get information about available LCX images"
    )

    app.callback()(verbose.verbose)
    app()


if __name__ == "__main__":
    main()
