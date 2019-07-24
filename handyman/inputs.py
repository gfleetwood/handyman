import pandas as pd
import subprocess as sp
import pyodbc
from io import StringIO

def read_csv_sample(fpath, nrows, seed = 8, header = "-r"):
    '''
    @description Sample from a csv on disk
    @param fpath The path to the file
    @param nrows The number of rows to sample
    @return An sample of the file
    '''    
    sample = sp.getoutput('subsample -s {seed} -n {nrows} {fpath} {header}'\
                          .format(seed = seed, nrows = nrows, fpath = fpath, header = header))
    
    # Remove the first line which is metadata
    sample_cleaned = StringIO(sample[(sample.find("\n") + 1):])
    
    df = pd.read_csv(sample_cleaned, sep = ",")
    
    return(df)
    
def get_data(server, un, pwd, driver, db, query):
    '''
    @description Runs a SQL query and returns the results
    @param server The server of the database
    @param un The username
    @param pwd The password
    @param driver The driver
    @param db The name of the database
    @param query The query to run
    @return A dataframe of the query results
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
    @description Runs a SQL query and returns the results
    query ex: "insert into reference.{tbname}({c1}, {c2}, depth) values (%d, %d, %d)
    @param server The server of the database
    @param un The username
    @param pwd The password
    @param driver The driver
    @param db The name of the database
    @param query The query to run
    @param data The data to insert
    @return A confirmation message
    '''
    con = pyodbc.connect('DRIVER=' + driver +
                     ';PORT=1433;' 'SERVER=' + server +
                     ';PORT=1443;' 'DATABASE=' + db +
                     ';UID=' + un + ';PWD=' + pwd)
    cursor = con.cursor()
    
    for val in data:
        cursor.execute(query.format(val))
        con.commit()

    cursor.close()
    con.close()

    return('Write Done')
