
## What is rootbox?

Rootbox is a tool for Linux and WSL that allows regular (unprivileged) users to deploy applications in a portable and reproducible way.


## How does it work
Rootbox uses Linux kernel namespaces to create contained environments.

## What is the difference between rootbox and Docker?
The focus of rootbox is to provide a tool that can be used to run applications without the need to install dependencies on the host system. Rootbox does **NOT** aim to provide full isolation between environemtns and the host, for such use cases please consider using Docker or Podman.

## Container Modes

Rootbox allows to operater containers in two different modes: simple execution and managed execution.

### Simple Containers

A simple container is created for the purpose of executing a command/process «interactive or not». The lifecycle of this container is associated with the new process lifetime. Once the process terminates all the associated resources will be destroyed. The `rootbox run` command provides simple containers.

### Managed Containers

A managed container is created for the purpose of executing multiple processes/commands which share a common filesystem view. A managed container is associated with a manager process which provides some management capabilities to the container. Once the manager process terminates all the associated resources will be destroyed. The `rootbox start` command provides managed containers.

Unlike other container tecnhologies (e.g. Docker), Rootbox does not use a multi container daemon. Instead, Rootbox provides a single container manager which is responsible for the management of a single container.

## What is nedded to run rootbox?
- A Linux distrubtion or Linux on Windows with WSL (Kernel version >=4.18)
- Python 3.8, 3.9, 3.10 or 3.11
- Only 64-bit architectures are supported

## What applications can I run with rootbox?

- images from the Linux Containers project ([LXC](https://https://images.linuxcontainers.org/)).

## Supported package managers

| Status | Tool | Distros |
|:------:|------|---------|
|✅|apk|Alpine|
|✅|pacman|ArchLinux|
|✅|dnf|Alma; CentOS; Fedora; Rocky|
|✅|xbps|VoidLinux|
|✅|zypper|openSUSE|
|❌|apt|Debian/Ubuntu|

## How to install
```sh
pip install rootbox
```
## How to use

### Run an in-memory single run container
Run a shell in an Alpine Linux container
```sh
rootbox run lxc:alpine:3.17
```
Check the apk version:
```sh
rootbox run lxc:alpine:3.17 "apk --version"
```

### Create an in-memory multi run container
```sh
rootbox start lxc:alpine:3.17
```
### Execute a command in a container
```sh
rootbox exec "apk --version"
```
