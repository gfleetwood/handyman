# Skeleton For Nested CV

model = sk_lm.LogisticRegression()
grid = None
mdl = sk_ms.RandomSearchCV(estimator = mdl, param_grid = grid, cv = 5) if grid is not None else model
training_scores = sk_ms.cross_val_score(mdl, X_train, y_train, cv = 5)
results = (training_scores.mean(), training_scores.std())

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

