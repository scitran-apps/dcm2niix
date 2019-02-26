# Creates docker container that runs dcm2niix
#
# Example usage:
#   docker run --rm -ti \
#       -v <someDirWithDicoms>:/flywheel/v0/input/dcm2niix_input \
#       -v <emptyOutputFolder>:/flywheel/v0/output \
#       scitran/dcm2niix
#
#

# Start with neurodebian image
FROM neurodebian:trusty
MAINTAINER Michael Perry <lmperry@stanford.edu>

# Install packages
RUN apt-get update -qq \
    && apt-get install -y \
    git \
    curl \
    build-essential \
    cmake \
    pkg-config \
    libgdcm-tools=2.2.4-1.1ubuntu4 \
    bsdtar \
    unzip \
    pigz \
    gzip \
    wget \
    jq \
    python

# Compile DCM2NIIX from source
ENV DCMCOMMIT=3d74eabceeaab57213e9ffef91c96de128ac5150
RUN curl -#L  https://github.com/rordenlab/dcm2niix/archive/$DCMCOMMIT.zip | bsdtar -xf- -C /usr/local
WORKDIR /usr/local/dcm2niix-${DCMCOMMIT}/build
RUN cmake -DUSE_OPENJPEG=ON -MY_DEBUG_GE=ON ../ && \
    make && \
    make install

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}

# Add executables
COPY run run_dcm2niix metadata.py ./
RUN chmod +x run metadata.py

# Create Flywheel User
RUN adduser --disabled-password --gecos "Flywheel User" flywheel

# Add manifest
COPY manifest.json ${FLYWHEEL}/manifest.json

# Configure entrypoint
ENTRYPOINT ["/flywheel/v0/run"]
