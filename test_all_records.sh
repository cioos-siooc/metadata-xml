# 1) download all cioos yaml files from the metadata form to directory `tmp`
mkdir -p tmp
cd tmp
echo "Downloading YAML files..."
wget -qr -np -nd https://waf.forms.cioos.ca/metadata/ --accept "*.yaml"

# 2) Create an XML for each yaml record
echo "Converting to XML..."
for f in *.yaml; do python -m metadata_xml -f $f >/dev/null; done

# 3) Validate each XML record
echo "Validating..."
for f in *.xml; do sh ../validate.sh $f 2>&1 | grep -v 'validates'; done

echo "Done"
