FROM python:3.6-slim

MAINTAINER Duy Nguyen <dnguyen0304@gmail.com>

ARG NAMESPACE

# unzip is needed to extract the package.
ENV BUILDTIME_DEPENDENCIES="unzip"

ARG PACKAGE_DIRECTORY="/opt/${NAMESPACE}"
ARG LOG_DIRECTORY="/var/opt/${NAMESPACE}/log"

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends ${BUILDTIME_DEPENDENCIES}

RUN useradd ${NAMESPACE}

RUN mkdir ${PACKAGE_DIRECTORY} && \
    mkdir --parent ${LOG_DIRECTORY}

WORKDIR ${PACKAGE_DIRECTORY}

RUN chown --recursive ${NAMESPACE}:${NAMESPACE} ${LOG_DIRECTORY}

RUN rm -fr /var/lib/apt/lists/*

VOLUME ${LOG_DIRECTORY}
