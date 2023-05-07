from rootbox import Container

with Container("lxc:alpine:edge", 1) as container:
    container.run("echo 'Hello World1!'")
    container.run("echo 'Hello World12!'")


with Container("lxc:alpine:edge", 1) as container:
    container.run("echo 'Hello World2!'")
    container.run("echo 'Hello World21!'")
