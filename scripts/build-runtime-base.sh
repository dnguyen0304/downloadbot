#!/usr/bin/env bash

set -eu

TAG=$(./scripts/get-package-version.sh)

docker build \
    --file docker/runtime/base/Dockerfile \
    --tag dnguyen0304/downloadbot-runtime-base:${TAG} \
    --build-arg NAMESPACE="downloadbot" \
    --build-arg CONFIGURATION_FILE_NAME="application.config" \
    .
