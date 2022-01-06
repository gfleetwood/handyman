from subprocess import run
from re import search
from pandas import DataFrame

def extract_dict_from_str(string):
    """
    Extract a dictionary from a string
    """
    result = ast.literal_eval(re.search('({.+})', string).group(0))

    return(result)

def get_types_na_count(df):
    '''
    Returns a dataframe of df's columns types and NA counts for them
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

def read_function_def(func):

  from inspect import getsource
  func_source = get_source(func)

  return(func_source)

def read_postgres_con_str_components(con_str):

  '''
  con_str_format = "postgres://USERNAME_PASSWORD@HOST:PORT/DATABASE"
  '''

  con_str_wo_db = con_str.replace("postgres://", "")

  un = con_str_wo_db.split(":")[0]
  con_str_no_un = con_str_wo_db.replace(un + ":", "")

  pw = con_str_no_un.split("@")[0]
  con_str_no_pw = con_str_no_un.replace(pw + "@", "")

  host = con_str_no_pw.split(":")[0]
  con_str_no_host = con_str_no_pw.replace(host + ":", "")

  port = con_str_no_host.split("/")[0]
  db_name = con_str_no_host.replace(port + "/", "")

  payload = {"username": un, "password": pw, "host": host, "port": port, "database_name": db_name}

  return(payload)

def read_ips_on_network():

  ip_call = run(["ip", "addr", "show"], capture_output = True)
  tp_output = ip_call.stdout.decode('utf-8').replace("\n", "")
  ip_wlp = search(r'wlp3s0: (.*?) inet [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}', tp_output).group()
  ip_wlp_inet = search(r'inet [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}', ip_wlp).group()
  ip_wlp_inet_addr = search(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}', ip_wlp_inet).group()
  ip_wo_bits = ip_wlp_inet_addr.split(".")[:-1] + ["1"]
  ip_w_bits = ".".join(ip_wo_bits) + "/{}".format(ip_wlp_inet_addr.split("/")[-1])

  nmap_scan = run(["nmap", "-sP", ip_w_bits], capture_output = True)

  nmap_scan_ips = [
    x.replace("Nmap scan report for ", "") 
    for i, x in enumerate(nmap_scan.stdout.decode('utf-8').split("\n")[1:-2])
    if i%2==0
  ]

  nmap_scan_ips_temp = [x.replace(")", "").split("(") for x in nmap_scan_ips]

  nmap_scan_ips_named = [
    ["Unknown", x[0]] 
    if len(x) == 1
    else x
    for x in nmap_scan_ips_temp
  ]

  nmap_scan_df = DataFrame(nmap_scan_ips_named, columns = ["device_name", "ip_address"])
  
  return(nmap_scan_df)
