#!/usr/bin/env bash

## Build the super small Alpine image locally

if [ ! -f config.py ]; then
    echo "Configuration file is missing. This needs to be created before building the image."
    exit 1
fi

docker build . -f Dockerfile.alpine -t arris-scrape:alpine --progress=plain
if [ $? -ne 0 ]; then
    echo "Docker build failed"
    exit 1
fi