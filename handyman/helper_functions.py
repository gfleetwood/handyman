import json
import datetime
import codecs
import numpy as np
import pandas as pd
import plotnine as pn
import sklearn.metrics as sk_mt
from collections import OrderedDict
from sklearn.metrics import roc_curve as rc

def impute_scale_data(df):
    '''
    Role
    ----
    Imputes missing values with the median for numeric features and the mode for categorical ones, and then scales the numeric features
    by subtracting the mean and dividing by the standard deviation.
  
    Parameters
    ---------
    * df: A pandas dataframe
  
    Returns
    -------
    * df_imputed_scaled: A dataframe that has been imputed and scaled.
    '''
    
    imputer_num = Imputer(strategy = 'median') 
    df.loc[:, df.select_dtypes(exclude = ['object']).columns] = \
    imputer_num.fit_transform(df.select_dtypes(exclude = ['object']))  
    
    scaler = StandardScaler()
    df.loc[:, df.select_dtypes(exclude = ['object']).columns] = \
    scaler.fit_transform(df.select_dtypes(exclude = ['object']))
    
    for col in df.select_dtypes(include = ['object']).columns:
        df.loc[:, col] = df.loc[:, col].fillna(value = df.loc[:, col].value_counts().index[0])
        
     df_imputed_scaled = df
        
    return df_imputed_scaled
    
def get_dummies_enhanced(df):
    '''
    Role
    ----
    A simple extension of pandas.get_dummies which adds the dummied columns (with drop_first=True) and removes the old ones.
  
    Parameters
    ---------
    * df: A pandas dataframe
  
    Returns
    -------
    * df_new: A pandas dataframe with dummied categorical variables.
    '''
    
    dummies = pd.get_dummies(df, drop_first = True)
    cols = df.select_dtypes(include = ['object']).columns
    
    df_new = pd.concat([df.drop(cols, axis = 1), dummies], axis = 1)
    return df_new

def cutoff_youdens_j(y, y_hat_probs):
    '''
    Role
    ----
    Implement's Younden's J Statistic for finding an optimal threshold for a classification model.
  
    Parameters
    ---------
    * y: The true labels
    * y_hat_probs: The probabilities of the positive class
  
    Returns
    ------- 
    * youden_j: A recommended threshold for the model.
    '''
    
    fpr, tpr, thresholds = rc(y, y_hat_probs, pos_label = 1)
    j_scores = tpr - fpr
    j_ordered = sorted(zip(j_scores,thresholds))
    youden_j = j_ordered[-1][1]
    
    return youden_j

def data_diagnostics(df, num_cols, cat_cols):
    '''
    Role
    ----
    Takes a dataframe, and lists of its numeric and categorical variables. Returns a summary for each.
  
    Parameters
    ---------
    * df: A pandas dataframe
    * num_cols: A list of the numeric column names
    * cat_cols: A list of the categorical column names
  
    Returns
    -------
    * smry: A list containing: 1) num_summary: A pandas dataframe with a summary of the numeric variables, and 
    2) cat_summary: A pandas dataframe with a summary of the categorical variables
    '''

    # Numerical summary
    df_num = df[num_cols]
    num_summary = df_num.describe().T
    num_missingness_dtypes = pd.concat([df_num.isnull().sum(), df_num.dtypes], axis=1)
    num_missingness_dtypes.columns = ['null_values', 'data_type']
    num_summary_full = num_missingness_dtypes.join(num_summary, how='inner')

    # Categorical summary
    df_cat = df[cat_cols]
    cat_summary = pd.concat([df_cat.isnull().sum(), df_cat.dtypes], axis=1)
    cat_summary.columns = ['null_values', 'data_type']
    cat_summary['num_unique_values'] = [len(df_cat[col].value_counts()) for col in cat_cols]
    cat_summary['most_frequent_value'] = [
        df_cat[col].value_counts().reset_index().ix[0, 'index']
        for col in cat_cols
              ]
    cat_summary['most_frequent_value_ratio'] = [
        df_cat[col].value_counts(normalize = True).reset_index().ix[0, col]
        for col in cat_cols
              ]
    cat_summary['least_frequent_value'] = [
        df_cat[col].value_counts().reset_index().ix[len(df_cat[col].value_counts()) - 1, 'index']
        for col in cat_cols
              ]
    cat_summary['least_frequent_value_ratio'] = [
        df_cat[col].value_counts(normalize = True).reset_index().ix[len(df_cat[col].value_counts()) - 1, col]
        for col in cat_cols
              ]
    
    smry = [num_summary_full, cat_summary]

    return (smry)


def get_num_corr_plot(df, num_cols):
    '''
    Role
    ----
    Takes a dataframe and a list of its numeric columns and returns a plot of the correlation between variables.

    Parameters
    ---------
    * df: A pandas dataframe
    * num_cols: A list of the numeric column names

    Returns
    -------
    * df_num_correlations_plot: A heatmap plot of the correlation between the numeric variables.
    '''

    df_num = df[num_cols]
    df_num_correlations = df_num.corr().reset_index().melt(id_vars = ['index'],
                                                           value_vars = df_num.corr().columns)
    df_num_correlations_plot = (pn.ggplot(df_num_correlations, pn.aes('variable', 'index', fill='value'))
                                   + pn.geom_tile(pn.aes(width=.95, height=.95))
                                   + pn.geom_text(pn.aes(label='value'), size=10))

    return(df_num_correlations_plot)

