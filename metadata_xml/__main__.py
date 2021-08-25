#!/usr/bin/env python3

"""

 Code to handle command line usage of this module
 eg `python -m metadata_xml my_record.yaml`

 Creates an XML file with same base name as Yaml file
 (eg, record.yaml -> record.xml)

"""

import os

import argparse
import yaml
from metadata_xml.template_functions import metadata_to_xml


def main():
    """Handles argparse and calls metadata_to_xml()"""
    parser = argparse.ArgumentParser(prog='metadata_xml',
                                     description="Convert yaml into CIOOS xml")

    parser.add_argument(
        '-f', type=str, dest="yaml_file",
        help="Enter filename of yaml file.", required=True)

    parser.add_argument(
        '-o', type=str, dest="output_folder",
        help="Enter the folder to write your xml file to." +
        "Defaults to the source file's directory.", required=False)

    parser.add_argument(
        '--multiple-platforms', '-m', dest='multiple_platforms', action='store_true',
        help="YAML source file formatted to contain multiple platforms instead of one.",
        required=False)

    parser.add_argument(
        '--encoding', '-e', type=str, default='utf-8', dest='encoding',
        help="The encoding of the YAML source file, default: utf-8",
        required=False)

    parser.add_argument(
        '--output-encoding', '-w', type=str, default='utf-8', dest='encoding',
        help="The encoding of the XML destination file, default: utf-8",
        required=False)

    args = parser.parse_args()
    filename = args.yaml_file
    output_folder = args.output_folder

    with open(args.yaml_file, encoding=args.encoding) as stream:
        record = yaml.safe_load(stream)

    basename = os.path.basename(filename)
    print("Input filename as: "+basename)

    # rearrange single platform records to be an array of one to allow the 
    # Jinja template to work with 1 or more platforms
    if not args.multiple_platforms:
        record['platform'] = [record['platform']]
    else:
        print("Multiple platform format enabled.")

    xml_string = metadata_to_xml(record)

    pre = os.path.splitext(basename)[0]
    path_with_file = os.path.splitext(filename)[0]

    if output_folder:
        yaml_filename = f'{output_folder}/{pre}.xml'
    else:
        yaml_filename = f'{path_with_file}.xml'

    file = open(yaml_filename, "w", encoding='utf-8')
    file.write(xml_string)
    print("Wrote " + file.name)


if __name__ == '__main__':
    main()
