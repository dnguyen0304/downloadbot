ARG CONFIGURATION_FILE_NAME
ARG AWS_CONFIGURATION_FILE_NAME
ARG AWS_CREDENTIALS_FILE_NAME

# wget is a dependency of Chrome.
ARG RUNTIME_DEPENDENCIES="wget"

ARG CHROME_DRIVER_VERSION="2.32"

ARG CONFIGURATION_DIRECTORY="/etc/opt/${NAMESPACE}"

ENV CONFIGURATION_FILE_PATH="${CONFIGURATION_DIRECTORY}/${CONFIGURATION_FILE_NAME}"
ENV AWS_CONFIG_FILE="${CONFIGURATION_DIRECTORY}/${AWS_CONFIGURATION_FILE_NAME}"
ENV AWS_SHARED_CREDENTIALS_FILE="${CONFIGURATION_DIRECTORY}/${AWS_CREDENTIALS_FILE_NAME}"

    ${RUNTIME_DEPENDENCIES}

RUN useradd ${NAMESPACE}

    mkdir --parent ${CONFIGURATION_DIRECTORY} && \

# Include the Chrome dependency.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee --append /etc/apt/sources.list.d/google.list > /dev/null
RUN apt-get update -y && \
    apt-get install -y google-chrome-stable

# Include the Chrome Driver dependency.
RUN wget http://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip -q -d /usr/local/bin chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip

RUN chown --recursive ${NAMESPACE}:${NAMESPACE} ${CONFIGURATION_DIRECTORY} && \

VOLUME ${CONFIGURATION_DIRECTORY}
