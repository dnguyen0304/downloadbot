#!/usr/bin/env bash

set -eu

COMPONENT=$1
SHARED_VOLUME=$2
VERSION=$3

# Set the build root to the working directory. Now relative references
# may be used.
BUILD_ROOT=$(pwd)

PACKAGE="${COMPONENT}-${VERSION}"
mkdir ${PACKAGE}

# Include the source code.
cp -r ${COMPONENT} ${PACKAGE}

# Include the dependencies.
pip install --requirement requirements.txt --target ${PACKAGE}

# Include the entry point.
cp main.py ${PACKAGE}

# Archive the package.
cd ${PACKAGE}
zip -9qr ${PACKAGE}.zip .
cp ${PACKAGE}.zip ${COMPONENT}-latest.zip
mv ${COMPONENT}-*.zip ${SHARED_VOLUME}
