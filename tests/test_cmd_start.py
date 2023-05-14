from typer.testing import CliRunner

from rootbox.__main__ import app

runner = CliRunner()


def test_start():
    result = runner.invoke(app, ["start", "lxc:alpine:edge"])
    assert result.exit_code == 0
