#!/usr/bin/env python3

# This is the most basic code needed to load the template and write XML

# From this directory, run: python iso_template.py


from jinja2 import Environment, FileSystemLoader
import yaml
import re


# eg if we have: {title_fr:"le title"}
# get_alternate_text('title') will return [("fr", "le title")]
# returns an array because it supports multilingual, not just bilingual
def get_alternate_text_wrapper(record):
    def get_alternate_text(key):
        # for this key, eg title, look for 3 letter suffixes using record
        matching_keys = list(filter(lambda k: re.search("^" + key + "_\w{3}$",
                                                        k[0]), record.items()))
        # formats tuples like [('fr','les courants')]
        tuples_with_lang_code = list(map(lambda k: (k[0][-3:], k[1]),
                                         matching_keys))
        return tuples_with_lang_code
    return get_alternate_text


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

xml = iso_template(template_path,  yaml_file_path)
file = open(xml_file_path, "w")
print("Wrote " + xml_file_path)
file.write(xml)
