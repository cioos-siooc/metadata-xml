#!/bin/bash

# stop on errors
set -e

# First install this package with `pip install -e .`

# extract schema if doesnt exist
[ ! -d "cioos-schema" ] && unzip -q cioos-schema.zip

# create an xml from a yaml file
python -m metadata_xml -f sample_records/record.yml

# make sure it validates with the schema
sh validate.sh sample_records/record.xml
