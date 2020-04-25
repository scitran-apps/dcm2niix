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
import re
import json
import logging
import datetime
from pprint import pprint as pp
logging.basicConfig()
log = logging.getLogger('metadata')


# Generate metadata
def metadata_gen(outbase, bids_sidecar_dir, config_file):
    """Generate file metadata.

    Builds file.info from BIDS sidecar json file, as output from dcm2niix.
    Also sets the classification (file.measurements) from the input
    config.json file, as provided by Flywheel, and file.type from the ext.

    Args:
        outbase:          Directory with output files.
        bids_sidecar_dir: Root path to BIDS sidecar json files.
        config_file:      Path to config.json file.

    Returns:
        metadata_file: Path to .metadata.json file.

    """
    output_files = os.listdir(outbase)
    files = []
    if len(output_files) > 0:

        # Read the config
        (config, modality, classification) = ([], None, [])
        if config_file.endswith('config.json'):
            with open(config_file) as config_f:
                config = json.load(config_f, strict=False)
            try:
                classification = config['inputs']['dcm2niix_input']['object']['classification']
            except:
                log.info('  Cannot determine classification from config.json.')
            try:
                modality = config['inputs']['dcm2niix_input']['object']['modality']
            except:
                log.info('  Cannot determine modality from config.json.')
        else:
            log.info('  No config file was found. Classification will not be set for outputs!')

        for f in output_files:

            # Determine the file's type
            if f.endswith('.nii.gz') or f.endswith('.nii'):
                ftype = 'nifti'
                bids_sidecar = os.path.join(bids_sidecar_dir, re.sub(r'(\.nii\.gz|\.nii)', '.json', f))
                log.info('  generated {}'.format(bids_sidecar))
                if not os.path.isfile(bids_sidecar):
                    bids_sidecar = os.path.join(bids_sidecar_dir, re.sub(r'(\.nii\.gz|\.nii|_[0-9][0-9]\.nii\.gz|_[0-9][0-9]\.nii|_[0-9]\.nii\.gz|_[0-9]\.nii)', '.json', f))
                    log.info(bids_sidecar)
            elif f.endswith('bvec'):
                ftype = 'bvec'
                bids_sidecar = os.path.join(bids_sidecar_dir, f.replace('.bvec','.json'))
            elif f.endswith('bval'):
                ftype = 'bval'
                bids_sidecar = os.path.join(bids_sidecar_dir, f.replace('.bval','.json'))
            elif f.endswith('json'):
                ftype = 'source code'
                bids_sidecar = os.path.join(bids_sidecar_dir, f)
            else:
                ftype = 'None'
                bids_sidecar = []

            # Build the file map
            fdict = {}
            fdict['name'] = f
            fdict['type'] = ftype
            fdict['classification'] = classification

            # Get the BIDS info from the sidecar associated with this file
            if bids_sidecar and os.path.isfile(bids_sidecar):
                with open(bids_sidecar) as bids_f:
                    bids_info = json.load(bids_f, strict=False)
                    if not modality and 'Modality' in bids_info:
                        modality = bids_info['Modality']

                # Add bids_info to info key
                fdict['info'] = bids_info

            # Set modality (config.json > bids_info > 'MR')
            if modality:
                fdict['modality'] = modality
            else:
                fdict['modality'] = 'MR'

            # Append this file dict to the list
            files.append(fdict)

        # Collate the metadata and write to file
        metadata = {}
        metadata['acquisition'] = {}
        metadata['acquisition']['files'] = files
        pp(metadata)
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
    ap.add_argument('bids_sidecar', nargs='?', help='root path to BIDS sidecar files')
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
