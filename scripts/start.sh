#!/usr/bin/env bash

set -eu

NAMESPACE="downloadbot"
TAG=$(./scripts/get-package-version.sh)

docker run \
    --rm \
    --volume $(pwd):/etc/opt/${NAMESPACE} \
    --volume $(pwd):/var/opt/${NAMESPACE}/log \
    dnguyen0304/${NAMESPACE}-runtime:${TAG}
