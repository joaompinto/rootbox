#!/bin/sh
set -eu
python -m rootbox start lxc:alpine:edge
python -m rootbox exec 'apk --version' > /dev/null
exit 0
