import pytest

from rootbox import Container


def test_container():
    with Container("lxc:alpine:edge", 1) as container:
        container.run("echo hello")
        container.run("true")
    with pytest.raises(RuntimeError, match="failed with exit code"):
        container.run("false")


if __name__ == "__main__":
    test_container()
