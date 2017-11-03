# coding: utf-8
import pandas as pd
from sklearn.metrics import confusion_matrix
def get_confusion_matrix(df,col_true,col_prob,threshold):
    thresholded = df[col_prob] >= threshold
    return confusion_matrix(df[col_true], thresholded)

def get_classification_performance(df,col_true,col_prob):
    threshold, tn, fp, fn, tp =[[] for i in range(5)]
    for thresh in df[col_prob]:
        tn_val, fp_val, fn_val, tp_val  = get_confusion_matrix(df,
                                                          col_true,
                                                          col_prob,
                                                          thresh).ravel()
        threshold.append(thresh)
        tn.append(tn_val)
        fp.append(fp_val)
        fn.append(fn_val)
        tp.append(tp_val)
    df_classification = pd.DataFrame({'threshold':threshold,
                                      'tn': tn,
                                      'fp': fp,
                                      'fn' : fn,
                                      'tp' : tp})
    return df_classification

def get_classification_scores(df,col_true,col_prob):
    qc_name = '_'.join(col_true.split('_')[:-1])
    df = get_classification_performance(df,col_true,col_prob)
    tpr = df.tp / (df.tp + df.fn)
    fpr = df.fp / (df.fp + df.tn)
    fdr = df.fp / (df.fp + df.tp)
    df_out = pd.DataFrame({
        qc_name + '_tpr' : tpr,
        qc_name + '_fpr' : fpr,
        qc_name + '_fdr' : fdr,
        qc_name + '_fp' : df.fp,
        qc_name + '_tp' : df.tp,
        qc_name + '_fn' : df.fn,
        qc_name + '_tn' : df.tn

    })
    return df_out

def test_get_classification():
    df_test = pd.DataFrame({'y_true':[0, 1, 0, 1, 1],'y_pred' : [1, 1, 1, 0, 1],'y_prob': [0.4,0.4,0.4,0.2, 0.8]})
    col_true = 'y_true'
    col_prob = 'y_prob'
    df_performance = get_classification_scores(df_test,col_true,col_prob)
    df_performance = pd.concat([df_test,df_performance],axis = 1)
    print(df_performance.head(),'\n\n')

    print(df_performance.sum())
    test_column_equalities = df_performance.sum() -pd.Series(
        {'y_fdr': 1.8999999999999999,
     'y_fpr': 4.0,
     'y_pred': 4.0,
     'y_prob': 2.2000000000000002,
     'y_tpr': 3.3333333333333335,
     'y_true': 3.0}) >0.1
    assert 0 == sum(test_column_equalities)