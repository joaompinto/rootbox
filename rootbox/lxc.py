import requests

from .verbose import verbose

LCX_INDEX = "https://images.linuxcontainers.org/meta/1.0/index-user"
LXC_URL_TEMPL = "https://images.linuxcontainers.org/images/{}/{}/{}/{}/{}/rootfs.tar.xz"


class NotSingleVersonError(Exception):
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

    def versions(self, distro_name, distro_version, distro_arch, distro_variant):
        return tuple(
            set(
                [
                    item["version"]
                    for item in self._index
                    if item["name"] == distro_name
                    and item["arch"] == distro_arch
                    and item["variant"] == distro_variant
                    and (item["version"] == distro_version if distro_version else True)
                ]
            )
        )

    def builds(self, distro_name, distro_version, distro_arch, distro_variant):
        return tuple(
            set(
                [
                    item["build"]
                    for item in self._index
                    if item["name"] == distro_name
                    and item["arch"] == distro_arch
                    and item["variant"] == distro_variant
                    and item["version"] == distro_version
                ]
            )
        )

    def image_url(
        self,
        distro_name,
        distro_version=None,
        distro_arch="amd64",
        distro_variant="default",
    ):
        """Return the URL for the given distro"""
        matching_versions = self.versions(
            distro_name, distro_version, distro_arch, distro_variant
        )
        if len(matching_versions) == 0:
            raise ValueError(
                f"No image found matching {distro_name} {distro_version} {distro_arch} {distro_variant}"
            )
        if len(matching_versions) > 1:
            raise NotSingleVersonError(
                f"Found multiple versions for {distro_name} {distro_version} {distro_arch}",
                matching_versions,
            )
        matching_version = matching_versions[0]
        matchin_builds = self.builds(
            distro_name, matching_version, distro_arch, distro_variant
        )
        assert len(matchin_builds) == 1
        matching_build = matchin_builds[0]
        url = LXC_URL_TEMPL.format(
            distro_name, matching_version, distro_arch, distro_variant, matching_build
        )
        verbose(f"Found image URL {url}")
        return url
