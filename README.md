# prenv

**p**ortable **r**eproducible **env**ironments for Linux applications

[![PyPi](https://img.shields.io/pypi/v/prenv.svg?style=flat-square)](https://pypi.python.org/pypi/prenv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

## What is prenv?

prenv is a tool that allows regular users to deploy applications in a portable and reproducible way.

prenv does not require root privileges to be installed or used.
The focus of prenv is to provide a tool that can be used to run applications in a reproducible way, without the need to install dependencies on the host system.
 > prenv does **NOT** aim to provide full isolation between environemtns and the host, for such kind case please consider using Docker or Podman.

## Which applications can I run with prenv?

Currently you can run applications available to install from the following distributions:

|Short Name|                      | Status | Test command |Comments |
|-|--------------------- |:------:|:------:|---|
|Alpine|Alpine Linux|✓| pacman -S --noconfirm jq|
|archlinux|Arch Linux| ✓ | |
|Fedora|Fedora Linux| ✓ | |
|Void|Void Linux| ✓ | |
|✗|Debian Linux| ✗ | APT fails on privileged operations|
|✗|Ubuntu Linux| ✗ | APT fails on privileged operations|

## System Requirements

- Linux or WSL2 (Kernel version >=4.18)
- Python 3.8, 3.9, 3.10 or 3.11

## How to install
```sh
pip install prenv
```
## How to use

Creating an in-memory ephemeral container with the default shell for a Linux distribution:
```sh
# Check the list of supported distro names in the table above
prenv create distroname
```
