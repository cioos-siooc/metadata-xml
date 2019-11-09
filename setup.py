#!/usr/bin/env python

from distutils.core import setup

setup(name='metadata_xml',
      version='0.1',
      description='Python module for converting ACDD style metadata into the '
      + 'CIOOS ISO profile',
      url='https://github.com/cioos-siooc/metadata-xml',
      packages=['metadata_xml', ],
      include_package_data=True,

      install_requires=['Jinja2 == 2.10.3',
                        'lxml == 4.4.1',
                        'PyYAML == 5.1.2'
                        ]

      )
