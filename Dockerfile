# Creates docker container that runs dcm2niix
#
# Example usage:
#   docker run --rm -ti \
#       -v <someDirWithDicoms>:/flywheel/v0/input/source \
#       -v <emptyOutputFolder>:/flywheel/v0/output \
#       scitran/dcm2niix <optional_flags>
#
#

# Start with neurodebian image
FROM neurodebian:trusty
MAINTAINER Michael Perry <lmperry@stanford.edu>

# Install packages
RUN apt-get update \
    && apt-get install -y \
    python \
    dcm2niix \
    pigz \
    unzip \
    gzip \
    libgdcm-tools \
    wget

# Install jq to parse manifest
RUN wget -N -qO- -O /usr/bin/jq http://stedolan.github.io/jq/download/linux64/jq
RUN chmod +x /usr/bin/jq

# Copy config for dcm2nii to default location
COPY dcm2nii.ini /root/dcm2nii.ini

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}

# Add executables
COPY run ${FLYWHEEL}/run

# Add manifest
COPY manifest.json ${FLYWHEEL}/manifest.json

# Configure entrypoint
ENTRYPOINT ["/flywheel/v0/run"]
