# coding: utf-8

from pathlib import Path
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

def make_swarm_path(directory,recon, analysis_version):
    directory = Path(directory)
    return directory.joinpath(recon + '_' + analysis_version + '.cmd')

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
                                        expert_opts = expert_opts
                                       longitudinal = longitudinal),
        axis = 1)
        )
    swm_file = make_swarm_path(freesurfer_dir, recon, analysis_version)
        
    swm_file.write_text('\n'.join(df[recon])) 
    return (df, swm_file)