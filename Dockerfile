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
    gzip

ENV DCM2NIIDIR /root/.dcm2nii
RUN mkdir -p $DCM2NIIDIR
COPY dcm2nii.ini $DCM2NIIDIR/dcm2nii.ini

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}

# Add executables
COPY run ${FLYWHEEL}/run
ADD https://raw.githubusercontent.com/scitran/utilities/daf5ebc7dac6dde1941ca2a6588cb6033750e38c/metadata_from_gear_output.py ${FLYWHEEL}/metadata_create.py
RUN chmod +x ${FLYWHEEL}/metadata_create.py

# Add manifest
COPY manifest.json ${FLYWHEEL}/manifest.json

# Configure entrypoint
ENTRYPOINT ["/flywheel/v0/run"]
