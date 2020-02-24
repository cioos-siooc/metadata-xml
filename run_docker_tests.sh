#!/bin/bash

# Run tests and schema validation using Docker if it's installed

if [ -x "$(command -v docker)" ]; then
   docker build --force-rm . -t metadata_xml && docker image rm metadata_xml
else
    echo "Docker is not installed"
fi