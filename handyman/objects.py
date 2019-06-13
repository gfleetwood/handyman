from skopt.space import Real, Integer, Categorical

# Sample grids for hyperparameter tuning

grid_kknr = {'leaf_size': [30, 40, 50, 60, 70, 80, 90], 
             'n_neighbors': [5, 15, 25, 35, 45, 55, 65, 75, 85]}

grid_rf = {
'bootstrap': [True, False], 'max_features': ['auto', 'sqrt'],
'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 5, 10],
'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}

grid_rf_skopt = { 
"max_depth": Integer(3, 10), "n_estimators": Integer(100, 500),  
"max_features": Categorical(['sqrt','log2']), "min_samples_split": Integer(2, 50), 
"min_samples_leaf": Integer(2, 50), "criterion": Categorical(['entropy'])}

grid_lgb = {
'learning_rate': (0.01, 1.0, 'log-uniform'), 'num_leaves': (1, 100),      
'max_depth': (0, 50), 'min_child_samples': (0, 50),
'max_bin': (100, 1000), 'subsample': (0.01, 1.0, 'uniform'),
'subsample_freq': (0, 10), 'colsample_bytree': (0.01, 1.0, 'uniform'),
'min_child_weight': (0, 10), 'subsample_for_bin': (100000, 500000),
'reg_lambda': (1e-9, 1000, 'log-uniform'), 'reg_alpha': (1e-9, 1.0, 'log-uniform'),
'scale_pos_weight': (1e-6, 500, 'log-uniform'), 'n_estimators': (50, 100)}
  
grid_xgb = {
'learning_rate': [0.005, 0.05, 0.1], 'n_estimators': [10, 100, 250, 500],
'num_leaves': [6, 50, 100, 250, 500], 'boosting_type': ['gbdt', 'rf'],
'colsample_bytree' : [0.65, 1], 'subsample': [0.7, 0.9],
'reg_alpha': [0, 1.2], 'reg_lambda': [0, 2]}

      
grid_xgb_skopt = {
'learning_rate': Real(0.005, 0.1), 'n_estimators': Integer(10, 500),
'num_leaves': Integer(6, 50), 'boosting_type' : Categorical(['gbdt', 'rf']),
'colsample_bytree' : Real(0.65, 1), 'subsample' : Real(0.7, 0.9),
'reg_alpha' : Real(0, 1.2), 'reg_lambda' : Real(0, 2)}

param_grid_lgb = {
    'learning_rate': [0.005, 0.05, 0.1], 'n_estimators': [10, 100, 250, 500],
    'num_leaves': [6, 50, 100, 250, 500], 'boosting_type': ['gbdt', 'rf'],
    'colsample_bytree' : [0.65, 1], 'subsample': [0.7, 0.9],
    'reg_alpha': [0, 1.2], 'reg_lambda': [0, 2],
    }

param_grid_xgb = {'bootstrap': [True, False],
 'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
 'max_features': ['auto', 'sqrt'],
 'min_samples_leaf': [1, 2, 4],
 'min_samples_split': [2, 5, 10],
 'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}
 
 param_grid = {
    'learning_rate': Real(0.005, 0.1), 'n_estimators': Integer(10, 500),
    'num_leaves': Integer(6, 50), 'boosting_type' : Categorical(['gbdt', 'rf']),
    'colsample_bytree' : Real(0.65, 1), 'subsample' : Real(0.7, 0.9),
    'reg_alpha' : Real(0, 1.2), 'reg_lambda' : Real(0, 2),
    }

param_grid2 = {
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
        'n_estimators': (50, 100),
    }

param_grid3 = {
        'learning_rate': (0.01, 1.0, 'log-uniform'),
        'min_child_weight': (0, 10),
        'max_depth': (0, 50),
        'max_delta_step': (0, 20),
        'subsample': (0.01, 1.0, 'uniform'),
        'colsample_bytree': (0.01, 1.0, 'uniform'),
        'colsample_bylevel': (0.01, 1.0, 'uniform'),
        'reg_lambda': (1e-9, 1000, 'log-uniform'),
        'reg_alpha': (1e-9, 1.0, 'log-uniform'),
        'gamma': (1e-9, 0.5, 'log-uniform'),
        'min_child_weight': (0, 5),
        'n_estimators': (50, 100),
        'scale_pos_weight': (1e-6, 500, 'log-uniform')
    }

