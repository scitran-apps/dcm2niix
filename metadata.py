#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Generate file metadata (file.info) from BIDS sidecar json file, as output
# from dcm2niix. Also sets the classification (file.measurements) from the
# input config.json file, as provided by Flywheel.
#
# @LMPERRY, 9/17
#

import os
import json
import logging
import datetime
logging.basicConfig()
log = logging.getLogger('metadata')


# Generate metadata
def metadata_gen(outbase, bids_sidecar, config_file):
    """Generate file metadata.

    Builds file.info from BIDS sidecar json file, as output from dcm2niix.
    Also sets the classification (file.measurements) from the input
    config.json file, as provided by Flywheel, and file.type from the ext.

    Args:
        outbase: Directory with output files.
        bids_sidecar: Path to BIDS sidecar json file.
        config_file: Path to config.json file.

    Returns:
        metadata_file: Path to .metadata.json file.

    """
    output_files = os.listdir(outbase)
    files = []
    if len(output_files) > 0:

        # Get the BIDS info from the sidecar
        with open(bids_sidecar) as bids_f:
            bids_info = json.load(bids_f)

        # Read the config
        (config, classification) = ([], [])
        if config_file.endswith('config.json'):
            classification = []
            with open(config_file) as config_f:
                config = json.load(config_f)
            try:
                classification = config['inputs']['dcm2niix_input']['object']['measurements']
            except:
                log.info('  Cannot determine classification from config.json.')
        else:
            log.info('  No config file was found. Classification will not be set.')

        for f in output_files:
            # Determine the file's type
            if f.endswith('.nii.gz') or f.endswith('.nii'):
                ftype = 'nifti'
            elif f.endswith('bvec'):
                ftype = 'bvec'
            elif f.endswith('bval'):
                ftype = 'bval'
            else:
                ftype = 'None'

            # Build the file map and append to files list
            fdict = {}
            fdict['name'] = f
            fdict['type'] = ftype
            fdict['info'] = bids_info
            fdict['measurements'] = classification
            files.append(fdict)

        # Collate the metadata and write to file
        metadata = {}
        metadata['acquisition'] = {}
        metadata['acquisition']['files'] = files
        metadata_file = os.path.join(outbase, '.metadata.json')
        with open(metadata_file, 'w') as metafile:
            json.dump(metadata, metafile)

    return metadata_file


if __name__ == '__main__':
    """Generate file metadata (file.info), type (file.type), name (file.name) and
    classification (file.measurements) for each file in <outdir>.
    """

    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('outdir', nargs='?', help='outfile directory')
    ap.add_argument('bids_sidecar', nargs='?', help='path to BIDS sidecar')
    ap.add_argument('config_file', help='Read classification from config_file')
    ap.add_argument('--log_level', help='logging level', default='info')
    args = ap.parse_args()

    log.setLevel(getattr(logging, args.log_level.upper()))
    logging.getLogger('metadata').setLevel(logging.INFO)
    log.info('  job start: %s' % datetime.datetime.utcnow())

    # Generate metadata
    metadata_file = metadata_gen(args.outdir, args.bids_sidecar, args.config_file)

    log.info('  job stop: %s' % datetime.datetime.utcnow())

    if metadata_file:
        log.info('  generated %s' % metadata_file)
    else:
        log.info('  Failed.')
