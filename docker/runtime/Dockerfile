ARG DOMAIN
ARG NAMESPACE
ARG BASE_IMAGE_VERSION
FROM ${DOMAIN}/${NAMESPACE}-runtime-base:${BASE_IMAGE_VERSION}

MAINTAINER Duy Nguyen <dnguyen0304@gmail.com>

ARG NAMESPACE

ARG PACKAGE="${NAMESPACE}-latest.zip"

COPY ${PACKAGE} .

RUN unzip -q ${PACKAGE} && \
    chown --recursive ${NAMESPACE}:${NAMESPACE} . && \
    rm ${PACKAGE}

RUN apt-get purge -y --auto-remove ${BUILDTIME_DEPENDENCIES}

ENTRYPOINT ["python", "./main.py"]
