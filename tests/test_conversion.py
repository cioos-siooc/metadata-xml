from pathlib import Path
import pytest 
from metadata_xml.template_functions import metadata_to_xml
import yaml
from lxml import etree


SAMPLE_RECORDS_DIR = Path(__file__).parent / ".." / "sample_records"
SAMPLE_RECORDS = SAMPLE_RECORDS_DIR.glob("*.yml")

MBD_SCHEMA = Path(__file__).parent / "../xsd/schemas.isotc211.org/19115/-3/mdb/2.0/mdb.xsd"
    

@pytest.mark.parametrize("record_file", SAMPLE_RECORDS)
def test_sample_records(record_file, tmp_path):
    """Test that sample records can be converted to XML."""
    with open(record_file) as stream:
        record = yaml.safe_load(stream)

    xml_string = metadata_to_xml(record)
    assert xml_string.strip(), "XML string is empty"

    # Write result just to review
    xml_file =  record_file.parent / f"{record_file.stem}.xml"
    xml_file.write_text(xml_string, encoding="utf-8")

    xml_doc = etree.XML(xml_string.encode("utf-8"))
    assert xml_doc is not None, "XML document is None"
    assert isinstance(xml_doc, etree._Element), "XML document is not an Element"


    schema = etree.XMLSchema(file=MBD_SCHEMA)
    schema.assertValid(xml_doc)
