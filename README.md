# metadata-xml

[![Create and validate and XML file](https://github.com/cioos-siooc/metadata-xml/actions/workflows/python.yaml/badge.svg)](https://github.com/cioos-siooc/metadata-xml/actions/workflows/python.yaml)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

`metadata-xml` is a Python3 package for converting metadata records defined using
ACDD-style field names into XML that fits into the [CIOOS](https://www.cioos.ca)
metadata profile.

It can be used as a command line tool, or imported into other Python code.

## Installation

Install via pip with:

```
pip install https://github.com/cioos-siooc/metadata-xml.git
```

## Development Installation

1. Install the environment and package manager uv: https://docs.astral.sh/uv/getting-started/installation/
2. From this directory, run:

   `uv sync --dev`

## Command line usage

To convert a Yaml file to XML, run:

`uv run python -m metadata_xml -f <yaml_file_path> -o <optional_destination_folder>`

eg:

`uv run python -m metadata_xml -f sample_records/record.yml`

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

You need first to unzip the file `cioos-schema.zip` which contains all the necessary schemas within the base directory.

Then run:

`uv run pytest .`
