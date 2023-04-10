from __future__ import print_function

import tarfile


def extract_tar(tar_fname, dest_dir):
    tarfile.os.chown = (
        lambda x, y, z: 0
    )  # Monkey patch chown because we don't care about ownership

    tarfile.os.mknod = (
        lambda x, y, z: 0
    )  # Monkey patch mknod because some layers include devices
    with tarfile.open(tar_fname) as image_tar:
        image_tar.extractall(dest_dir, numeric_owner=True)
