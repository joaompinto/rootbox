from pathlib import Path


class MountChecker:
    mounts: list[str] = []

    @staticmethod
    def read_mounts() -> list[str]:
        mounts = []
        with open("/proc/mounts") as f:
            for line in f:
                mounts.append(line.split()[1])
        MountChecker.mounts = mounts

    def is_on(self, path: Path):
        if path.is_symlink():
            return False
        for mount in self.mounts:
            if path.starts_with(mount):
                return True

    def is_on_mount_dir(path: str):
        """Check if the path is present only on the mount dir"""
        if path[0] == ".":
            path = path[1:]
        for mount in MountChecker.mounts:
            if path.startswith(mount) and mount != "/":
                return False
        return True


def is_path_contained(path1: Path, path2: Path) -> bool:
    """Check if path2 is contained in path1"""
    return (
        Path(path1).resolve().parts[: len(Path(path2).resolve().parts)]
        == Path(path2).resolve().parts
    )
