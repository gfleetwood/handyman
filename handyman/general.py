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

def load_libs(file_path = None, include_defaults = False, verbose = True):    
    
    defaults = [['numpy', 'np'], ['pandas', 'pd'], ['matplotlib.pyplot', "plt"], 
                ['sklearn.linear_model', "sk_lm"]]
    requirements = []
    
    if file_path is not None:
        requirements.extend(pd.read_csv(file_path).values.tolist())
        msg = "\nLoading user specified libraries from custom file"
        
        if include_defaults is True:
            try:
                requirements.extend(pd.read_csv("~/.pydato/pydato.csv").values.tolist())
                msg = "\nLoading user specified libraries from custom file and base"
            except:
                print("include_defaults is True but the file `~/.pydato/pydato.csv` doesn't exist")
        print(msg)
    else:    
        try:
            requirements.extend(pd.read_csv("~/.pydato/pydato.csv").values.tolist())
            msg = "\nLoading user specified libraries from base"
            print(msg)
        except:
            requirements.extend(defaults)
            msg = "\nLoading default libraries"
            print(msg)
    
    imported_libs = {lib[1]: importlib.import_module(lib[0]) for lib in requirements}  
    
    print("_"*len(msg) + "\n")
    
    if verbose is True:         
        loaded_libs = list(map(lambda x: print(x[0] + " loaded as " + x[1] + "\n"), requirements))
        loaded_libs
        
    return(imported_libs)
