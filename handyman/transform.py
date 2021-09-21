def impute_scale_data(df):

    '''
    Imputes missing values with the median for numeric features and the mode for categorical ones, 
    and then scales the numeric features by subtracting the mean and dividing by the standard deviation.
    '''    

    imputer_num = sk_pp.Imputer(strategy = 'median') 
    df.loc[:, df.select_dtypes(exclude = ['object']).columns] = \
    imputer_num.fit_transform(df.select_dtypes(exclude = ['object']))  
    
    scaler = sk_pp.StandardScaler()
    df.loc[:, df.select_dtypes(exclude = ['object']).columns] = \
    scaler.fit_transform(df.select_dtypes(exclude = ['object']))
    
    for col in df.select_dtypes(include = ['object']).columns:
        df.loc[:, col] = df.loc[:, col].fillna(value = df.loc[:, col].value_counts().index[0])
        
    df_imputed_scaled = df
        
    return(df_imputed_scaled)
