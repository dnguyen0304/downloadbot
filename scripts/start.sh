#!/usr/bin/env bash

set -eu

TAG=$(./scripts/get-package-version.sh)

docker run \
    --rm \
    --volume $(pwd):/var/opt/roomlistwatcher/log \
    dnguyen0304/downloadbot-runtime:${TAG}
