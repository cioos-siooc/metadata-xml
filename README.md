# metadata-xml

Documentation and code for creating and working with CIOOS metadata XML files

## Using the command line tool

To load a Yaml file, run:

`python metadata_xml/iso_template.py -f <yaml_file_path>`

## To install the metadata_xml python module

`pip install .`

When this package changes, use `pip install . --upgrade` to upgrade

## Using the python module

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

See example .yaml files in this directory for more examples.

    - acknowledgement
    - comment
    - contributor_name
    - creator_email
    - creator_name
    - creator_url
    - date_created
    - date_created
    - date_issued
    - date_issued
    - date_modified
    - date_modified
    - geospatial_lat_max
    - geospatial_lat_min
    - geospatial_lon_max
    - geospatial_lon_min
    - geospatial_vertical_max
    - geospatial_vertical_min
    - history
    - id
    - institution
    - keywords
    - keywords_vocabulary
    - keywords_vocabulary
    - lang_code
    - lang_text
    - language
    - language_country
    - license
    - naming_authority
    - platform_description
    - platform_id
    - platform_id_authority
    - platform_name
    - platform_role
    - progress_code
    - project
    - publisher_country
    - publisher_email
    - publisher_name
    - publisher_url
    - summary
    - time_coverage_duration
    - time_coverage_end
    - time_coverage_resolution
    - time_coverage_start
    - title

These can be repeated with different instrument/sensor numbers, eg:

    - instrument_1_id
    - instrument_1_description
    - instrument_1_description_other
    - instrument_1_type
    - instrument_1_version

    - instrument_1_sensor_1_id
    - instrument_1_sensor_1_description
    - instrument_1_sensor_1_version
