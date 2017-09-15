#!/usr/bin/env bash

set -eu

echo $(grep -Po "version='\K\d\.\d\.\d" setup.py)
