from skopt.space import Real, Integer, Categorical
import numpy as np

grid_kknr = {'leaf_size': [30, 40, 50, 60, 70, 80, 90],
             'n_neighbors': [5, 15, 25, 35, 45, 55, 65, 75, 85]}

grid_rf = {
    'bootstrap': [True, False], 'max_features': ['auto', 'sqrt'],
    'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
    'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 5, 10],
    'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}

grid_rf_skopt = {
    "max_depth": Integer(
        3, 10), "n_estimators": Integer(
        100, 500), "max_features": Categorical(
        [
            'sqrt', 'log2']), "min_samples_split": Integer(
        2, 50), "min_samples_leaf": Integer(
        2, 50), "criterion": Categorical(
        ['entropy'])}

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
    'colsample_bytree': [0.65, 1], 'subsample': [0.7, 0.9],
    'reg_alpha': [0, 1.2], 'reg_lambda': [0, 2]}


grid_xgb_skopt = {
    'learning_rate': Real(0.005, 0.1), 'n_estimators': Integer(10, 500),
    'num_leaves': Integer(6, 50), 'boosting_type': Categorical(['gbdt', 'rf']),
    'colsample_bytree': Real(0.65, 1), 'subsample': Real(0.7, 0.9),
    'reg_alpha': Real(0, 1.2), 'reg_lambda': Real(0, 2)}

param_grid_lgb = {
    'learning_rate': [0.005, 0.05, 0.1], 'n_estimators': [10, 100, 250, 500],
    'num_leaves': [6, 50, 100, 250, 500], 'boosting_type': ['gbdt', 'rf'],
    'colsample_bytree': [0.65, 1], 'subsample': [0.7, 0.9],
    'reg_alpha': [0, 1.2], 'reg_lambda': [0, 2],
}

param_grid_xgb = {
    'bootstrap': [
        True, False], 'max_depth': [
        10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None], 'max_features': [
        'auto', 'sqrt'], 'min_samples_leaf': [
        1, 2, 4], 'min_samples_split': [
            2, 5, 10], 'n_estimators': [
        200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}

param_grid = {
    'learning_rate': Real(0.005, 0.1), 'n_estimators': Integer(10, 500),
    'num_leaves': Integer(6, 50), 'boosting_type': Categorical(['gbdt', 'rf']),
    'colsample_bytree': Real(0.65, 1), 'subsample': Real(0.7, 0.9),
    'reg_alpha': Real(0, 1.2), 'reg_lambda': Real(0, 2),
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

grid_xgb_small = {'learning_rate': [0.005, 0.05, 0.1],
                  'n_estimators': [10, 100, 250, 500],
                  'num_leaves': [6, 50, 100, 250, 500],
                  'boosting_type': ['gbdt', 'rf'],
                  'colsample_bytree': [0.65, 1],
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
    'n_estimators': np.arange(50, 100, 10)}

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
    "max_features": Categorical(['sqrt', 'log2']),
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
    'n_estimators': Integer(10, 100)}
