def extract_dict_from_str(string):
    """
    Extract a dictionary from a string
    """
    result = ast.literal_eval(re.search('({.+})', string).group(0))

    return(result)

def get_types_na_count(df):
    '''
    @description Returns columns types and NA counts for them
    @param df A dataframe
    @return A dataframe of columns types and NA counts for them
    '''
    result = pd.concat([df.dtypes, df.isnull().sum()], axis = 1)
    result.columns = ["type", "na_count"]

    return(result)
  
def data_diagnostics(df, num_cols, cat_cols):
    '''
    @description Constructs a combined numerical and categorical summary for a dataframe
    @param df A dataframe
    @param num_cols A list of numeric columns
    @param cat_cols A list of categorical columns
    @return A dataframe of columns types and NA counts for them
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
    
    result = [num_summary_full, cat_summary]

    return(result)


def flatten_dict(y):  
    '''
    @description Flatten an arbitrarily nested dictionary. Source: https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
    @param y A dictionary
    @return A flattened version of y 
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

def get_object(name):
    
    grid_kkn = {'leaf_size': [30, 40, 50, 60, 70, 80, 90],
             'n_neighbors': [5, 15, 25, 35, 45, 55, 65, 75, 85]}
             
    grid_rf = {
    'bootstrap': [True, False], 'max_features': ['auto', 'sqrt'],
    'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
    'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 5, 10],
    'n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}
    
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
    'reg_alpha': [0, 1.2], 'reg_lambda': [0, 2]} 
    
    param_grid_xgb = {
    'bootstrap': [
        True, False], 'max_depth': [
        10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None], 'max_features': [
        'auto', 'sqrt'], 'min_samples_leaf': [
        1, 2, 4], 'min_samples_split': [
            2, 5, 10], 'n_estimators': [
        200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}
                  
    object_dict = {
        "grid_kkn": grid_kkn,
        "grid_rf": grid_rf,
        "grid_lgb": grid_lgb,
        "grid_xgb": grid_xgb,
        "grid_xgb_skopt": grid_xgb_skopt,
        "param_grid_lgb": param_grid_lgb,
        "param_grid_xgb": param_grid_xgb
    }
    
    result = object_dict(name)
                  
    return(result)
