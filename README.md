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

## List of fields

These are the ACDD style keywords that you can use in your record.

For the fields that are text, you can add on '\_fra' or '\_eng' to input the alternate language.

See example .yaml files in the 'sample_records' directory for more examples.

- acknowledgement
- comment
- contributor_name
- contributor_role
- creator_email
- creator_name
- creator_url
- data_maintenance_note
- date_created
- date_issued
- date_modified
- distributor_name
- erddap_dataset_url
- geospatial_bounds
- geospatial_lat_max
- geospatial_lat_min
- geospatial_lon_max
- geospatial_lon_min
- geospatial_vertical_max
- geospatial_vertical_min
- history
- id
- institution
- keywords_vocabulary
- keywords
- language
- naming_authority
- platform_id_authority
- platform_id
- platform_name
- platform_role
- progress_code
- project
- publisher_country
- publisher_email
- publisher_name
- publisher_url
- standard_name_vocabulary
- summary
- time_coverage_duration
- time_coverage_end
- time_coverage_resolution
- time_coverage_start
- title
- use_constraints

These can be repeated with different instrument/sensor numbers, eg:

- instrument_1_id
- instrument_1_description
- instrument_1_description_other
- instrument_1_type
- instrument_1_version

- instrument_1_sensor_1_id
- instrument_1_sensor_1_description
- instrument_1_sensor_1_version
