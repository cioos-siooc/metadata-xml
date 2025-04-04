#!/usr/bin/env python3

"""

Defines custom functions used by the Jinja template

Also defines metadata_to_xml()

"""

import os
import pathlib
from datetime import date

import validators
from jinja2 import Environment, FileSystemLoader
from yattag import indent

SCHEMA_FOLDER_NAME = "iso19115-cioos-template"


def is_url(val):
    return val and validators.url(val)


def list_or_value_to_list(val):
    """turns a list or a single value into a list"""
    if isinstance(val, list):
        return val
    if val is None:
        return []
    return [val]


def normalize_datestring(datestring):
    """groks date string into ISO8601
    Adopted from Pygeometa,
    https://github.com/geopython/pygeometa/blob/master/pygeometa/core.py
    """

    try:
        if isinstance(datestring, date):
            if datestring.year < 1900:
                datestring2 = "{0.day:02d}.{0.month:02d}.{0.year:4d}".format(datestring)
            else:
                datestring2 = datestring.strftime("%Y-%m-%dT%H:%M:%SZ")
            if datestring2.endswith("T00:00:00Z"):
                datestring2 = datestring2.replace("T00:00:00Z", "")
            return datestring2
        elif isinstance(datestring, int) and len(str(datestring)) == 4:  # year
            return str(datestring)
    except AttributeError:
        raise RuntimeError("Invalid datestring: {}".format(datestring))
    return datestring


def list_all_languages_in_record(record):
    """Lists all languages used, so that we can list all
    languages used in the otherLocale section of XML"""

    def list_keys_in_record(record_subset, all_keys):
        """recursive function, works on nested dict for example"""
        for key, val in record_subset.items():
            if isinstance(val, dict):
                all_keys.append(key)
                list_keys_in_record(val, all_keys)
            else:
                all_keys.append(key)
        return set(all_keys)

    keys_in_record = list_keys_in_record(record, [])

    two_character_keys = list(
        filter(lambda x: (len(x) == 2) and (x != "id"), keys_in_record)
    )
    return sorted(two_character_keys)


def metadata_to_xml(record):
    """Runs steps needed to render the Jinja template"""

    this_directory = pathlib.Path(__file__).parent.absolute()
    schema_path = os.path.join(this_directory, SCHEMA_FOLDER_NAME)

    template_loader = FileSystemLoader(searchpath=schema_path)
    template_env = Environment(
        loader=template_loader, trim_blocks=True, lstrip_blocks=True, autoescape=True
    )

    template_env.globals.update(
        list_all_languages_in_record=list_all_languages_in_record,
        list_or_value_to_list=list_or_value_to_list,
        is_url=is_url,
    )
    template_env.filters["normalize_datestring"] = normalize_datestring
    template = template_env.get_template("main.j2")

    xml_string = template.render({"record": record})
    pretty_string = indent(xml_string)

    return pretty_string
