from rootbox import Container


def test_container():
    with Container("lxc:busybox:1.34.1", 1) as container:
        container.run("true")
