from rootbox import Container

with Container("lxc:alpine:edge", 1, state_id="build_container") as container:
    container.run("echo ok", store=True)
