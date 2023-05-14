from rootbox.process import ProcessManager


def test_manager():
    manager = ProcessManager(1)
    manager.apply_image("lxc:alpine:edge")
