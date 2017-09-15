#!/usr/bin/env bash

set -eu

TAG=$(./scripts/get-package-version.sh)

docker build \
    --file docker/buildtime/base/Dockerfile \
    --tag dnguyen0304/downloadbot-buildtime-base:${TAG} \
    --build-arg SHARED_VOLUME="/tmp/build" \
    .
