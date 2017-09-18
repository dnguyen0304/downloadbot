ARG DOMAIN
ARG NAMESPACE
ARG BASE_IMAGE_VERSION
FROM ${DOMAIN}/${NAMESPACE}-runtime-base:${BASE_IMAGE_VERSION}

MAINTAINER Duy Nguyen <dnguyen0304@gmail.com>

ARG NAMESPACE

ARG PACKAGE="${NAMESPACE}-latest.zip"

ENV DOWNLOAD_DIRECTORY="/var/opt/${NAMESPACE}/data"

RUN mkdir --parent ${DOWNLOAD_DIRECTORY}

COPY ${PACKAGE} .

RUN unzip -q ${PACKAGE} && \
    chown --recursive ${NAMESPACE}:${NAMESPACE} . && \
    rm ${PACKAGE}

RUN chown --recursive ${NAMESPACE}:${NAMESPACE} ${DOWNLOAD_DIRECTORY}

RUN apt-get purge -y --auto-remove ${BUILDTIME_DEPENDENCIES}

VOLUME ${DOWNLOAD_DIRECTORY}

ENTRYPOINT ["python", "./main.py"]
