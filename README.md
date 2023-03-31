# prenv

**p**ortable **r**eproducible **env**ironments for Linux applications

## What is prenv?

prenv is a tool that allows regular users to deploy applications in a portable and reproducible way.


Unlike other container tecnhologies, prenv aims to provide integration with the running system - providing only the file level isolation required to execute an application.

This means that prenv can be used to run applications that require access to the host's network, devices, or other resources.

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
