# prenv

**p**ortable **r**eproducible **env**ironments for Linux applications

## What is prenv?

prenv is a tool that allows to run Linux applications in unprivileged containerized environments. It aims to enable the use of several image types by regular Linux/WSL users.

Currently supported image formats:

    [X] Rootfs archives
        [X] Tar
            [X] Apine Linux
            [ ] Arch Linux
            [ ] Debian
            [ ] Fedora
            [ ] Gentoo
            [ ] Ubuntu

    [ ] Docker images

prenv does not aim to be a full container runtime, but rather a tool enabling the distribution of applications in a portable and reproducible way.


## System Requirements

- Linux or WSL2 (Kernel version >=4.18)
- Python 3.8, 3.9, 3.10 or 3.11

## How to install
```sh
pip install prenv
```
## Examples
Create an ephemeral in-memory Alpine instance

```sh
prenv create alpine
```
