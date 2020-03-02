import sklearn.preprocessing as sk_pp
from skopt.space import Real, Integer, Categorical
import json
import datetime
import codecs
import numpy as np
import pandas as pd
import plotnine as pn
import sklearn.metrics as sk_mt
import statsmodels.formula.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import subprocess as sp
from io import StringIO
from collections import OrderedDict
from sklearn.metrics import roc_curve as rc
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler
from statsmodels.graphics.gofplots import ProbPlot
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pyodbc
import statsmodels.api as sm
import pandas as pd
import subprocess as sp
import pyodbc
from io import StringIO
import importlib
import pickle
import pandas as pd
import datetime
import cProfile, pstats, io
import json
import pandas as pd
from collections import OrderedDict

def training(mdl, X, y, folds, cv = 2, metric = "accuracy"):
    
    if cv == 1:
        mdl.fit(X, y)
        training = None
        results = None
    if cv == 2:
        training = sk_ms.cross_val_score(mdl, X, y, cv = folds, scoring = metric, n_jobs = -1)
        results = (training.mean(), training.std()) 
        
    return(mdl, training, results)

def substr_overlap(s, n):
    
    result = [s[i:(i+n)] for i in range(len(s) - (n - 1))]
    
    return(result)

def substr_distinct(s, n):
    
    r = list(range(0, len(s) + 1, n))
    result = [s[r[i]:r[(i+1)]] for i, _ in enumerate(r[:-1])] + [s[r[-1]:]]
    
    return(result)

def adverserial_validation(X1, X2):

    df_av = pd.concat([X2.assign(test = 1), X1.assign(test = 0)], axis = 0)
    mdl_av = sk_lm.LogisticRegression()
    training_scores_av = sk_ms.cross_val_score(mdl_av, 
                                               df_av.drop(['test'], axis = 1),
                                               df_av.test.values, 
                                               cv = 5, 
                                               scoring = 'roc_auc')
    results = (training_scores_av.mean(), training_scores.std())
    
    return(results)

def process_param(key_val):
    
    key_val_li = list(key_val)
    key, val = key_val_li
    
    if val == 1:
        val = list(np.linspace(0, 1, 100))
    elif isinstance(val, int):
        val = list(np.arange(val, 10**2, 10))
        
    if key == 'n_jobs': 
        val = -1
    elif isinstance(key, str) and val is not None:
        val = list([val])
    
    return((key, val))
    
def subset_by_iqr(df, column, whisker_width = 1.5):
    
    q1 = df[column].quantile(0.25)                 
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    
    mask = (df[column] >= q1 - whisker_width*iqr) & (df[column] <= q3 + whisker_width*iqr)
    
    return df.loc[mask]
    
def generate_params(mdl, scale = "small"):
    
    params = {}
    
    for key, val in mdl.get_params().items(): 
        
        if isinstance(mdl.get_params()[key], bool):
            params[key] = random.choice([False, True])
        elif key == 'n_jobs':
            params[key] = -1            
        else:
            params[key] = val
    
    return(params)

def generate_grid_default(mdl):
    
    grid_test = map(lambda x: process_param(x), mdl.get_params().items())
    grid = dict(list(grid_test))
    
    return(grid)

def train(mdl, X, y, metric = None, method = 'cv', grid = None, seed = 8):
if method == 'cv':
  cv_scores = sk_ms.cross_val_score(mdl, 
                                    X, 
                                    y, 
                                    cv = 5,
                                    n_jobs = -1,
                                    scoring = metric)
  
  mu = (np.sqrt(-1*cv_scores.mean()) 
        if metric == 'neg_mean_squared_error' 
        else cv_scores.mean())
  sd = cv_scores.std()
  results = {"scores_mu": mu, "scores_sd": sd}
