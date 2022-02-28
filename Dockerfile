# Run tests using docker
FROM python:3
WORKDIR /repo
COPY . .

RUN apt update
RUN apt install -y libxml2-utils
RUN sh docker_init.sh
