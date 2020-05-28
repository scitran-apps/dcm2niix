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
FROM neurodebian:xenial
MAINTAINER Michael Perry <lmperry@stanford.edu>

# Install packages
RUN apt-get update -qq \
    && apt-get install -y \
    git \
    curl \
    build-essential \
    cmake \
    pkg-config \
    libgdcm-tools \
    bsdtar \
    unzip \
    pigz \
    gzip \
    wget \
    jq \
    python-pip \
    python-nibabel

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt && rm -rf /root/.cache/pip

# Compile DCM2NIIX from source
ENV DCMCOMMIT=485c387c93bbca3b29b93403dfde211c4bc39af6
RUN curl -#L  https://github.com/rordenlab/dcm2niix/archive/$DCMCOMMIT.zip | bsdtar -xf- -C /usr/local
WORKDIR /usr/local/dcm2niix-${DCMCOMMIT}/build
RUN cmake -DUSE_OPENJPEG=ON -MY_DEBUG_GE=ON ../ && \
    make && \
    make install

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}

## Copy in fix_dcm_vols
ENV FIXDCMCOMMIT=918ee3327174c3c736e7b3839a556e0a709730c8
RUN curl -#L https://raw.githubusercontent.com/VisionandCognition/NHP-Process-MRI/$FIXDCMCOMMIT/bin/fix_dcm_vols > ${FLYWHEEL}/fix_dcm_vols.py
RUN chmod +x ${FLYWHEEL}/fix_dcm_vols.py

# Add executables
COPY run run_dcm2niix metadata.py coil_combine.py ./
RUN chmod 777 run metadata.py coil_combine.py fix_dcm_vols.py

# Create Flywheel User
RUN adduser --disabled-password --gecos "Flywheel User" flywheel

# Add manifest
COPY manifest.json ${FLYWHEEL}/manifest.json

# Configure entrypoint
ENTRYPOINT ["/flywheel/v0/run"]
