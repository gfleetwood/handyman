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

def run_cv(mdl, X, y,metric):
    cv_scores = sk_ms.cross_val_score(mdl, X, y, cv = 5, n_jobs = -1, scoring = metric)
    return({"scores_mean": np.sqrt(cv_scores.mean()), "scores_sd": cv_scores.std()})

def get_baseline_regress(X, y):
    
    mdl = sk_lm.LinearRegression()
    cv_scores = sk_ms.cross_val_score(mdl, X, y, cv = 5, scoring = "neg_mean_squared_error", n_jobs = -1)
    print("Naive Baseline: ", y.std(), 
          "Naive Model Baseline(mu, sigma): ", np.sqrt(-1*cv_scores.mean()), cv_scores.std())
    return("Done")
