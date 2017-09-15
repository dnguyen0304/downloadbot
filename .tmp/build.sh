if [ "${1:-}" = test ]; then
    FOR_TESTING="true"
else
    FOR_TESTING="false"
fi

if [ "${FOR_TESTING}" = true ]; then
    docker build \
        --file docker/runtime/testing/Dockerfile \
        --tag ${tag} \
        --build-arg DOMAIN=${DOMAIN} \
        --build-arg NAMESPACE=${NAMESPACE} \
        --build-arg BASE_IMAGE_VERSION=${VERSION} \
        .
fi
