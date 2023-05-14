from dataclasses import dataclass
from urllib.parse import urlparse

from ..http import download_url


@dataclass
class HTTPHandler:
    url: str

    def cache_key(self) -> str:
        url_obj = urlparse(self.url)
        last_path = url_obj.path.split("/")[-1]
        return last_path

    def download(self):
        return download_url(self.url)

    def is_local(self):
        return False

    def is_remote(self):
        return True
