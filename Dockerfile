# Run tests using docker
FROM python:3
WORKDIR /repo

RUN apt update && apt install -y libxml2-utils

COPY validate.sh .
COPY cioos-schema.zip .
RUN unzip -q cioos-schema.zip

COPY setup.py .
COPY ./metadata_xml ./metadata_xml
COPY sample_records ./sample_records
RUN pip install .

RUN python -m metadata_xml -f sample_records/record.yml
# make sure it validates with the schema
RUN sh validate.sh sample_records/record.xml
