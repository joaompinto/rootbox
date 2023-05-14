from rootbox.images import pull


def test_lxc_pull():
    assert pull("lxc:alpine:edge")
    assert pull(
        "https://dl-cdn.alpinelinux.org/alpine/v3.18/releases/x86_64/alpine-minirootfs-3.18.0-x86_64.tar.gz"
    )
