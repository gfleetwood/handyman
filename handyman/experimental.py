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

def tuner(mdl, X, y, grid, seed):
    
    mdl_tuner = sk_ms.RandomizedSearchCV(estimator = mdl,
                                         cv = 5, 
                                         param_distributions = grid, 
                                         scoring = 'neg_mean_squared_error', 
                                         n_jobs = -1, 
                                         n_iter = 100, 
                                         verbose = 0, 
                                         refit = True, 
                                         random_state = seed)    
    mdl_tuner.fit(X, y)
    score = mdl_tuner.best_estimator_.score(X, y)
    
    return({"best_model": mdl_tuner.best_estimator_, "best_score": score})

