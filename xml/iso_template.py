#!/usr/bin/env python3

# This is the most basic code needed to load the template and write XML

# From this directory, run: python iso_template.py


from jinja2 import Environment, FileSystemLoader
import yaml
import re
from lxml import etree


# eg if we have: {title_fra:"le title"}
# get_alternate_text('title') will return [("fra", "le title")]
# returns an array because it supports multilingual, not just bilingual
def get_alternate_text_wrapper(record):
    default_language = record['language']
    if not default_language:
        raise Exception("Variable language is required")

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
        if(default_language in matching_languages):
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
    xml_pretty_str = etree.tostring(tree.getroot(),
                                    pretty_print=True,
                                    xml_declaration=True,
                                    encoding='UTF-8')
    return xml_pretty_str


def iso_template(template_file, yaml_file):
    '''Takes a Jinja template file and a yaml file in this directory and
    outputs XML'''
    TEMPLATE_FOLDER = "./"

    template_loader = FileSystemLoader(searchpath=TEMPLATE_FOLDER)
    template_env = Environment(loader=template_loader, trim_blocks=True,
                               lstrip_blocks=True)

    template = template_env.get_template(template_file)

    with open(yaml_file) as stream:
        yaml_data = yaml.safe_load(stream)
        data = {"record": yaml_data}
        get_alternate_text = get_alternate_text_wrapper(yaml_data)
        template_env.filters['get_alternate_text'] = get_alternate_text
        template_env.globals.update(get_alternate_text=get_alternate_text)

        xml = template.render(data)

    return xml


# the record input as yaml file
yaml_file_path = "record.yaml"

# the jinja template file
template_path = "cioos_template.xml"

# The output file
xml_file_path = "record.xml"

xml = pretty_xml(iso_template(template_path,  yaml_file_path))
file = open(xml_file_path, "wb")
file.write(xml)
print("Wrote " + xml_file_path)
