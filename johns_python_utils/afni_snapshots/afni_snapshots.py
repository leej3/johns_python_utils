# coding: utf-8
__all__  = ['make_montage']
from pathlib import Path
def make_montage(ulay=None,olay=None,image_dir=None,output_dir=None,cbar='FreeSurfer_Seg_i255',opacity='4',montx='3',monty='1',blowup='1'):
    output_dir = Path(output_dir)
    image_dir = Path(image_dir)
    prefix = output_dir.joinpath(image_dir.name)

    if not ulay:
        ulay = image_dir.joinpath('T1.nii.gz')
    if not olay:
        olay = image_dir.joinpath('aparc+aseg.nii.gz')
    cbar = 'FreeSurfer_Seg_i255'
    opacity = '4'
    
    cmd = 'module load afni;' + \
    'center=`3dCM {i}`;'.format(i = olay.as_posix()) + \
    'anal/afni_freesurfer_qc_files/other_files/drive_afni.tcsh' + \
    ' -ulay ' + ulay.as_posix() + \
    ' -olay ' + olay.as_posix() + \
    ' -prefix ' + prefix.as_posix() + \
    ' -cbar ' + cbar + \
    ' -opacity ' + opacity + \
    ' -do_clean' + \
    ' -montx ' + montx + \
    ' -monty ' + monty + \
    ' -set_dicom_xyz $center' + \
    ' -blowup ' + blowup + ';' +  \
    'echo Files for concatenation: ' + \
    ' $(ls {p}*png);'.format(p=prefix) + \
    'convert +append {p}*png {p}.jpg;'.format(p = prefix) + \
    'rm {p}.[a-z][a-z][a-z].png'.format(p = prefix)
    return cmd

