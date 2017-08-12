# Creates docker container that runs dcm2niix
#
# Example usage:
#   docker run --rm -ti \
#       -v <someDirWithDicoms>:/flywheel/v0/input/dcm2niix \
#       -v <emptyOutputFolder>:/flywheel/v0/output \
#       scitran/dcm2niix <optional_flags>
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
    wget

# Compile DCM2NIIX from source
ENV DCMCOMMIT=7fb7bcc56348f3a61012bba851bfa11057e55dc1
RUN curl -#L  https://github.com/rordenlab/dcm2niix/archive/$DCMCOMMIT.zip | bsdtar -xf- -C /usr/local
WORKDIR /usr/local/dcm2niix-${DCMCOMMIT}/build
RUN cmake -DUSE_OPENJPEG=ON ../ && \
    make && \
    make install

# Install jq to parse manifest
RUN wget -N -qO- -O /usr/bin/jq http://stedolan.github.io/jq/download/linux64/jq
RUN chmod +x /usr/bin/jq

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}

# Add executables
COPY run ${FLYWHEEL}/run

# Add manifest
COPY manifest.json ${FLYWHEEL}/manifest.json

# Configure entrypoint
ENTRYPOINT ["/flywheel/v0/run"]
