#!/usr/bin/env python3

# This is the most basic code needed to load the template and write XML

# From this directory, run: python iso_template.py

import jinja2
import yaml


def iso_template(template_file, yaml_file):
    '''Takes a Jinja template file and a yaml file in this directory and
    outputs XML'''
    TEMPLATE_FOLDER = "./"

    templateLoader = jinja2.FileSystemLoader(searchpath=TEMPLATE_FOLDER)
    templateEnv = jinja2.Environment(loader=templateLoader)

    template = templateEnv.get_template(template_file)

    with open(yaml_file) as stream:
        yaml_data = yaml.safe_load(stream)
        outputText = template.render({"record": yaml_data})
    return outputText


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
