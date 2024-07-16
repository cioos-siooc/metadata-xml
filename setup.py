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

      install_requires=['markupsafe == 2.0.1',
                        'Jinja2 == 2.10.3',
                        'PyYAML >= 6.0.1',
                        'yattag == 1.14.0',
                        'validators == 0.20.0'
                        ]

      )
