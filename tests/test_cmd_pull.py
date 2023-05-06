# from typer.testing import CliRunner

# from rootbox.__main__ import app

# runner = CliRunner()


# def test_pull_remote():
#     result = runner.invoke(app, ["pull", "bananas"])
#     assert "Only remote images are supported" in result.stdout
#     assert result.exit_code == 2

#     result = runner.invoke(app, ["pull", "lxc:alpine"])
#     assert isinstance(result.exception, SystemExit)
#     assert result.exit_code == 2
