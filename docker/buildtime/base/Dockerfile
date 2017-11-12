FROM python:3.6-slim

MAINTAINER Duy Nguyen <dnguyen0304@gmail.com>

ARG SHARED_VOLUME

ARG BUILD_DIRECTORY="/tmp/.build"

# build-essential is needed to compile C source code.
# zip is needed to archive the package.
ARG DEPENDENCIES="build-essential zip"

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends ${DEPENDENCIES}

RUN mkdir --parents ${SHARED_VOLUME} && \
    mkdir --parents ${BUILD_DIRECTORY}

WORKDIR ${BUILD_DIRECTORY}

RUN rm -fr /var/lib/apt/lists/*

VOLUME ${SHARED_VOLUME}

ENTRYPOINT ["./build.sh"]
