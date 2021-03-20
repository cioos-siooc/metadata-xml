#!/usr/bin/env python

from distutils.core import setup

setup(name='metadata_xml',
      version='0.1',
      description='Python module for converting ACDD style metadata into the '
      + 'CIOOS ISO profile',
      url='https://github.com/cioos-siooc/metadata-xml',
      packages=['metadata_xml'],
      package_data={'metadata_xml': ['iso19115-cioos-template/*.j2']},
      include_package_data=True,

      install_requires=['Jinja2 == 2.11.3',
                        'PyYAML == 5.1.2',
                        ]

      )
