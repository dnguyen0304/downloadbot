if [ "${1:-}" = test ]; then
    FOR_TESTING="true"
else
    FOR_TESTING="false"
fi

# Create the container.
tag=${DOMAIN}/${NAMESPACE}-runtime:${VERSION}

if [ ! -z $(sudo docker images --quiet ${tag}) ]; then
    docker rmi --force ${tag}
fi
docker build \
    --file docker/runtime/Dockerfile \
    --tag ${tag} \
    --build-arg DOMAIN=${DOMAIN} \
    --build-arg NAMESPACE=${NAMESPACE} \
    --build-arg BASE_IMAGE_VERSION=${VERSION} \
    --build-arg NAMESPACE=${NAMESPACE} \
    .

if [ "${FOR_TESTING}" = true ]; then
    docker build \
        --file docker/runtime/testing/Dockerfile \
        --tag ${tag} \
        --build-arg DOMAIN=${DOMAIN} \
        --build-arg NAMESPACE=${NAMESPACE} \
        --build-arg BASE_IMAGE_VERSION=${VERSION} \
        .
fi
