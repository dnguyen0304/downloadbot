#!/usr/bin/env bash

set -eu

TAG=$(./scripts/get-package-version.sh)

docker run \
    --rm \
    --volume $(pwd):/etc/opt/downloadbot \
    --volume $(pwd):/var/opt/roomlistwatcher/log \
    dnguyen0304/downloadbot-runtime:${TAG}
