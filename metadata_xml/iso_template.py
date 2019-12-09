#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import re
from lxml import etree
import os
from datetime import date
from metadata_xml.validation import validate, get_alternate_language
from xml.sax.saxutils import escape

TEMPLATE_FILE = './cioos_template.jinja2'


class ValidationError(Exception):
    pass


def get_instruments_from_record(record):
    ''' converts flat instrument variables to a nested dict
        See test for example

        This function is used within the Jinja template
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

    def get_alternate_text(key):
        # for this key, eg title, look for 3 letter suffixes using record
        matching_keys = list(filter(lambda k: re.search("^" + key + r"_\w{3}$",
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
                            .format(default_language, key, "_"
                                    + default_language))

        return tuples_with_lang_code
    return get_alternate_text


def pretty_xml(ugly_xml):
    'Beautifies an XML string, adds the XML declaration line'
    parser = etree.XMLParser(ns_clean=True,
                             # Keeping in comments for now
                             remove_comments=True,
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


def sanitize_record(record):
    ''' escape all strings in dict so its suitable for XML. Not recursive
        also removes empty keys
     '''
    out = {}
    for key, val in record.items():
        if isinstance(val, str):
            out[key] = escape(val)
        else:
            if val:
                out[key] = val
    return out


def convert_record_to_xml(record):
    '''Takes a Jinja template file and a dictionary and
        outputs XML
    '''
    this_dir = os.path.dirname(os.path.realpath(__file__))

    template_loader = FileSystemLoader(searchpath=this_dir)
    template_env = Environment(loader=template_loader, trim_blocks=True,
                               lstrip_blocks=True)

    template = template_env.get_template(TEMPLATE_FILE)

    get_alternate_text = get_alternate_text_wrapper(record)
    language_alt = get_alternate_language(record)
    template_env.filters['get_alternate_text'] = get_alternate_text
    template_env.globals.update(get_alternate_text=get_alternate_text)
    template_env.globals.update(
        instruments=get_instruments_from_record(record),
        date_today=date.today().strftime("%Y-%m-%d"),
        language_alt=language_alt)

    xml = template.render({"record": record})
    return xml


def iso_template(record, use_validation=True):
    'The main function. `use_validation` flag provided for testing'

    # remove empty fields and escape special chars
    record = sanitize_record(record)

    if use_validation:
        errors = validate(record)
        if errors:
            raise ValidationError(errors)

    xml = pretty_xml(convert_record_to_xml(record))

    return xml
