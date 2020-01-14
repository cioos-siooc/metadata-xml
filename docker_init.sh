#!/bin/bash
# This script is run by Docker and CircleCI
set -e
pip -q install . 
cd metadata_xml && python -m unittest tests.py
cd ..
wget https://pac-dev1.cioos.org/dev/public/schema.zip -q
unzip -qq schema.zip
apt update -qq && apt install --yes -qq libxml2-utils
for i in sample_records/*.yaml; do echo "$i";python -m metadata_xml -f "$i"; done
for i in sample_records/*.xml; do echo "$i";xmllint --noout --schema ./standards.iso.org/iso/19115/-3/mds/2.0/mds.xsd "$i"; done