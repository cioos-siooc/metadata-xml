#!/bin/bash

# use like `sh validate.sh record.xml`
SCRIPT_DIR=$(dirname $(realpath "$0"))
SCHEMA_FOLDER="$SCRIPT_DIR/cioos-schema/schema"
export XML_CATALOG_FILES=$SCRIPT_DIR/cioos-schema/catalog.xsd
xmllint --noout --schema "$SCHEMA_FOLDER"/standards.iso.org/iso/19115/-3/mds/2.0/mds.xsd "$1" --nowarning
