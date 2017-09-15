#!/usr/bin/env bash

set -e

package="${COMPONENT}-$(grep -Po "version='\K\d\.\d\.\d" ${SHARED_VOLUME}/setup.py)"

if [ -d ${SHARED_VOLUME}/build ]; then
    rm -r ${SHARED_VOLUME}/build
fi
mkdir ${SHARED_VOLUME}/build ${package}

# Include the source code.
cp -r ${SHARED_VOLUME}/${COMPONENT} ${package}/${COMPONENT}

# Include the dependencies.
pip install --no-cache \
            --requirement ${SHARED_VOLUME}/requirements.txt \
            --target ${package}

# Include the configuration.
cp -r ${SHARED_VOLUME}/configuration ${package}

# Compress the package.
cd ${package}
zip -9qr ${package}.zip .
cp ${package}.zip ${COMPONENT}-latest.zip
mv ${COMPONENT}-*.zip ${SHARED_VOLUME}/build
