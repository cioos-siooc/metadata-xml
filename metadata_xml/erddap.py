#!/usr/bin/env python3

'''

Converts a record in yaml format into a chunk of <addAttributes>
to use in erddap

'''

import argparse
from typing import Dict
import yaml


def get_in_language(val, language):
    '''
    Handle optionally bilingual fields that are written without
    specifying language. eg could handle
    comment:"my comment" or comment: { en:"my comment" }
    '''

    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        return val[language]

    return None


def main():
    'Handles argparse stuff and calls yaml_to_erddap()'
    parser = argparse.ArgumentParser(prog='metadata_xml',
                                     description="Convert yaml into CIOOS xml")

    parser.add_argument(
        '-f', type=str, dest="yaml_file",
        help="Enter filename of yaml file.", required=True)

    args = parser.parse_args()
    filename = args.yaml_file

    with open(filename) as stream:
        record = yaml.safe_load(stream)
        xml = yaml_to_erddap(record)
        print(xml)


def yaml_to_erddap(record: Dict):
    'Converts a record to an erddap xml chunk'

    language = record['metadata']['language']

    if not language:
        raise Exception("'language' cannot be empty")

    organizations = []

    for role in record['contact']:
        organization = role.get('organization', {}).get('name')
        if organization:
            organizations = list(set(organizations+[organization]))

    instruments = []

    if record['platform']['instruments']:
        for instrument in record['platform']['instruments']:
            if instrument['id']:
                instruments = list(set(instruments + [str(instrument['id'])]))

    bbox = record['spatial'].get('bbox')

    # get first publisher, ACDD seems to indicate this should be a single value
    publisher = {}
    contributor = {}

    contributor_names = []
    contributor_roles = []
    for contact in record['contact']:
        if 'publisher' in contact['roles']:
            publisher = contact

        if 'orginator' in contact['roles']:
            contributor = contact

        contributor_names.append(contact.get(
            'individual', {}).get('name'))

        # just getting the first role
        contributor_roles.append(contact['roles'][0])

        break

    erddap_globals = {
        #    "infoUrl": "",  # from erddap
        #    "sourceUrl": "",  # from erddap
        #    "Conventions": "",
        #    "acknowledgement": "",
        #    "cdm_data_type": "",
        "comment": get_in_language(record['metadata'].get('comment'), language),
        "contributor_name": ','.join(contributor_names or []),
        "contributor_role": ','.join(contributor_roles or []),
        #    "coverage_content_type": "",
        "creator_email": contributor.get('email'),
        "creator_institution": contributor.get('organization'),
        "creator_name": contributor.get('name'),
        "creator_type": contributor.get('type'),
        "creator_url": contributor.get('url'),
        "date_created": record['identification']['dates'].get('creation'),
        #    "date_issued": "",
        #    "date_metadata_modified": "",
        #    "date_modified": "",
        "geospatial_bounds":
        record['spatial']['polygon'] if not bbox else None,
        #    "geospatial_bounds_crs": "",
        #    "geospatial_bounds_vertical_crs": "",
        "geospatial_lat_max": bbox[3] if bbox else None,
        "geospatial_lat_min": bbox[1] if bbox else None,
        "geospatial_lon_max": bbox[0] if bbox else None,
        "geospatial_lon_min": bbox[2] if bbox else None,
        "geospatial_vertical_max": record['spatial']['vertical'][1],
        "geospatial_vertical_min": record['spatial']['vertical'][0],
        #    "geospatial_vertical_positive": "",
        #    "geospatial_vertical_resolution": "",
        #    "geospatial_vertical_units": "",
        #    "history": "",
        #    "id": ""
        "institution": ','.join(organizations or []),
        "instrument": ','.join(instruments or []),
        #    "instrument_vocabulary": "",
        "keywords": ','.join(list(set(
            record['identification']['keywords']['default'][language] +
            record['identification']['keywords']['eov']))),
        #    "keywords_vocabulary": "",
        "license": record.get('use_constraints',
                              {}).get('licence', {}).get('title'),
        #    "metadata_link": "",
        #    "naming_authority": "",
        "platform": record['platform']['name'],
        #    "platform_vocabulary": "",
        #    "processing_level": "",
        #    "product_version": "",
        #    "program": "",
        #    "project": "",
        "publisher_email":
        publisher.get('organization', {}).get('email') or
        publisher.get('individual', {}).get('email'),
        "publisher_institution": publisher.get('organization', {}).get('name'),
        "publisher_name":
        publisher.get('individual', {}).get('name') or
        publisher.get('organization', {}).get('name'),
        #    "publisher_type": "",
        "publisher_url": publisher.get('organization', {}).get('url'),
        #    "references": "",
        #    "source": "",
        #    "standard_name_vocabulary": "",
        "summary":
            get_in_language(record['identification']['abstract'][language],
                            language),
        #    "time_coverage_duration": "",
        #    "time_coverage_end": "",
        #    "time_coverage_resolution": "",
        #    "time_coverage_start": "",
        "title": get_in_language(record['identification']['title'][language],
                                 language),
        #    "Metadata_Convention": ""
    }

    xml_snippet = "<addAttributes>\n"

    for key, value in erddap_globals.items():
        if value:
            line = f'\t<att name="{key}">{value}</att>'
            xml_snippet = xml_snippet+line+"\n"
    xml_snippet = xml_snippet + "</addAttributes>"

    return xml_snippet


if __name__ == '__main__':
    main()
