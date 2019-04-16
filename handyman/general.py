import importlib

def pydata(libs = None, verbose = False):

    '''
    Role
    ----
    globals().update(pydata())
  
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

    if libs is None: 
    
        libs = [
    ['pd', 'pandas'], ['sk', 'sklearn'], ['np', 'numpy'], ['pn', 'plotnine'], ['plt', 'matplotlib.pyplot'],
    ['lz', 'logzero'], ['pandasql', 'pandasql'],
    ]
  
  imported_libs = {lib[0]: importlib.import_module(lib[1]) for lib in libs}
  
  if verbose:  
    for lib in libs: 
        print(lib[1] + " loaded as " + lib[0])
  
  return imported_libs


def exclusion(x,y): 
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

    result = lambda x,y: [j for i,j in enumerate(x) if i != y]
    return(result)
    
def get_types_na_count(df):
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
  result = pd.concat([df.dtypes, df.isnull().sum()], axis = 1)
  result.columns = ["type", "na_count"]
  return(result)
  
  
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


def flatten_dict(y):  
    '''
    Role
    ----
    Flatten an arbitrarily nested dictionary.
    
    Parameters
    ---------
    * y: A dictionary
  
    Returns
    -------    
    * out: A flattened version of y. 
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
    * * A list contains two elements as strings: 1) date, and 2) time.
    '''
    return str(datetime.datetime.now()).split(' ')

