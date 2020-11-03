#!/bin/bash
# This script is run by Docker and CircleCI
set -e

# install this package 
pip install .

# download an install cioos-iso-validate
wget https://codeload.github.com/cioos-siooc/cioos-iso-validate/zip/master -O cioos-iso-validate.zip
unzip cioos-iso-validate.zip
cd cioos-iso-validate-master
sh download_schema_files.sh
pip install .

cd ..

python -m metadata_xml -f sample_records/record.yml
python -m cioos_iso_validate sample_records/record.xml

apt update -qq  && apt install -qq  libxml2-utils

python -m metadata_xml.erddap -f sample_records/record.yml | xmllint -