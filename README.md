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

| field name               | example value                                 | data type          | bilingual support | codelist options                              | Convention |
| ------------------------ | --------------------------------------------- | ------------------ | ----------------- | --------------------------------------------- | ---------- |
| comment                  |                                               | text               | ✓                 |                                               | ACDD       |
| acknowledgement          |                                               | text               | ✓                 |                                               | ACDD       |
| contributor_name         |                                               | text               |                   |                                               | ACDD       |
| contributor_role         | sponsor                                       | text               |                   | [Role Codes](#role-codes)                     | ACDD       |
| creator_email            | nobody@example.com                            | email              |                   |                                               | ACDD       |
| creator_name             |                                               | text               |                   |                                               | ACDD       |
| creator_url              | <http://example.com>                          | text               |                   |                                               | ACDD       |
| creator_type             | person                                        | text               |                   | Codelist                                      | ACDD       |
| data_maintenance_note    |                                               | text               | ✓                 |                                               | CIOOS      |
| date_created             | 2010-01-22                                    | ISO 8601 Date/Time |                   |                                               | ACDD       |
| date_issued              | 2010-01-23                                    | ISO 8601 Date/Time |                   |                                               | ACDD       |
| date_modified            | 2010-01-24                                    | ISO 8601 Date/Time |                   |                                               | ACDD       |
| distributor_name         | distributor name                              | text               |                   |                                               | ACDD       |
| erddap_dataset_url       | <http://example.com/erddap/tabledap/abc.html> | URL                |                   |                                               | CIOOS      |
| geospatial_bounds        | 0,0 100,0 100,100 0,100                       |                    |                   |                                               | ACDD       |
| geospatial_lat_max       |                                               | Numeric            |                   |                                               | ACDD       |
| geospatial_lat_min       |                                               | Numeric            |                   |                                               | ACDD       |
| geospatial_lon_max       |                                               | Numeric            |                   |                                               | ACDD       |
| geospatial_lon_min       |                                               | Numeric            |                   |                                               | ACDD       |
| geospatial_vertical_max  |                                               | Numeric            |                   |                                               | ACDD       |
| geospatial_vertical_min  |                                               | Numeric            |                   |                                               | ACDD       |
| history                  |                                               | text               | ✓                 |                                               | ACDD       |
| id                       | 12345                                         | text               |                   |                                               | ACDD       |
| institution              |                                               | text               |                   |                                               | ACDD       |
| keywords_vocabulary      |                                               | text               | ✓                 |                                               | ACDD       |
| keywords                 |                                               | text               | ✓                 | At least one of [EOV codelist](#eov-codelist) | ACDD       |
| language                 | eng                                           | text               |                   | fra or eng                                    | CIOOS      |
| naming_authority         |                                               | text               | ✓                 |                                               | ACDD       |
| platform_id_authority    |                                               | text               | ✓                 |                                               | CIOOS      |
| platform_id              |                                               | text               |                   |                                               | IOOS       |
| platform_name            |                                               | text               |                   |                                               | IOOS       |
| platform_role            | author                                        | text               |                   | [Role Codes](#role-codes)                     | CIOOS      |
| progress_code            | onGoing                                       | text               |                   | [Progress Codes](#progress-codes)             | CIOOS      |
| project                  |                                               | text               | ✓                 |                                               | ACDD       |
| publisher_country        |                                               | text               | ✓                 |                                               | IOOS       |
| publisher_email          | nobody@example.com                            | email              |                   |                                               | ACDD       |
| publisher_institution    |                                               | text               |                   |                                               | ACDD       |
| publisher_name           |                                               | text               |                   |                                               | ACDD       |
| publisher_url            |                                               | URL                |                   |                                               | ACDD       |
| publisher_type           | group                                         | text               |                   | [Party Role Codes](#party-role-codes)         | ACDD       |
| summary                  |                                               | text               |                   |                                               | ACDD       |
| time_coverage_duration   | P1D                                           | ISO 8601 Duration  |                   |                                               | ACDD       |
| time_coverage_start      | 2012-10-21                                    | ISO 8601 Date/Time |                   |                                               | ACDD       |
| time_coverage_end        | 2012-10-22                                    | ISO 8601 Date/Time |                   |                                               | ACDD       |
| time_coverage_resolution | P1D                                           | ISO 8601 Duration  |                   |                                               | ACDD       |
| title                    |                                               | text               |                   |                                               | ACDD       |
| use_constraints          |                                               | text               | ✓                 |                                               | CIOOS      |

These can be repeated with different instrument numbers, eg:

| field name               | example value | data type | bilingual support | codelist options | Notes |
| ------------------------ | ------------- | --------- | ----------------- | ---------------- | ----- |
| instrument_1_id          |               | text      |                   |                  | CIOOS |
| instrument_1_description |               | text      |                   |                  | CIOOS |
| instrument_1_type        |               | text      |                   |                  | CIOOS |
| instrument_1_version     |               | text      |                   |                  | CIOOS |

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
