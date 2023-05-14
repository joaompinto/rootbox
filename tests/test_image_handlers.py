from rootbox.images.handler import ImageHandler

test_cases = {
    "https://dl-cdn.alpinelinux.org/alpine/v3.18/releases/x86_64/alpine-minirootfs-3.18.0-x86_64.tar.gz": "alpine-minirootfs-3.18.0-x86_64.tar.gz",  # noqa: E501
    "lxc:alpine:edge": "lxc_alpine_edge_amd64_default_",
}


def test_cache_keys():
    for url, expected in test_cases.items():
        handler = ImageHandler.get_handler(url)
        assert handler.cache_key() == expected
