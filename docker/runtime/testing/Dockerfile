ARG DOMAIN
ARG NAMESPACE
ARG BASE_IMAGE_VERSION
FROM ${DOMAIN}/${NAMESPACE}-runtime:${BASE_IMAGE_VERSION}

MAINTAINER Duy Nguyen <dnguyen0304@gmail.com>

COPY requirements-testing.txt .

# Include the dependencies for testing.
RUN pip install --requirement requirements-testing.txt

ENTRYPOINT ["nosetests", "roomlistwatcher"]
