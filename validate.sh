#!/bin/bash

# use like `sh validate.sh record.xml`
SCRIPT_DIR=$(dirname $(realpath "$0"))
SCHEMA_FOLDER="$SCRIPT_DIR/cioos-schema/schema"
xmllint --noout --schema "$SCHEMA_FOLDER"/schemas.isotc211.org/19115/-3/mdb/2.0/mdb.xsd "$1" --nowarning