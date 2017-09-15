#!/usr/bin/env bash

set -eu

DOMAIN="dnguyen0304"
NAMESPACE="downloadbot"
VERSION=$(grep -Po "version='\K\d\.\d\.\d" setup.py)
REMOTE_SHARED_VOLUME="/tmp/build"

# Clean up existing packages created by previous builds.
rm --force ${NAMESPACE}*.zip

# Create the buildtime container.
BUILDTIME_BASE_IMAGE_VERSION="0.1.0"
tag=${DOMAIN}/${NAMESPACE}-buildtime:${BUILDTIME_BASE_IMAGE_VERSION}

if [ ! -z $(sudo docker images --quiet ${tag}) ]; then
    docker rmi --force ${tag}
fi
docker build \
    --file docker/buildtime/Dockerfile \
    --tag ${tag} \
    --build-arg DOMAIN=${DOMAIN} \
    --build-arg NAMESPACE=${NAMESPACE} \
    --build-arg BASE_IMAGE_VERSION=${BUILDTIME_BASE_IMAGE_VERSION} \
    --build-arg COMPONENT=${NAMESPACE} \
    .

# Create the package.
docker run \
    --rm \
    --volume $(pwd):${REMOTE_SHARED_VOLUME} \
    ${tag} \
    ${NAMESPACE} ${REMOTE_SHARED_VOLUME} ${VERSION}
