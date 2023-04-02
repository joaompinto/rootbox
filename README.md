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

|Distro|Status|Command|Exec. time|Notes|
|:----:|:----:|--------|:---------:|:-------|
|Alpine Linux|✓|prenv run alpine:3.17 true|2|
|openSUSE|✓|prenv run opensuse:tumbleweed true|5|
|Void Linux|✓|prenv run voidlinux true|5
|Amazon Linux|✓|prenv run amazonlinux true|6|
|Springdale Linux|✓|prenv run springdalelinux:9 true|8|
|AlmaLinuxOS|✓|prenv run almalinux:9 true|10|
|CentoOS|✓|prenv run centos:9-Stream true|10|
|Fedora Linux|✓|prenv run fedora:37 true|10
|Rocky Linux|✓|prenv run rockylinux:9 true|10|
|Arch Linux|✓|prenv run archlinux true|16|



The Linux images are sourced from https://linuxcontainers.org/ and are based on the official images from the respective distributions.

## System Requirements

- Linux or WSL2 (Kernel version >=4.18)
- Python 3.8, 3.9, 3.10 or 3.11

## How to install
```sh
pip install prenv
```
## How to use

List all the distributions available from the LXC project
```sh
# Check the list of supported distro names in the table above
prenv lxc list
```

### Run an in-memory single run container
Run a shell in an Alpine Linux container
```sh
prenv run alpine:3.17
```
Check the apk version:
```sh
prenv run alpine:3.17 "apk --version"
```

### Create an in-memory multi run container
```sh
prenv create alpine:3.17
```
### Execute a command in a container
```sh
prenv execute alpine:3.17 "apk --version"
```
