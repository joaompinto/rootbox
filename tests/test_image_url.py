from pathlib import Path

from rootbox.images import DockerImage, LXCImage, parse_image_url


def test_local_url():
    result = parse_image_url("/path/to/file.tar.gz")
    assert isinstance(result, Path)


def test_lxc_url():
    result = parse_image_url("lxc:archlinux")
    assert isinstance(result, LXCImage)
    assert result.name == "archlinux"
    assert result.version is None

    result = parse_image_url("lxc:alpine:edge")
    assert isinstance(result, LXCImage)
    assert result.name == "alpine"
    assert result.version == "edge"


def test_docker_url():
    result = parse_image_url("docker:busybox")
    assert isinstance(result, DockerImage)
    assert result.registry == "registry-1.docker.io"
    assert result.image_name == "library/busybox"
    assert result.image_tag == "latest"

    result = parse_image_url("docker:busybox:1.2")
    assert isinstance(result, DockerImage)
    assert result.registry == "registry-1.docker.io"
    assert result.image_name == "library/busybox"
    assert result.image_tag == "1.2"

    result = parse_image_url("docker:ghcr.io/deselikem/hello-docker-gcr-demo:latest")
    assert isinstance(result, DockerImage)
    assert result.registry == "ghcr.io"
    assert result.image_name == "deselikem/hello-docker-gcr-demo"
    assert result.image_tag == "latest"
