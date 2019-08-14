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

