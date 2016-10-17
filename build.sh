#!/bin/bash
# Builds the dcm-convert container.
# The container can be exported using the export.sh script

GEAR=scitran/dcm2niix
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

docker build --no-cache --tag $GEAR $DIR