elif method == 'tune':
  mdl_tuner = sk_ms.RandomizedSearchCV(estimator = mdl,
                                       cv = 5, 
                                       param_distributions = grid, 
                                       scoring = metric, 
                                       n_jobs = -1, 
                                       n_iter = 100, 
                                       verbose = 0, 
                                       refit = True, 
                                       random_state = seed)    
  mdl_tuner.fit(X, y)
  score = np.sqrt(-1*mdl_tuner.best_score_)
  score = (np.sqrt(-1*mdl_tuner.best_score_) 
           if metric == 'neg_mean_squared_error' 
           else mdl_tuner.best_score_)
  results = {"best_model": mdl_tuner.best_estimator_, "best_score": score}
else:
    return("Invalid method selected!")

return(results)

def extract_dict_from_str(string):

    x = ast.literal_eval(re.search('({.+})', string).group(0))
    
    return(x)

def get_shap_exp_vals(mdl, X, y):
    """
    fplot = shap.force_plot(explainer.expected_value, shap_vals[45,:], X_train.iloc[45,:], link = 'logit')
    """
    
    mdl.fit(X.values, y.values)
    explainer = shap.TreeExplainer(test, model_output = "probability")
    shap_values = explainer.shap_values(X.values)
    
    return((explainer, shap_values))  

def get_shap_df(shap_values, X):
    
    df_shap = pd.DataFrame(
        list(zip(np.mean(shap_values, axis = 0), X.columns)),
        columns = ['shap_mean', 'feature'])
    df_shap = df_shap[['feature', 'shap_mean']]
    df_shap['shap_mean_abs'] = np.absolute(df_shap['shap_mean'])
    df_shap.sort_values(['shap_mean_abs'], ascending = False, inplace = True)
    
    return(df_shap)

def extract_dict_from_str(string):

    x = ast.literal_eval(re.search('({.+})', string).group(0))
    
    return(x)

def shap_df_one_record(data):
    x = extract_dict_from_str(data)

    top = [ ['LoS_student_prediction', float("NaN"), x['outValue']],
           ['LoS_base_prediction', float("NaN"), x['baseValue']], 
     ['student_base_diff_val', float("NaN"), x["outValue"] - x['baseValue']]]

    bottom = [
        ['feature_' + j, x['features'][str(i)]['value'], x['features'][str(i)]['effect']]
        for i,j in enumerate(x['featureNames'])]

    result = (pd.DataFrame(top + bottom, columns = ['characteristic', 'student_data', 'shap_val_log_odds'])
     .assign(shap_probability = lambda x: np.exp(x.shap_val_log_odds) / ( 1 + np.exp(x.shap_val_log_odds)))
     .round(2))
    
    return(result)

import cProfile, pstats, io

def profile(fnc):
    
    """A decorator that uses cProfile to profile a function"""
    
    def inner(*args, **kwargs):
        
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner

def date_decomposition(df):

	result = df.assign(
	               day = df.ts.dt.day,
	               month = df.ts.dt.month,
	               year = df.ts.dt.year)
	
	return(result)

ks = ks.assign(hour=ks.launched.dt.hour,
               day=ks.launched.dt.day,
               month=ks.launched.dt.month,
               year=ks.launched.dt.year)

grid_xgb_small = {'learning_rate': [0.005, 0.05, 0.1], 
        'n_estimators': [10, 100, 250, 500],
        'num_leaves': [6, 50, 100, 250, 500],
        'boosting_type': ['gbdt', 'rf'],
        'colsample_bytree' : [0.65, 1], 
        'subsample': [0.7, 0.9],
        'reg_alpha': [0, 1.2], 
        'reg_lambda': [0, 2]}

ps_knn = {"n_neighbors": range(5, 25, 1), "weights": ["uniform", "distance"]}

