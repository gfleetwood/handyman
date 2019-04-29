import importlib
import pickle
import pandas as pd
import datetime

def pydata(libs = None, verbose = True):
    '''
    @description Import multiple libraries at once. Call: globals().update(pydata())
    @param libs A list of lists containing libraries to be imported and their aliases
    @param verbose A boolean indicator of whether or not to print the names of the imported libraries
    @return An object to add to the globals() object
    '''
    if libs is None: 
    
        libs = [['pd', 'pandas'], ['sk_lm', 'sklearn.linear_model'], ['np', 'numpy'],
                ['pn', 'plotnine'], ['plt', 'matplotlib.pyplot'], ['lz', 'logzero']]
  
    imported_libs = {lib[0]: importlib.import_module(lib[1]) for lib in libs}
    
    if verbose:  
        for lib in libs: 
            print(lib[1] + " loaded as " + lib[0])
    
    return imported_libs
    
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
    @description Flatten an arbitrarily nested dictionary.
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
    
def get_date_time():  
    '''
    @description Returns the system date and time as a string.
    @return The date in ISO-8601 
    '''
    return str(datetime.datetime.now()).split(' ')

