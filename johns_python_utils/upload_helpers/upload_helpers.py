# coding: utf-8
from pathlib import Path
import json
def get_scan_fields(series,fieldnames):
    """
        For applying to each row of a dataframe.
        The field is extracted from the json and added to the
        sub_sess tsv.
    """
    json_path = series.json_path
    
    with json_path.open() as j:    
        data = json.load(j)
        for f in fieldnames:
            val = data[f]
            series[f] = val
    return series

def get_scans_tsv(series):
    scans_tsv = Path(series.json_path.parent.parent.joinpath(series.subject + '_' + series.session + '_scans.tsv'))        
    series['scans_tsv_path'] = scans_tsv   
    return series

def write_scan_fields(series,fieldnames):
    if type(fieldnames) == str:
        fieldnames = [fieldnames]
    elif not type(fieldnames) == list:
        assert False
    json_path = series.json_path
    scans_tsv = series.scans_tsv_path
    scan = json_path.parent.name + '/' + json_path.with_suffix('.nii.gz').name
    if not scans_tsv.exists():
        scans_tsv.write_text('filename\tacq_time\n')
#         print('type: fieldname is ',type(fieldnames),'\n','type series: ',type(series))

    with scans_tsv.open('a') as f:
            f.write(scan + '\t' + '\t'.join(series.loc[fieldnames]) + '\n')
    return None

