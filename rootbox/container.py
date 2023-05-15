import os
import sys
from contextlib import contextmanager

from .process import ProcessManager
from .socket import get_process_socket
from .verbose import verbose


@contextmanager
def Container(image_name: str, ram_disk_size: int, state_id: str = ""):
    """Create a container with the given image name and ram disk size."""
    cm = ContainerManager(image_name, ram_disk_size, state_id)
    try:
        yield cm
    finally:
        cm.stop()


class ContainerManager:
    def __init__(self, image_name, ram_disk_size, state_id) -> None:
        self.child_pid = None
        manager = ProcessManager(ram_disk_size)
        manager.apply_image(image_name)
        self.manager = manager
        verbose("End of container manager init")

    def stop(self):
        try:
            conn = get_process_socket(self.manager.get_pid())
            conn.sendall(b"terminate")
            conn.close()
        except ConnectionRefusedError:
            pass

    def run(self, command: str, store: bool = False):
        verbose("Running command", command)
        pid = os.fork()
        if pid:
            pid, exit_code = os.wait()
            if exit_code:
                raise RuntimeError(
                    f"Command {command} failed with exit code {exit_code}"
                )
            return exit_code
        else:
            os.chroot(self.manager.root_mnt)
            os.chdir("/")
            rc = os.system(f"{command}")
            resultcode = os.waitstatus_to_exitcode(rc)
            os.chroot("/host_root")
            if rc != 0:
                print(f"Command {command} failed with exit code {rc}", file=sys.stderr)
            # Do not want to trigger the parent stop action
            os._exit(resultcode)
