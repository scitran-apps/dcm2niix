[![Docker Pulls](https://img.shields.io/docker/pulls/scitran/dcm2niix.svg)](https://hub.docker.com/r/scitran/dcm2niix/)
[![Docker Stars](https://img.shields.io/docker/stars/scitran/dcm2niix.svg)](https://hub.docker.com/r/scitran/dcm2niix/)

## scitran/dcm2niix

Build context for a [Flywheel Gear](https://github.com/flywheel-io/gears/tree/master/spec) to execute ```dcm2niix```.

### Description
Chris Rorden's [dcm2niiX](https://www.nitrc.org/projects/dcm2nii) is a popular tool for converting images from the complicated formats used by scanner manufacturers (DICOM, PAR/REC) to the simple NIfTI format used by many scientific tools. dcm2niix works for all modalities (CT, MRI, PET, SPECT) and sequence types.

### Build the Image
To build the image, either download the files from this repo or clone the repo:
```
docker build --no-cache -t scitran/dcm2niix
```

### Inputs
The input to this gear can be either a zip, a tgz, or a directory containing DICOMs.

### Options
Default options are set in `manifest.json` and copied to the container on build. Defaults are then loaded by the `run` script when the algorithm is executed.

### Example Usage
To run dcm2niix locally from this container you can do the following:
*Ensure your input file is in it's own directory.*
```
docker run --rm -ti \
    -v </path/to/input/data_dir>:/flywheel/v0/input/dcm2niix_input \
    -v </path/to/output>:/flywheel/v0/output \
    scitran/dcm2niix
```