def classification_metrics(y_actual, y_predicted):

    '''
    Role
    ----
    Generates a set of classification scores for a model's predictions.

    Parameters
    ---------
    * y_actual: The correct labels for the data.
    * y_predicted: The predicted labels produced by a model.

    Returns
    -------
    * metrics_dict: A dictionary with the accuracy, roc-auc, and f1 scores for the model's predictions.
    '''
    
    metrics_dict = OrderedDict()
    metrics_dict['accuracy'] = sum(y_actual == y_prediction)/float(len(y_actual))
    metrics_dict['roc_auc'] = sk_mt.roc_auc_score(y_actual, y_predicted)
    metrics_dict['f1_score'] = sk_mt.f1_score(y_actual, y_predicted)

    return(metrics_dict)
    
    
def kaiser_harris_criterion(df):
    '''
    Role
    ----
    Implement's the Kaiser-Harris criterion for suggesting an optimal number of dimensions for Principal Component Analysis.
  
    Parameters
    ---------
    * df: A pandas dataframe.
  
    Returns
    -------
    * dim_rec: The recommended dimensional space to project the original data into.
    '''
    
    cov_mat = np.cov(df.T)
    e_vals, _ = np.linalg.eig(cov_mat)
    dim_rec = len(e_vals[e_vals > 1])
    return(dim_rec)
    

def serialize_model(model, descr):
  
    '''
    Role
    ----
    T
  
    Parameters
    ---------
    * 
    * 
    * 
  
    Returns
    -------
    A
    
    * num_summary: 
    * cat_summary:
    '''
    
    attrs = [i for i in dir(model) if i.endswith('_') and not i.endswith('__')]   
    attr_dict = {i: getattr(model, i) for i in attrs}    
    for k in attr_dict:
        if isinstance(attr_dict[k], np.ndarray):
            attr_dict[k] = attr_dict[k].tolist()
    attr_json = json.dumps(attr_dict)
    
    d = OrderedDict()
    d['model_type'] = [str(model).split('(')[0]]
    d['description'] = descr
    d['params'] = [json.dumps(model.get_params())]
    d['attrs'] = [attr_json]    
        
    df = pd.DataFrame(d)
    return df

def unserialize_model(df, model_revival, model_index = 0):
  
    '''
    Role
    ----
    T
  
    Parameters
    ---------
    * 
    * 
    * 
  
    Returns
    -------
    A
    
    * num_summary: 
    * cat_summary:
    '''
    
    params = json.loads(df.params[model_index])
    attributes = json.loads(df.attrs[model_index])
    model_revival.set_params(**params)
    for k in attributes:
        if isinstance(attributes[k], list):
            setattr(model_revival, k, np.array(attributes[k]))
        else:
            setattr(model_revival, k, attributes[k])
            
    return model_revival

def rf_feature_importance(df, model_rf):
  
    '''
    Role
    ----
    T
  
    Parameters
    ---------
    * 
    * 
    * 
  
    Returns
    -------
    A
    
    * num_summary: 
    * cat_summary:
    '''

    fi = list(zip(df.columns, model_rf.feature_importances_))
    fi_sorted = sorted(fi, key = lambda x: -x[1])
    return fi_sorted

def flatten(L):
  
    '''
    Role
    ----
    T
  
    Parameters
    ---------
    * 
    * 
    * 
  
    Returns
    -------
    A
    
    * num_summary: 
    * cat_summary:
    '''
    if not L:
        result = []
    elif len(L) == 1:
        if type(L[0]) is not list:
            result = L
        elif type(L[0]) is list:
            result = flatten(L[0])
    else:
        cut = len(L) // 2
        result = flatten(L[0: cut]) + flatten(L[cut:])
    return result
    
def get_coefficients_logreg(df, model):
    '''
    Role
    ----
    Takes a model and a dataframe and returns a dataframe with the proper column and model coefficient pairs.
  
    Parameters
    ---------
    * 
    * 
    * 
  
    Returns
    -------
    A
    
    * num_summary: 
    * cat_summary:
    '''
    df_coefficient = pd.DataFrame(sorted(list(zip(df.columns, model.coef_[0])), key = lambda x: -x[1]), 
                                  columns = ['feature', 'coefficient'])
    
    return df_coefficient
    
    
def flatten_dict(y):  
    '''
    Role
    ----
    Takes a model and a dataframe and returns a dataframe with the proper column and model coefficient pairs.
  
    Parameters
    ---------
    * 
    * 
    * 
  
    Returns
    -------
    A
    
    * num_summary: 
    * cat_summary:
    '''
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out
    
def get_date_time():  
    '''
    Role
    ----
    Returns the system date and time as a string.
  
    Parameters
    ---------
    * None 
  
    Returns
    -------
    * String representation of date and time.
    '''
   return str(datetime.datetime.now()).split(' ')
























