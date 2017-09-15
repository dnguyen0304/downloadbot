#!/usr/bin/env bash

set -eu

TAG=$(grep -Po "version='\K\d\.\d\.\d" setup.py)

docker build \
    --file docker/buildtime/base/Dockerfile \
    --tag dnguyen0304/downloadbot-buildtime-base:${TAG} \
    --build-arg SHARED_VOLUME="/tmp/build" \
    .
