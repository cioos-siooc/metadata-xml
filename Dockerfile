# Run tests using docker
FROM python:3
WORKDIR /repo
COPY . .
RUN pip install . 
RUN cd metadata_xml && python -m unittest tests.py

