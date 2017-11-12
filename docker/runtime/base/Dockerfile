FROM python:3.6-slim

MAINTAINER Duy Nguyen <dnguyen0304@gmail.com>

ARG NAMESPACE
ARG CONFIGURATION_FILE_NAME
ARG AWS_CONFIGURATION_FILE_NAME
ARG AWS_CREDENTIALS_FILE_NAME

# unzip is needed to extract the package.
# wget is a dependency of Chrome.
ENV BUILDTIME_DEPENDENCIES="unzip"
ARG RUNTIME_DEPENDENCIES="wget"

ARG CHROME_DRIVER_VERSION="2.32"

ARG PACKAGE_DIRECTORY="/opt/${NAMESPACE}"
ARG CONFIGURATION_DIRECTORY="/etc/opt/${NAMESPACE}"
ARG LOG_DIRECTORY="/var/opt/${NAMESPACE}/log"

ENV CONFIGURATION_FILE_PATH="${CONFIGURATION_DIRECTORY}/${CONFIGURATION_FILE_NAME}"
ENV AWS_CONFIG_FILE="${CONFIGURATION_DIRECTORY}/${AWS_CONFIGURATION_FILE_NAME}"
ENV AWS_SHARED_CREDENTIALS_FILE="${CONFIGURATION_DIRECTORY}/${AWS_CREDENTIALS_FILE_NAME}"
ENV DOWNLOAD_DIRECTORY="/var/opt/${NAMESPACE}/tmp"

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends ${BUILDTIME_DEPENDENCIES} ${RUNTIME_DEPENDENCIES}

RUN useradd ${NAMESPACE}

RUN mkdir ${PACKAGE_DIRECTORY} && \
    mkdir --parent ${CONFIGURATION_DIRECTORY} && \
    mkdir --parent ${LOG_DIRECTORY} && \
    mkdir --parent ${DOWNLOAD_DIRECTORY}

WORKDIR ${PACKAGE_DIRECTORY}

# Include the Chrome dependency.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee --append /etc/apt/sources.list.d/google.list > /dev/null
RUN apt-get update -y && \
    apt-get install -y google-chrome-stable

# Include the Chrome Driver dependency.
RUN wget http://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip -q -d /usr/local/bin chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip

# Xvfb is needed to use a non-headless browser without a display.
#
# As of 2017-11-02, the Chrome browser cannot download files in headless mode.
# This is a known issue. This issue is not a bug but a feature for security
# reasons. See the discussion for more details.
#
# The configuration value is the default from xvfb-run.
#
# xauth is needed to use xvfb-run.
#
# Links
# - https://bugs.chromium.org/p/chromium/issues/detail?id=696481
RUN apt-get install -y --no-install-recommends xvfb xauth
ENV DISPLAY=":99"

RUN chown --recursive ${NAMESPACE}:${NAMESPACE} ${CONFIGURATION_DIRECTORY} && \
    chown --recursive ${NAMESPACE}:${NAMESPACE} ${LOG_DIRECTORY} && \
    chown --recursive ${NAMESPACE}:${NAMESPACE} ${DOWNLOAD_DIRECTORY}

RUN rm -fr /var/lib/apt/lists/*

VOLUME ${CONFIGURATION_DIRECTORY}
VOLUME ${LOG_DIRECTORY}
VOLUME ${DOWNLOAD_DIRECTORY}
