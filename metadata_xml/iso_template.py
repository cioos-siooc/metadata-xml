#!/usr/bin/env python3

# From this directory, run: python iso_template.py


from jinja2 import Environment, FileSystemLoader
import yaml
import re
from lxml import etree
import os
import argparse

TEMPLATE_FILE = './cioos_template.jinja2'


class ValidationError(Exception):
    pass


def get_instruments_from_record(record):
    ''' converts flat instrument variables to a nested dict
        See test for example
    '''
    instruments = {}
    for key, val in record.items():
        matches_instrument = re.search(r'^instrument_(\d)+_?(\w+)?', key)
        if not matches_instrument:
            continue

        instrument_num = matches_instrument[1]
        if instrument_num not in instruments:
            instruments[instrument_num] = {}

        instrument = instruments[instrument_num]

        instrument_field = matches_instrument[2]

        matches_sensor = re.search(r'^sensor_(\d)+_?(\w+)?', instrument_field)
        if matches_sensor:
            sensor_num = matches_sensor[1]
            sensor_field = matches_sensor[2]
            if 'sensor' not in instrument:
                instrument['sensor'] = {}
            if sensor_num not in instrument['sensor']:
                instrument['sensor'][sensor_num] = {}

            instrument['sensor'][sensor_num][sensor_field] = val
        else:
            instrument[instrument_field] = val

    return instruments


def check_mandatory_fields(record):
    # could add more logic here
    mandatory_fields = [
        'id',
        'title',
        'summary',
        'language',
        'language_country',
        'keywords',
        'date_created',
        'creator_name',
        'creator_url',
        'creator_email',
        'institution',
        'project',
        'acknowledgement',
        'contributor_name',
        'contributor_role',
        # 'scope_code',
        # 'platform_id',
        # 'platform_role',
        # 'platform_id_authority'
    ]
    pass_test = 1
    missing_fields = []
    for field in mandatory_fields:
        if field in record:
            if record[field] is None:
                pass_test = 0
                missing_fields.append(field)
        elif field not in record:
            pass_test = 0
            missing_fields.append(field)

    if pass_test is 0:
        raise ValidationError("Missing required fields/values: '{}'"
                              .format(missing_fields))
    return pass_test


def get_alternate_text_wrapper(record):
    """ Given a dict, return a function that will take a key and return all
        the keys for alternate languages

        This function is used inside the Jinja template

        eg if we have: {title_fra:"le title"}
        get_alternate_text('title') will return [("fra", "le title")]
        returns an array because it supports multilingual, not just bilingual
    """
    if 'language' not in record:
        raise ValidationError("missing variable 'language' in record")

    default_language = record['language']

    if not default_language:
        raise ValidationError("Variable language is required")

    def get_alternate_text(key):
        # for this key, eg title, look for 3 letter suffixes using record
        matching_keys = list(filter(lambda k: re.search("^" + key + "_\w{3}$",
                                                        k[0]), record.items()))
        # formats tuples like [('fra','les courants')]
        tuples_with_lang_code = list(map(lambda k: (k[0][-3:], k[1]),
                                         matching_keys))

        # list of all the languages given for this key
        matching_languages = list(map(lambda k: k[0], tuples_with_lang_code))

        # eg if language="fra" there cant be a title_fra variable
        if (default_language in matching_languages):
            raise Exception('Default language is "{}", field "{}" '
                            'cannot have suffix "{}"'
                            .format(default_language, key, "_" +
                                    default_language))

        return tuples_with_lang_code
    return get_alternate_text


def pretty_xml(ugly_xml):
    'Beautifies an XML string, adds the XML declaration line'
    parser = etree.XMLParser(ns_clean=True,
                             # Keeping in comments for now
                             remove_comments=False,
                             remove_blank_text=True)

    tree = etree.ElementTree(etree.fromstring(ugly_xml, parser=parser))
    xml_pretty_str = etree.tostring(
        tree,
        pretty_print=True,
        # not using xml_declaration as it produces single quotes
        # which the validator doesnt like
        doctype='<?xml version="1.0" encoding="utf-8"?>',
        encoding="unicode")
    return xml_pretty_str


def iso_template(record):
    '''Takes a Jinja template file and a dictionary and
    outputs XML'''

    this_dir = os.path.dirname(os.path.realpath(__file__))

    template_loader = FileSystemLoader(searchpath=this_dir)
    template_env = Environment(loader=template_loader, trim_blocks=True,
                               lstrip_blocks=True)

    template = template_env.get_template(TEMPLATE_FILE)

    check_mandatory_fields(record)
    get_alternate_text = get_alternate_text_wrapper(record)
    template_env.filters['get_alternate_text'] = get_alternate_text
    template_env.globals.update(get_alternate_text=get_alternate_text)
    template_env.globals.update(
        instruments=get_instruments_from_record(record))

    xml = pretty_xml(template.render({"record": record}))

    return xml


if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description="Convert yaml and Jinja template into xml.")
    parser.add_argument('-f', type=str, dest="string", default="record.yaml",
                        help="Enter filename of yaml file. (default = record.yaml)")
    args = parser.parse_args()
    filename = args.string
    print("Input filename as: "+filename.split('.')[0])
    with open(args.string) as stream:
        yaml_data = yaml.safe_load(stream)

        xml = iso_template(yaml_data)
        file = open(filename.split('.')[0] + ".xml", "w")
        file.write(xml)
        print("Wrote " + file.name)
