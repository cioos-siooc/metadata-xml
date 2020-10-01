#!/usr/bin/env python3

'''

 Code to handle command line usage of this module
 eg `python -m metadata_xml my_record.yaml`

 Creates an XML file with same base name as Yaml file
 (eg, record.yaml -> record.xml)

'''
from metadata_xml.template_functions import metadata_to_xml
import argparse
import yaml
import os

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='metadata_xml',
                                     description="Convert yaml into CIOOS xml")

    parser.add_argument(
        '-f', type=str, dest="yaml_file",
        help="Enter filename of yaml file.", required=True)

    args = parser.parse_args()
    filename = args.yaml_file

    with open(args.yaml_file) as stream:
        record = yaml.safe_load(stream)

    basename = os.path.basename(filename)
    print("Input filename as: "+basename)

    xml = metadata_to_xml(record)

    pre, ext = os.path.splitext(filename)
    yaml_filename = f'{pre}.xml'
    file = open(yaml_filename, "w")
    file.write(xml)
    print("Wrote " + file.name)
