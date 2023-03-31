# prenv

**p**ortable **r**eproducible **env**ironments for Linux applications

[![PyPi](https://img.shields.io/pypi/v/prenv.svg?style=flat-square)](https://pypi.python.org/pypi/prenv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

## What is prenv?

prenv is a tool that allows regular users to deploy applications in a portable and reproducible way.

Unlike other container tools like Docker or Podman, prenv does not require root privileges to be installed or used.
The developer focus of prenv is to provide a tool that can be used to run applications in a reproducible way, without the need to install dependencies on the host system. It does not aim to provide the same level of isolation as other container tools.

## Which applications can I run with prenv?

Currently you can run any application that can be installed on Alpine Linux.

## System Requirements

- Linux or WSL2 (Kernel version >=4.18)
- Python 3.8, 3.9, 3.10 or 3.11

## How to install
```sh
pip install prenv
```
## How to use
Create an ephemeral in-memory Alpine instance

```sh
prenv create alpine
apk update
apk add curl jq
curl -s https://www.githubstatus.com/api/v2/status.json
```
