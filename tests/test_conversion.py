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
    with open(record_file) as stream:
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
    with open(record) as stream:
        record = yaml.safe_load(stream)

    xml_string = metadata_to_xml(record)
    assert xml_string.strip(), "XML string is empty"

    xml_doc = etree.XML(xml_string.encode("utf-8"))
    assert xml_doc is not None, "XML document is None"
    assert isinstance(xml_doc, etree._Element), "XML document is not an Element"

    # Validate against cioos-schema
    schema = etree.XMLSchema(file=CIOOS_SCHEMA)
    schema.assertValid(xml_doc)


def test_identical_translated_keywords_not_duplicated():
    """Keywords identical across languages (e.g. taxa) are only listed once (#116)."""
    record = yaml.safe_load((SAMPLE_RECORDS_DIR / "record.yml").read_text())
    taxa = ["Animalia", "Apis mellifera"]
    record["identification"]["keywords"] = {
        "taxa": {"en": taxa, "fr": taxa},
        "eov": {"en": ["oxygen"], "fr": ["oxygène"]},
    }

    xml_doc = etree.XML(metadata_to_xml(record).encode("utf-8"))
    keyword_texts = [
        "".join(kw.itertext()).strip()
        for kw in xml_doc.iter("{*}keyword")
    ]

    for name in taxa:
        assert keyword_texts.count(name) == 1
    # Real translations are still included
    assert "oxygen" in keyword_texts
    assert "oxygène" in keyword_texts


def _resource_locales(xml_doc):
    """Language codes of the resource (dataset) default and other locales."""
    ns = {
        "mri": "http://standards.iso.org/iso/19115/-3/mri/1.0",
        "lan": "http://standards.iso.org/iso/19115/-3/lan/1.0",
    }
    path = "//mri:MD_DataIdentification/mri:{}/lan:PT_Locale/lan:language/lan:LanguageCode/@codeListValue"
    return (
        xml_doc.xpath(path.format("defaultLocale"), namespaces=ns),
        xml_doc.xpath(path.format("otherLocale"), namespaces=ns),
    )


def test_resource_locale_defaults_to_metadata_language():
    """Resource language falls back to the metadata language (#108)."""
    record = yaml.safe_load((SAMPLE_RECORDS_DIR / "record.yml").read_text())
    record["identification"].pop("language", None)
    record["identification"].pop("language_alternate", None)

    xml_doc = etree.XML(metadata_to_xml(record).encode("utf-8"))

    assert _resource_locales(xml_doc) == (["eng"], [])


def test_resource_locale_from_identification():
    """Explicit resource languages are used when given (#108)."""
    record = yaml.safe_load((SAMPLE_RECORDS_DIR / "record.yml").read_text())
    record["identification"]["language"] = "fr"
    record["identification"]["language_alternate"] = "en"

    xml_doc = etree.XML(metadata_to_xml(record).encode("utf-8"))

    assert _resource_locales(xml_doc) == (["fra"], ["eng"])
    etree.XMLSchema(file=CIOOS_SCHEMA).assertValid(xml_doc)
