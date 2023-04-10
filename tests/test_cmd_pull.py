import pytest
import typer

from rootbox.cli import cmd_pull


def test_cmd_pull_local():
    with pytest.raises(typer.BadParameter):
        cmd_pull.pull("/path/to/file.tar.gz")


def test_cmd_pull_lxc():
    with pytest.raises(typer.BadParameter):
        cmd_pull.pull("lxc:unknown")

    with pytest.raises(ValueError):
        cmd_pull.pull("lxc:alpine")

    cmd_pull.pull("lxc:alpine:edge")
    cmd_pull.pull("lxc:alpine:edge", ignore_cache=True)


def test_cmd_pull_docker():
    pass
    # with pytest.raises(requests.exceptions.HTTPError):
    #     cmd_pull.pull("docker:unknown")
    # cmd_pull.pull("docker:alpine")
