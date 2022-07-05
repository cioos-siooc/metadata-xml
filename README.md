# metadata-xml

[![Create and validate and XML file](https://github.com/cioos-siooc/metadata-xml/actions/workflows/python.yaml/badge.svg)](https://github.com/cioos-siooc/metadata-xml/actions/workflows/python.yaml)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

`metadata-xml` is a Python3 package for converting metadata records defined using
ACDD-style field names into XML that fits into the [CIOOS](https://www.cioos.ca)
metadata profile.

It can be used as a command line tool, or imported into other Python code.

## Installation

1. Setup and activate a new Python 3 environment
2. From this directory, run:

   `pip install .`

3. To upgrade this package if you have already installed it, use:

   `pip install . --upgrade`

   - or If you are developing this package, to avoid reinstalling each time,
     use:

     `pip install -e .`

## Command line usage

To convert a Yaml file to XML, run:

`python -m metadata_xml -f <yaml_file_path> -o <optional_destination_folder>`

eg:

`python -m metadata_xml -f sample_records/record.yaml`

## Importing into other Python projects

You can perform the yaml to XML conversion in other projects this way:

```python
from metadata_xml.template_functions import metadata_to_xml

record = {...}
xml = metadata_to_xml(record)
```

and add to your requirements.txt:

`git+git://github.com/cioos-siooc/metadata-xml.git`

## YAML Metadata format

See `sample_records/record.yaml` for an example. Most text fields have the option to be bilingual, eg:

```yaml
   comment: just in the primary language

   # -- or --

   comment:
      en: comment in english
      fr: comment in french
```

## Codelists

### Party Role Codes

person, group, institution, position

### Role Codes

resourceProvider, custodian, owner, user, distributor, originator, pointOfContact, principalInvestigator, processor, publisher, author, sponsor, coAuthor, collaborator, editor, mediator, rightsHolder, contributor, funder, stakeholder

### Progress Codes

deprecated, proposed, withdrawn, notAccepted, accepted, valid, tentative, superseded, retired, pending, final, underDevelopment, required, planned, onGoing, obsolete, historicalArchive, completed

### EOV codelist

dissolvedOrganicCarbon, fishAbundanceAndDistribution, hardCoralCoverAndComposition, inorganicCarbon, invertebrateAbundanceAndDistribution, macroalgalCanopyCoverAndComposition, marineDebris, marineTurtlesBirdsMammalsAbundanceAndDistribution, microbeBiomassAndDiversity, nitrousOxide, nutrients, oceanColour, oceanSound, oceanSurfaceHeatFlux, oceanSurfaceStress, other, oxygen, particulateMatter, phytoplanktonBiomassAndDiversity, seagrassCoverAndComposition, seaIce, seaState, seaSurfaceHeight, seaSurfaceSalinity, seaSurfaceTemperature, stableCarbonIsotopes, subSurfaceCurrents, subSurfaceSalinity, subSurfaceTemperature, surfaceCurrents, transientTracers, zooplanktonBiomassAndDiversity

## Running tests

`sh run_docker_tests.sh`
