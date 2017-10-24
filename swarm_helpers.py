# coding: utf-8
from pathlib import Path
import pandas as pd
def tmas(swarm_dir=None,job_id=None,files_of_interest=None,parallel_label='_[01]',filetype='*'):
    from pathlib import Path
    if not swarm_dir:
        swarm_dir = Path.cwd()
    
    df_file_paths = pd.DataFrame([x.as_posix() for x in swarm_dir.glob('*.'+ filetype)],columns=['paths'])
    df_file_paths = (df_file_paths.
                      loc[df_file_paths.paths.str.find(job_id)>0,:].
                      assign(run = lambda df:
                             df.paths.str.extract(
                                 '/.*swarm_\d*_(\d*).'+filetype,
                                 expand=False).astype(int)).
                      sort_values('run'))

    files_text = [Path(x).read_text() for x in df_file_paths.query("run in @files_of_interest").paths]
    return files_text
   
    

    
# if not job_id:
    #     job_id = '.*'
#df_file_paths = pd.DataFrame([x.as_posix() for x in swarm_dir.glob('*.'+ filetype)],columns=['paths'])
#job_id = '.*'
#df_file_paths.paths.str.extract('.*swarm_({j}_[0-9_]*).{f}'.format(j= job_id, f = filetype))
