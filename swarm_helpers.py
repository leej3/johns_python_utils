# coding: utf-8
from pathlib import Path
import pandas as pd
def tmas(swarm_dir=None,job_id=None,files_of_interest=None,parallel_label='_[01]',filetype='*'):
    from pathlib import Path
    if not swarm_dir:
        swarm_dir = Path.cwd()

    
    df_file_paths = (
        pd.DataFrame(
            [x.as_posix() for x in swarm_dir.glob('*.'+ filetype)],
            columns=['paths'])
    )
    df_swarm = (pd.concat(
        [df_file_paths,
        df_file_paths.
        paths.
        str.
        extract(
            '.*/swarm_(?P<job_id>\d{8})_(?P<sub_job>[0-9]{1,4})(?P<parallel_label>_[0-9]{1,2})?.'+ filetype,
            expand = True)],
        axis = 1)
    )
    df_swarm.fillna(value = "",inplace = True)
    df_swarm = df_swarm.assign(job_id = df_swarm.job_id.astype('int'),
                               sub_job = df_swarm.sub_job.astype('int'))

    if not job_id:
        job_ids = df_swarm.job_id.unique()
        job_id = [job_ids[0]]
        print("Using first job of: ", '\n'.join([str(j) for j in job_ids]) )
    if not files_of_interest:
        files_of_interest = df_swarm.query("job_id in @job_id").sub_job.unique()

    df_swarm.sort_values(['job_id','sub_job'],inplace= True)
    files_text = [Path(x).read_text() for x in df_swarm.query("job_id in @job_id and sub_job in @files_of_interest").paths]
    
    return files_text
   
    

    
# if not job_id:
    #     job_id = '.*'
#df_file_paths = pd.DataFrame([x.as_posix() for x in swarm_dir.glob('*.'+ filetype)],columns=['paths'])
#job_id = '.*'
#df_file_paths.paths.str.extract('.*swarm_({j}_[0-9_]*).{f}'.format(j= job_id, f = filetype))
