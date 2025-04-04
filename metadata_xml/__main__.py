#!/usr/bin/env python3

"""

Code to handle command line usage of this module
eg `python -m metadata_xml my_record.yaml`

Creates an XML file with same base name as Yaml file
(eg, record.yaml -> record.xml)

"""

import argparse
import os

import yaml

from metadata_xml.template_functions import metadata_to_xml


def main():
    """Handles argparse and calls metadata_to_xml()"""
    parser = argparse.ArgumentParser(
        prog="metadata_xml", description="Convert yaml into CIOOS xml"
    )

    parser.add_argument(
        "-f",
        type=str,
        dest="yaml_file",
        help="Enter filename of yaml file.",
        required=True,
    )

    parser.add_argument(
        "-o",
        type=str,
        dest="output_folder",
        help="Enter the folder to write your xml file to."
        + "Defaults to the source file's directory.",
        required=False,
    )

    args = parser.parse_args()
    filename = args.yaml_file
    output_folder = args.output_folder

    with open(args.yaml_file) as stream:
        record = yaml.safe_load(stream)

    basename = os.path.basename(filename)
    print("Input filename as: " + basename)

    xml_string = metadata_to_xml(record)

    pre = os.path.splitext(basename)[0]
    path_with_file = os.path.splitext(filename)[0]

    if output_folder:
        yaml_filename = f"{output_folder}/{pre}.xml"
    else:
        yaml_filename = f"{path_with_file}.xml"

    file = open(yaml_filename, "w")
    file.write(xml_string)
    print("Wrote " + file.name)


if __name__ == "__main__":
    main()
