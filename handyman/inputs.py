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
