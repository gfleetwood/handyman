def read_csv_sample(fpath, nrows, seed = 8, header = "-r"):

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
    
    sample = sp.getoutput('subsample -s {seed} -n {nrows} {fpath} {header}'\
                          .format(seed = seed, nrows = nrows, fpath = fpath, header = header))
    
    # Remove the first line which is metadata
    sample_cleaned = StringIO(sample[(sample.find("\n") + 1):])
    
    df = pd.read_csv(sample_cleaned, sep = ",")
    
    return(df)
    
def get_data(server, un, pwd, driver, db, query):
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
    
    con = pyodbc.connect('DRIVER=' + driver +
                     ';PORT=1433;' 'SERVER=' + server +
                     ';PORT=1443;' 'DATABASE=' + db +
                     ';UID=' + un + ';PWD=' + pwd)
                     
    cursor = con.cursor()
    cursor.execute(query)
    cols = [column[0] for column in cursor.description]
    data = [list(row) for row in cursor.fetchall()]
    df = pd.DataFrame(data = data, columns = cols)

    cursor.close()
    con.close()
    return(df)

def set_data(server, un, pwd, driver, db, query, data):
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
    con = pyodbc.connect('DRIVER=' + DRIVER +
                     ';PORT=1433;' 'SERVER=' + SERVER +
                     ';PORT=1443;' 'DATABASE=' + DB +
                     ';UID=' + USERNAME + ';PWD=' + PASSWORD)
    cursor = con.cursor()
    
    #query ex: "insert into reference.{tbname}({c1}, {c2}, depth) values (%d, %d, %d)"
    for val in data:
        cursor.execute(insertion_query)
        CXN.commit()

    cursor.close()
    con.close()
    return 'Write Done'
