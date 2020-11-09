def adverserial_validation(X1, X2):
    """
    Get the top resulting cricle from the hough circle transform
    """

    df_av = pd.concat([X2.assign(test=1), X1.assign(test=0)], axis=0)
    mdl_av = sk_lm.LogisticRegression()
    training_scores_av = sk_ms.cross_val_score(
        mdl_av,
        df_av.drop(['test'], axis=1),
        df_av.test.values,
        cv = 5,
        scoring='roc_auc'
        )
        
    results = (training_scores_av.mean(), training_scores.std())

    return(results)

def subset_by_iqr(df, column, whisker_width = 1.5):
    """
    Get the top resulting cricle from the hough circle transform
    """

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    mask = (
        df[column] >= q1 -
        whisker_width *
        iqr) & (
        df[column] <= q3 +
        whisker_width *
        iqr)

    return df.loc[mask]

def get_exp_shap_vals(mdl, X, y):
    """
    fplot = shap.force_plot(explainer.expected_value, shap_vals[45,:], X_train.iloc[45,:], link = 'logit')
    """

    mdl.fit(X.values, y.values)
    explainer = shap.TreeExplainer(test, model_output = "probability")
    shap_values = explainer.shap_values(X.values)

    return((explainer, shap_values))

def date_decomposition(df, col):
    """
    Get the top resulting cricle from the hough circle transform
    """

    result = df.assign(
        hour = lambda x: x[col].dt.hour,
        day = lambda x: x[col].dt.day,
        month = lambda x: x[col].dt.month,
        year = lambda x: x[col].dt.year
    )

    return(result)


def get_shap_df(shap_values, X):
    
    df_shap = pd.DataFrame(
        list(zip(np.mean(shap_values, axis = 0), X.columns)),
        columns = ['shap_mean', 'feature']
        )
    df_shap = df_shap[['feature', 'shap_mean']]
    df_shap['shap_mean_abs'] = np.absolute(df_shap['shap_mean'])
    df_shap.sort_values(['shap_mean_abs'], ascending = False, inplace = True)

    return(df_shap)

def shap_breakdown_row_oriented(data):
    """
    Gives the SHAP breakdown for a single record with a row for each column name
    """
    x = ast.literal_eval(re.search('({.+})', data).group(0))

    top = [ ['LoS_student_prediction', float("NaN"), x['outValue']],
           ['LoS_base_prediction', float("NaN"), x['baseValue']], 
     ['student_base_diff_val', float("NaN"), x["outValue"] - x['baseValue']]]

    bottom = [
        ['feature_' + j, x['features'][str(i)]['value'], x['features'][str(i)]['effect']]
        for i,j in enumerate(x['featureNames'])]

    result = (
    pd.DataFrame(top + bottom, columns = ['characteristic', 'student_data', 'shap_val_log_odds'])
    .assign(shap_probability = lambda x: np.exp(x.shap_val_log_odds) / ( 1 + np.exp(x.shap_val_log_odds)))
    .round(2)
    )

    return(result)
  
def shap_breakdown_col_oriented(data):
    """
    Gives the SHAP breakdown for a single record across the data's columns
    """
    x = ast.literal_eval(re.search('({.+})', data).group(0))

    data_dict = {
      'LoS_student_prediction': [x['outValue']],
      'LoS_base_prediction': [x['baseValue']],
      'student_base_diff_val': [x["outValue"] - x['baseValue']]
      }

    data_dict_features = {
      j: [x['features'][str(i)]['effect']] # x['features'][str(i)]['value']
      for i,j in enumerate(x['featureNames'])
      }

    data_dict.update(data_dict_features)
    result = pd.DataFrame(data_dict)

    return(result)

# Getting diagonals from a numpy matrix

def get_ldiag(mat, loc):
    
    result = np.concatenate((get_ldiag_upper(mat, loc), get_ldiag_lower(mat, loc)))
    
    return(result)

def get_ldiag_upper(mat, loc):
    
    row, col = loc[0], loc[1]
    nrow, ncol = mat.shape[0], mat.shape[1]
    locs = list(zip(range(row - 1, -1, -1), range(col - 1, -1, -1)))
    
    result = [mat[pos] for pos in locs][::-1]
    
    return(result)

def get_ldiag_lower(mat, loc):
    
    row, col = loc[0], loc[1]
    nrow, ncol = mat.shape[0], mat.shape[1]
    locs = list(zip(range(row, nrow), range(col, ncol)))
    
    result = [mat[pos] for pos in locs]
    
    return(result)

def get_nldiag(mat, loc):
        
    result = np.concatenate((get_nldiag_upper(mat, loc), get_nldiag_lower(mat, loc)))
    
    return(result)

def get_nldiag_upper(mat, loc):
    
    row, col = loc[0], loc[1]
    nrow, ncol = mat.shape[0], mat.shape[1]
    locs = list(zip(range(row - 1, -1, -1), range(col + 1, ncol)))
    
    result = [mat[pos] for pos in locs][::-1]
    
    return(result)

def get_nldiag_lower(mat, loc):
    
    row, col = loc[0], loc[1]
    nrow, ncol = mat.shape[0], mat.shape[1]
    locs = list(zip(range(row, nrow), range(col, -1, -1)))
    
    result = [mat[pos] for pos in locs]
    
    return(result)

def url_status_code(url):
    
    try:
        result = requests.get(x).status_code != 200
    except:
        result = -1
        
    
    return([url, result])

'''
g = Github(os.environ.get('GHUB'))
con_str = "sqlite:////repo_issues.db" 
eng = create_engine(con_str)
repo = g.get_repo(os.environ.get('EXAMPLE_REPO'))  
issues = [x for x in repo.get_issues()]

issues_df = pd.DataFrame([get_issue_data(issue) for issue in issues])
issues_df.to_sql("TBL", con = eng, index = False, if_exists = "replace")
'''

def get_issue_data(issue):
    
    result =     {
        "title": issues[0].title, 
        "body": [issues[0].body],
        "state": [issues[0].state],
        "assignees": ["|||".join(issues[0].assignees)],
        "comments": ["|||".join([x.body for x in issues[0].get_comments()])],
        'created_at': [issues[0].created_at.isoformat()],
        "labels": ["|||".join([x.name for x in issues[0].get_labels()])]
    }
    
    return(result)
