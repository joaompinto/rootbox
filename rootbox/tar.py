"""
We use tar to extract the image instead of tarfile because
before Python3.11.4 tarfile does not support member filtering
that we need to ignore certain files in the image.
"""

import os

from print_err import print_err


def extract_tar(tar_fname, dest_dir):
    excludes_str = " ".join(
        [
            f"--exclude='{e}'"
            for e in ["./dev", "./sys", "./proc", "./run", "./tmp", "./host_root"]
        ]
    )
    cmd = f"tar  -C {dest_dir} -xf {tar_fname} {excludes_str} --no-same-owner"
    rc = os.system(cmd)
    if rc != 0:
        print_err("Failed to extract tar file")
