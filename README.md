# metadata-xml

`metadata-xml` is a Python3 package for converting metadata records defined using
ACDD-style field names into XML that fits into the [CIOOS](https://www.cioos.ca)
metadata profile.

It can be used as a command line tool, or imported into other Python code.

## Installation

1. Setup and activate a new Python 3 environment
2. From this directory, run:

   `pip install .`

3. To upgrade this package if you have already installed it, use:

   `pip install . --upgrade`

   - or If you are developing this package, to avoid reinstalling each time,
     use:

     `pip install -e .`

## Command line usage

To convert a Yaml file to XML, run:

`python -m metadata_xml -f <yaml_file_path>`

eg:

`python -m metadata_xml -f sample_records/record.yaml`

## From Python code

Here is an example of how to use this module in your Python code.

```python
from metadata_xml.iso_template import iso_template

record = {"language": "fra",
          "summary": "summary in french..",
          ...
          }
xml = iso_template(record)
```

## Table of fields

These are the ACDD style keywords that you can use in your record.

For the fields that are text and have bilingual support, you can add on '\_fra' or '\_eng' to input the alternate language.

See example .yaml files in the 'sample_records' directory for more examples.

| field name               | example value                                 | data type          | bilingual support | codelist options                              | Notes                                            |
| ------------------------ | --------------------------------------------- | ------------------ | ----------------- | --------------------------------------------- | ------------------------------------------------ |
| comment                  |                                               | text               | ✓                 |                                               |                                                  |
| acknowledgement          |                                               | text               | ✓                 |                                               |                                                  |
| contributor_name         |                                               | text               |                   |                                               |                                                  |
| contributor_role         | Source of Level 2b data                       | text               |                   | ✓                                             |                                                  |
| creator_email            | nobody@example.com                            | email              |                   |                                               |                                                  |
| creator_name             |                                               | text               |                   |                                               |                                                  |
| creator_url              | <http://example.com>                          | text               |                   |                                               |                                                  |
| creator_type             | person                                        | text               |                   | Codelist                                      |                                                  |
| data_maintenance_note    |                                               | text               | ✓                 |                                               | Not from ACDD/CF                                 |
| date_created             | 2010-01-22                                    | ISO 8601 Date/Time |                   |                                               |                                                  |
| date_issued              | 2010-01-23                                    | ISO 8601 Date/Time |                   |                                               |                                                  |
| date_modified            | 2010-01-24                                    | ISO 8601 Date/Time |                   |                                               |                                                  |
| distributor_name         | distributor name                              | text               |                   |                                               |                                                  |
| erddap_dataset_url       | <http://example.com/erddap/tabledap/abc.html> | URL                |                   |                                               | Not from ACDD/CF                                 |
| geospatial_bounds        | 0,0 100,0 100,100 0,100                       |                    |                   |                                               |                                                  |
| geospatial_lat_max       |                                               | Numeric            |                   |                                               |                                                  |
| geospatial_lat_min       |                                               | Numeric            |                   |                                               |                                                  |
| geospatial_lon_max       |                                               | Numeric            |                   |                                               |                                                  |
| geospatial_lon_min       |                                               | Numeric            |                   |                                               |                                                  |
| geospatial_vertical_max  |                                               | Numeric            |                   |                                               |                                                  |
| geospatial_vertical_min  |                                               | Numeric            |                   |                                               |                                                  |
| history                  |                                               | text               | ✓                 |                                               |                                                  |
| id                       | 12345                                         | text               |                   |                                               |                                                  |
| institution              |                                               | text               |                   |                                               |                                                  |
| keywords_vocabulary      |                                               | text               | ✓                 |                                               |                                                  |
| keywords                 |                                               | text               | ✓                 | At least one of [EOV codelist](#eov-codelist) |                                                  |
| language                 | eng                                           | text               |                   | fra or eng                                    | Not from ACDD/CF                                 |
| naming_authority         |                                               | text               | ✓                 |                                               |                                                  |
| platform_id_authority    |                                               | text               | ✓                 |                                               | Not from ACDD/CF                                 |
| platform_id              |                                               | text               |                   |                                               | Not from ACDD/CF                                 |
| platform_name            |                                               | text               |                   |                                               | Not from ACDD/CF                                 |
| platform_role            | author                                        | text               |                   | [Role Codes](#role-codes)                     | Not from ACDD/CF                                 |
| progress_code            | onGoing                                       | text               |                   | [Progress Codes](#progress-codes)             | Not from ACDD/CF                                 |
| project                  |                                               | text               | ✓                 |                                               |                                                  |
| publisher_country        |                                               | text               | ✓                 |                                               | Not from ACDD/CF                                 |
| publisher_email          | nobody@example.com                            | email              |                   |                                               |                                                  |
| publisher_institution    |                                               | text               |                   |                                               |                                                  |
| publisher_name           |                                               | text               |                   |                                               |                                                  |
| publisher_url            |                                               | URL                |                   |                                               |                                                  |
| publisher_type           | group                                         | text               |                   | [Party Role Codes](#party-role-codes)         |                                                  |
| summary                  |                                               | text               |                   |                                               | Required in ERDDAP                               |
| time_coverage_duration   | P1D                                           | ISO 8601 Duration  |                   |                                               |                                                  |
| time_coverage_start      | 2012-10-21                                    | ISO 8601 Date/Time |                   |                                               | Set in ERDDAP automatically when source is files |
| time_coverage_end        | 2012-10-22                                    | ISO 8601 Date/Time |                   |                                               | Set in ERDDAP automatically when source is files |
| time_coverage_resolution | P1D                                           | ISO 8601 Duration  |                   |                                               |                                                  |
| title                    |                                               | text               |                   |                                               | Required in ERDDAP                               |
| use_constraints          |                                               | text               | ✓                 |                                               | Not from ACDD/CF                                 |

These can be repeated with different instrument numbers, eg:

| field name                     | example value | data type | bilingual support | codelist options | Notes            |
| ------------------------------ | ------------- | --------- | ----------------- | ---------------- | ---------------- |
| instrument_1_id                |               | text      |                   |                  | Not from ACDD/CF |
| instrument_1_description       |               | text      |                   |                  | Not from ACDD/CF |
| instrument_1_description_other |               | text      |                   |                  | Not from ACDD/CF |
| instrument_1_type              |               | text      |                   |                  | Not from ACDD/CF |
| instrument_1_version           |               | text      |                   |                  | Not from ACDD/CF |

## Codelists

### Party Role Codes

person, group, institution, position

### Role Codes

resourceProvider, custodian, owner, user, distributor, originator, pointOfContact, principalInvestigator, processor, publisher, author, sponsor, coAuthor, collaborator, editor, mediator, rightsHolder, contributor, funder, stakeholder

### Progress Codes

deprecated, proposed, withdrawn, notAccepted, accepted, valid, tentative, superseded, retired, pending, final, underDevelopment, required, planned, onGoing, obsolete, historicalArchive, completed

### EOV codelist

oxygen, nutrients, nitrate, phosphate, silicate, inorganicCarbon, dissolvedOrganicCarbon, seaSurfaceHeight, seawaterDensity, potentialTemperature, potentialDensity, speedOfSound, seaIce, seaState, seaSurfaceSalinity, seaSurfaceTemperature, subSurfaceCurrents, subSurfaceSalinity, subSurfaceTemperature, surfaceCurrents

## Running tests

```bash
cd metadata_xml
python -m unittest tests.py

```

Or if you have Docker installed, from this directory:
`sh run_docker_tests.sh`
