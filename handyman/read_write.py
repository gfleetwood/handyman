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

def get_file_paths(path):
    '''
    @description Sample from a csv on disk
    @param fpath The path to the file
    @param nrows The number of rows to sample
    @return An sample of the file
    '''    
  
    result =  [
    os.path.join(dp, f) 
    for dp, dn, filenames in os.walk(path) 
    for f in filenames
                ]
                
    return(result)

def list_all_files_recursive(raw_path):

    abs_path = os.path.abspath(raw_path)
    files = [path + "/" + file for file in os.listdir(abs_path)]

    return(files)
