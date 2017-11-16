# coding: utf-8
import pandas as pd
def merge_and_report(df1,df2,on):
    df_out = df1.merge(df2, on = on, how = 'outer', indicator = True)
    if  sum(df_out._merge != 'both') > 0:
        print('The following were dropped: \n\n\n\n\n',df_out.query("_merge != 'both'"))
        df_out = df_out.query("_merge == 'both'")
    df_out = df_out.drop('_merge',axis = 1)
    return df_out