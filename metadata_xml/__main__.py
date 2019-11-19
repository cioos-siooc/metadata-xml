#!/usr/bin/env python3

'''

 Code to handle command line usage of this module
 eg `python -m metadata_xml my_record.yaml`

 Creates an XML file with same base name as Yaml file
 (eg, record.yaml -> record.xml)

'''


import os
import yaml
import argparse

from metadata_xml.iso_template import iso_template

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='metadata_xml',
                                     description="Convert yaml into CIOOS xml")

    parser.add_argument(
        '-f', type=str, dest="yaml_file",
        help="Enter filename of yaml file.", required=True)

    args = parser.parse_args()
    filename = args.yaml_file

    basename = os.path.basename(filename)
    print("Input filename as: "+basename)

    with open(args.yaml_file) as stream:
        yaml_data = yaml.safe_load(stream)

        xml = iso_template(yaml_data, use_validation=True)
        file = open(basename.split('.')[0] + ".xml", "w")
        file.write(xml)
        print("Wrote " + file.name)
