from rootbox import Container


def test_container():
    with Container("lxc:alpine:edge", 1) as container:
        container.run("true")