hp_xgb_grl = {
  'learning_rate': np.linspace(0.01, 1.0, 10), 
  'num_leaves': np.arange(10, 100, 10), 
  'max_depth': np.arange(0, 50, 10), 
  'min_child_samples': np.arange(0, 50, 10),
  'max_bin': np.arange(100, 1000, 100), 
  'subsample': np.linspace(0.01, 1.0, 10),
  'subsample_freq': np.arange(0, 10, 1),
  'colsample_bytree': np.linspace(0.01, 1.0, 10),
  'min_child_weight': np.arange(0, 10, 1),
  'subsample_for_bin': np.arange(100000, 500000, 1000),
  'reg_lambda': np.linspace(1e-9, 1000, 10), 
  'reg_alpha': np.linspace(1e-9, 1.0, 100), 
  'scale_pos_weight': np.linspace(1e-9, 500, 10), 
  'n_estimators':  np.arange(50, 100, 10)}
    
hp_rf_gr = {
'bootstrap': [True, False], 
'max_features': ['auto', 'sqrt'],
'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
'min_samples_leaf': [1, 2, 4], 
'min_samples_split': [2, 5, 10],
'n_estimators': [200, 400, 600, 800, 1000, 1200, 1800, 2000]}

hp_lgb_gr = {
'learning_rate': (0.01, 1.0, 'log-uniform'),
'num_leaves': (1, 100),      
'max_depth': (0, 50),
'min_child_samples': (0, 50),
'max_bin': (100, 1000),
'subsample': (0.01, 1.0, 'uniform'),
'subsample_freq': (0, 10), 
'colsample_bytree': (0.01, 1.0, 'uniform'),
'min_child_weight': (0, 10),
'subsample_for_bin': (100000, 500000),
'reg_lambda': (1e-9, 1000, 'log-uniform'), 
'reg_alpha': (1e-9, 1.0, 'log-uniform'),
'scale_pos_weight': (1e-6, 500, 'log-uniform'),
'n_estimators': (50, 100)}
  
hp_rf_bs = { 
"max_depth": Integer(3, 10), 
"n_estimators": Integer(100, 500),  
"max_features": Categorical(['sqrt','log2']),
"min_samples_split": Integer(2, 50), 
"min_samples_leaf": Integer(2, 50), 
"criterion": Categorical(['entropy'])}

hp_xgb_bs = {
'learning_rate': Real(0.005, 0.1),
'n_estimators': Integer(10, 500),
'num_leaves': Integer(6, 50), 
'boosting_type': Categorical(['gbdt', 'rf']),
'colsample_bytree': Real(0.65, 1),
'subsample': Real(0.7, 0.9),
'reg_alpha': Real(0, 1.2), 
'reg_lambda': Real(0, 2)}

hp_xgb_bl = {
  'learning_rate': Real(0.01, 1.0), 
  'num_leaves': Integer(10, 100), 
  'max_depth': Integer(0, 50), 
  'min_child_samples': Integer(0, 50),
  'max_bin': Integer(100, 1000), 
  'subsample': Real(0.01, 1.0, 10),
  'subsample_freq': Integer(0, 10),
  'colsample_bytree': Real(0.01, 1.0, 10),
  'min_child_weight': Integer(0, 10),
  'subsample_for_bin': Integer(100000, 500000),
  'reg_lambda': Real(1e-9, 1000, 10), 
  'reg_alpha': Real(1e-9, 1.0, 100), 
  'scale_pos_weight': Real(1e-9, 500, 10), 
  'n_estimators':  Integer(10, 100)}

# Time Series Clustering
ts_clustering <- function(mat, dist = "dtw", linkage = "average"){
  mat_dist <- parDist(x = stories_temp, method = dist)
  stories_clust <- hclust(mat_dist,  method = linkage)
}



def adverserial_validation(X1, X2):

    df_av = pd.concat([X2.assign(test = 1), X1.assign(test = 0)], axis = 0)
    mdl_av = sk_lm.LogisticRegression()
    training_scores_av = sk_ms.cross_val_score(
        mdl_av, 
        df_av.drop(['test'], axis = 1),
        df_av.test.values, 
        cv = 5, 
        scoring = 'roc_auc')
    
    results = (training_scores_av.mean(), training_scores.std())
    
    return(results)

