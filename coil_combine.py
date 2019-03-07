#!/usr/bin/python
import os
import sys
import glob
import nibabel as nb

output_directory = sys.argv[1]
nifti_files = glob.glob(os.path.join(output_directory, '*.nii*'))

for n in nifti_files:
    try:
        print('  Loading data from: %s...' % (n))
        n1 = nb.load(n)
        d1 = n1.get_data()
        d2 = d1[...,-1]
        n2 = nb.Nifti1Image(d2, n1.get_affine(), header=n1.get_header())
        nb.save(n2, n)
        print('  Generated %s.' % (n))
        exit(0)
    except:
        print('  Could not generate combined coil data for %s' % (n))
        exit(1)
