from pathlib import Path

import pytest
import yaml
from lxml import etree

from metadata_xml.template_functions import metadata_to_xml

SAMPLE_RECORDS_DIR = Path(__file__).parent / ".." / "sample_records"
SAMPLE_RECORDS = SAMPLE_RECORDS_DIR.glob("*.yml")

CIOOS_SCHEMA = (
    Path(__file__).parent
    / "../cioos-schema/schema/schemas.isotc211.org/19115/-3/mdb/2.0/mdb.xsd"
)


def test_schema_exist():
    """Test that the schema file exists."""
    assert CIOOS_SCHEMA.exists(), (
        f"Schema file does not exist: {CIOOS_SCHEMA}, unzip the cioos-schema.zip file in the base directory"
    )


@pytest.mark.parametrize("record_file", SAMPLE_RECORDS)
def test_sample_records(record_file):
    """Test that sample records can be converted to XML."""
    with open(record_file, encoding="UTF-8") as stream:
        record = yaml.safe_load(stream)

    xml_string = metadata_to_xml(record)
    assert xml_string.strip(), "XML string is empty"

    # Write result just to review
    xml_file = record_file.parent / f"{record_file.stem}.xml"
    xml_file.write_text(xml_string, encoding="utf-8")

    xml_doc = etree.XML(xml_string.encode("utf-8"))
    assert xml_doc is not None, "XML document is None"
    assert isinstance(xml_doc, etree._Element), "XML document is not an Element"

    # Validate against cioos-schema
    schema = etree.XMLSchema(file=CIOOS_SCHEMA)
    schema.assertValid(xml_doc)


external_sample_files = list(Path("metadata").glob("**/*.yaml"))


@pytest.mark.skipif(not external_sample_files, reason="No external sample files found")
@pytest.mark.parametrize("record", external_sample_files)
def test_external_records(record):
    """Test that external records can be converted to XML."""
    with open(record, encoding="UTF-8") as stream:
        record = yaml.safe_load(stream)

    xml_string = metadata_to_xml(record)
    assert xml_string.strip(), "XML string is empty"

    xml_doc = etree.XML(xml_string.encode("utf-8"))
    assert xml_doc is not None, "XML document is None"
    assert isinstance(xml_doc, etree._Element), "XML document is not an Element"

    # Validate against cioos-schema
    schema = etree.XMLSchema(file=CIOOS_SCHEMA)
    schema.assertValid(xml_doc)
