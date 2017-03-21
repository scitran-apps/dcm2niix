[![Docker Pulls](https://img.shields.io/docker/pulls/scitran/dcm2niix.svg)](https://hub.docker.com/r/scitran/dcm2niix/)
[![Docker Stars](https://img.shields.io/docker/stars/scitran/dcm2niix.svg)](https://hub.docker.com/r/scitran/dcm2niix/)

## scitran/dcm2niix

This Dockerfile will create a docker image that can execute ```dcm2niix```.

## Options
Options are set in `manifest.json`. Current defaults are set and loaded into the container on build.

### Build the Image
To build the image, either download the files from this repo or clone the repo:
```
docker build --no-cache -t scitran/dcm2niix
```

### Example Usage ###
To run dcm2niix from this container you can do the following:
```
docker run --rm -ti \
    -v </path/to/input/data>:/flywheel/v0/input/source \
    -v </path/to/output>:/flywheel/v0/output \
    scitran/dcm2niix
```
