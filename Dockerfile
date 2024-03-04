# Base container name
ARG BASE_NAME=python:3.11

FROM $BASE_NAME as base

ARG PACKAGE_NAME="lamini-train-orca"

# Install python packages
WORKDIR /app/${PACKAGE_NAME}
COPY ./requirements.txt /app/${PACKAGE_NAME}/requirements.txt

RUN pip install -r requirements.txt

# Copy all files to the container
COPY scripts /app/${PACKAGE_NAME}/scripts
COPY orca /app/${PACKAGE_NAME}/orca
WORKDIR /app/${PACKAGE_NAME}

# Set the entrypoint
RUN chmod a+x /app/${PACKAGE_NAME}/scripts/start.sh

ENV PACKAGE_NAME=$PACKAGE_NAME
ENTRYPOINT ["/app/lamini-train-orca/scripts/start.sh"]



