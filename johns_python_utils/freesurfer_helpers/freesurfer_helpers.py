# coding: utf-8
__all__ = ['generate_freesurfer_command',
            'generate_template_command',
            'generate_subfield_command',
            'generate_recon_swarm',
            'make_swarm_path',]

from pathlib import Path

def make_swarm_path(directory,recon, analysis_version):
    directory = Path(directory)
    return directory.joinpath(recon + '_' + analysis_version + '.cmd')

def generate_freesurfer_command(df_row=None,output_dir=None,ncpus='4',conf_script=None,clustered_directive='all',image_col='scan_path',expert_opts=None,longitudinal=False):
    tpNid = df_row.subject + '_' + df_row.ses
    
    cmd = 'source ' + conf_script.as_posix() + ';' + \
    ' recon-all' +  \
    ' -' + clustered_directive + \
    ' -hires' + \
    ' -no-isrunning' + \
    ' -openmp ' + ncpus + \
    ' -expert ' + expert_opts.as_posix() +  ' -xopts-overwrite'
    if clustered_directive in ['autorecon1','all']:
        cmd = cmd + ' -i ' + df_row[image_col]
    if longitudinal:
        cmd = cmd + ' -long' + \
        ' ' + tpNid + \
        ' ' + df_row.subject + '_template'
    else:
        cmd = cmd + ' -s ' + tpNid
    return cmd

def generate_recon_swarm(df,recon,clust,outdir,conf_script,ncpus,freesurfer_dir,analysis_version,expert_opts,longitudinal=False):
    df[recon] = (
        df.
        copy().
        apply(
            lambda row:
            generate_freesurfer_command(df_row = row,
                                        output_dir = outdir,
                                        conf_script = conf_script,
                                        clustered_directive = clust,
                                        ncpus = ncpus,
                                        expert_opts = expert_opts,
                                       longitudinal = longitudinal),
        axis = 1)
        )
    swm_file = make_swarm_path(freesurfer_dir, recon, analysis_version)
        
    swm_file.write_text('\n'.join(df[recon])) 
    return (df, swm_file)

def generate_template_command(df=None,output_dir=None,conf_script=None,expert_opts=None):
# command to generate:    recon-all -base <templateid> -tp <tp1id> -tp <tp2id> ... -all
    sub_ids = set(df.subject)
    assert len(sub_ids) == 1
    sub_id = list(sub_ids)[0]

    cmd = 'source ' + conf_script.as_posix() + ';' + \
    ' recon-all' +  \
    ' -base' + \
    ' ' + sub_id + '_template' + \
    ' -tp ' + ' -tp '.join(df.subject + '_' + df.ses) + \
    ' -hires' + \
    ' -expert ' + expert_opts.as_posix() +  ' -xopts-overwrite' + \
    ' -all' 

    return cmd
# generate_template_command(df, outdir, subj_dir, conf_script)


def generate_subfield_command(df=None,conf_script=None,expert_opts=None):
    # (cross sectional):  recon-all -all -s <tpNid> -i path_to_tpN_dcm
    # longitudinal command:  recon-all -long <tpNid> <templateid> -all  
    # command to generate: longHippoSubfieldsT1.sh <baseID> [SubjectsDirectory]
    cmd = 'source ' + conf_script.as_posix() + ';' + \
    ' longHippoSubfieldsT1.sh' + \
    ' ' + df.subject + '_template'
    return cmd
