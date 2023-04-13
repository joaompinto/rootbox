from dataclasses import dataclass

import requests
import typer

from rootbox.verbose import verbose

from ..http import download_url

LCX_INDEX = "https://images.linuxcontainers.org/meta/1.0/index-user"
LXC_URL_TEMPL = "https://images.linuxcontainers.org/images/{}/{}/{}/{}/{}/rootfs.tar.xz"


@dataclass
class LXCImage:
    name: str
    version: str = None
    arch: str = "amd64"
    variant: str = "default"
    build: str = None

    def as_url(self) -> str:
        return url_to_filename(
            f"lxc_{self.name}_{self.version}_{self.arch}_{self.variant}_{self.build or ''}"
        )

    def download(self):
        return download_url(get_lcx_distro_url(self))


class NotSingleVersionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class LCXMetaData:
    def __init__(self):
        verbose(f"Fetching LXC metadata from {LCX_INDEX}")
        reply = requests.get(LCX_INDEX)
        reply.raise_for_status()
        verbose(f"Received {reply.status_code} {reply.reason} from {reply.url}")
        self._index = self.csv_to_dict(reply.text)

    @staticmethod
    def csv_to_dict(csv):
        lines = csv.splitlines()
        header = ("name", "version", "arch", "variant", "build", "path")
        return [dict(zip(header, line.split(";"))) for line in lines]

    def distros(self):
        return tuple(set([item["name"] for item in self._index]))

    def versions(self, image_name, distro_version, distro_arch, distro_variant):
        return tuple(
            set(
                [
                    item["version"]
                    for item in self._index
                    if item["name"] == image_name
                    and item["arch"] == distro_arch
                    and item["variant"] == distro_variant
                    and (item["version"] == distro_version if distro_version else True)
                ]
            )
        )

    def builds(
        self, image_name, distro_version, distro_arch, distro_variant, distro_build
    ):
        return tuple(
            set(
                [
                    item["build"]
                    for item in self._index
                    if item["name"] == image_name
                    and item["arch"] == distro_arch
                    and item["variant"] == distro_variant
                    and item["version"] == distro_version
                    and (not distro_build or distro_build == item["build"])
                ]
            )
        )

    def image_url(
        self,
        image_name,
        distro_version=None,
        distro_arch="amd64",
        distro_variant="default",
        distro_build=None,
    ):
        """Return the URL for the given distro"""
        matching_versions = self.versions(
            image_name, distro_version, distro_arch, distro_variant
        )
        if len(matching_versions) == 0:
            raise ValueError(
                f"No image found matching {image_name} {distro_version} {distro_arch} {distro_variant}"
            )
        if len(matching_versions) > 1:
            raise NotSingleVersionError(
                f"Found multiple versions for {image_name} {distro_version} {distro_arch}",
                matching_versions,
            )
        matching_version = matching_versions[0]
        matchin_builds = self.builds(
            image_name, matching_version, distro_arch, distro_variant, distro_build
        )
        assert len(matchin_builds) == 1
        matching_build = matchin_builds[0]
        url = LXC_URL_TEMPL.format(
            image_name, matching_version, distro_arch, distro_variant, matching_build
        )
        verbose(f"Found image URL {url}")
        return url


def get_lcx_distro_url(lxc_image: LXCImage) -> str:
    """Get download url from LXC images for a given distro"""
    lcx = LCXMetaData()
    if lxc_image.name not in lcx.distros():
        raise typer.BadParameter(f"Unknown distro {lxc_image.name}")
    return lcx.image_url(
        lxc_image.name,
        lxc_image.version,
        lxc_image.arch,
        lxc_image.variant,
        lxc_image.build,
    )


def url_to_filename(url: str):
    """Convert url to filename"""
    url = url.replace("://", "_")
    url = url.replace("/", "_")
    url = url.replace(":", "_")
    return url
