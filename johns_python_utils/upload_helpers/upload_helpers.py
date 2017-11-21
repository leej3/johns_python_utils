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


def obfuscate_acquisition_time(series,df_offset):
    df_offset_row =  df_offset.loc[df_offset.participant_id == series.subject ,:]
    series.AcquisitionDateTime = str(pd.to_datetime(series.AcquisitionDateTime) - pd.DateOffset(years = df_offset_row.offset_years.values[0]) + pd.Timedelta("%d days"%df_offset_row.offset_days.values[0]))
    return series
        
    
def remove_json_fields(j_in,fieldname_tuples):
    """
    Each field name should be  a tuple
    """
    for f in fieldname_tuples:
        tmp = j_in
        if isinstance(f,tuple):
            for i,l in enumerate(f):
                try:
                    if i == (len(f)-1):
                        del tmp[l]
                    else:
                        tmp[l]
                        tmp = tmp[l]
                except KeyError:
                        pass
#                         print(f, ' not found as a json field')
                        
                        
        else:
            try:
                del tmp[f]
            except KeyError:
                        pass
#                         print(f, ' not found as a json field')


def delete_scan_json_fields(series,fieldname_tuples):
    json_path = series.json_path
    
    with json_path.open() as j:    
        data = json.load(j)
    
    remove_json_fields(data, fieldname_tuples)
    json_path.write_text(json.dumps(data))
    

def test_remove_json_fields():
    foo = {'a':{'b':{'c':20}},'d': 30}
    fieldname_tuples = [('a','b','c')]
    remove_json_fields(foo,fieldname_tuples)
    assert foo =={'a': {'b': {}}, 'd': 30}

    foo = {'a':{'b':{'c':20}},'d': 30}
    fieldname_tuples = [('a','b','c'),'d']
    remove_json_fields(foo,fieldname_tuples)
    assert foo =={'a': {'b': {}}}
    
    foo = {'a':{'b':{'c':20}},'d': 30}
    fieldname_tuples = ['d']
    remove_json_fields(foo,fieldname_tuples)
    assert foo =={'a': {'b': {'c': 20}}}
    
    foo = {'a':{'b':{'c':20}},'word': 30}
    fieldname_tuples = ['word']
    remove_json_fields(foo,fieldname_tuples)
    assert foo =={'a': {'b': {'c': 20}}}

    foo = {'a':{'b':{'c':20}},'d': 30}
    fieldname_tuples = [('a','d')]
    # some times fields are missing, this can be ignored
    remove_json_fields(foo,fieldname_tuples)
    assert foo == {'a': {'b': {'c': 20}}, 'd': 30}

