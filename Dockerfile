# Run tests using docker
FROM python:3
WORKDIR /repo
COPY . .

RUN apt update && apt install -y libxml2-utils
RUN pip install .
RUN sh docker_init.sh
