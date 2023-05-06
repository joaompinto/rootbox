from rootbox.base import base_setup
from rootbox.shell.execute import execute


def run_base_setup():
    base_setup("lxc:busybox:1.34.1")
    execute("busybox")


if __name__ == "__main__":
    run_base_setup()
