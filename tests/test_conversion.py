from pathlib import Path
import pytest 
from metadata_xml.template_functions import metadata_to_xml
import yaml
from lxml import etree


SAMPLE_RECORDS_DIR = Path(__file__).parent / ".." / "sample_records"
SAMPLE_RECORDS = SAMPLE_RECORDS_DIR.glob("*.yml")

XSD_DIR = Path(__file__).parent / ".." / "xsd"
MBD_SCHEMA = Path(__file__).parent / "../xsd/schemas.isotc211.org/19115/-3/mdb/2.0/mdb.xsd"
    

@pytest.mark.parametrize("record_file", SAMPLE_RECORDS)
def test_sample_records(record_file, tmp_path):
    """Test that sample records can be converted to XML."""
    with open(record_file) as stream:
        record = yaml.safe_load(stream)

    xml_string = metadata_to_xml(record)
    
    # Save the XML string to a temporary file
    temp_file = tmp_path / record_file.name.replace(".yml", ".xml")
    temp_file.write_text(xml_string, encoding="utf-8")
    
    # Check that the XML string is not empty
    assert xml_string.strip(), "XML string is empty"

    schema = etree.XMLSchema(file=MBD_SCHEMA)
    xml_doc = etree.parse(temp_file)
    schema.assertValid(xml_doc)
