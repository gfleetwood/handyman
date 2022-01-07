import pandas as pd
from sqlalchemy import create_engine
import pandas as pd

def get_exp_shap_vals(mdl, X, y):

    """
    fplot = shap.force_plot(explainer.expected_value, shap_vals[45,:], X_train.iloc[45,:], link = 'logit')
    """

    mdl.fit(X.values, y.values)
    explainer = shap.TreeExplainer(test, model_output = "probability")
    shap_values = explainer.shap_values(X.values)

    payload = (explainer, shap_values)

    return(payload)

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

    top = [ ['f1', float("NaN"), x['outValue']],
           ['f2', float("NaN"), x['baseValue']], 
     ['f3', float("NaN"), x["outValue"] - x['baseValue']]]

    bottom = [
        ['feature_' + j, x['features'][str(i)]['value'], x['features'][str(i)]['effect']]
        for i,j in enumerate(x['featureNames'])]

    result = (
    pd.DataFrame(top + bottom, columns = ['c1', 'c2', 'c3'])
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
      'c1': [x['outValue']],
      'c2': [x['baseValue']],
      'c3': [x["outValue"] - x['baseValue']]
      }

    data_dict_features = {
      j: [x['features'][str(i)]['effect']] # x['features'][str(i)]['value']
      for i,j in enumerate(x['featureNames'])
      }

    data_dict.update(data_dict_features)
    result = pd.DataFrame(data_dict)

    return(result)

def get_ldiag(mat, loc):

    # Getting diagonals from a numpy matrix    
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

def sort_md_by_headings(file, heading):

    # te = sort_md_by_headings(file, "\n# ")
    
    if re.search(heading, file) is None:
        return(heading[:-2] + " " + file) 
    
    result = ""
    temp = re.split(heading, file)
    
    result = result + \
    heading[:-2] + " " + temp[0] + "\n" + \
    "\n".join([
        sort_md_by_headings(x, heading[:-1] + "# ") + "\n"
        for x in sorted(temp[1:])
    ])

    return(result.strip().replace("\n\n\n", "\n\n"))

def get_hackernews_favorites(user):
    
    more_favorites = True
    counter = 1
    url_base = "https://news.ycombinator.com/"
    url = url_base + "favorites?id={}&p={}"
    data = []

    while more_favorites:

        te = r.get(url.format(user, str(counter)))
        soup = bs(te.content)

        df = pd.DataFrame([
        (x.find("a", {"class": "storylink"}).text, x.find("a", {"class": "storylink"})['href'])
        for x in soup.find_all("tr", {"class": "athing"})
        ], columns = ["name", "link"])

        data.append(df)

        if counter > 20:
            break

        counter = counter + 1

    data_df = pd.concat(data)
    
    return(data_df)

def print_repos_info(base_dir, repos):
 
  import os

  repos_full_paths = [os.path.join(base_dir, r) for r in repos]
  _ = [print_repo_info(x) for x in repos_full_paths]

  return(True)

def print_repo_info(repo_path):

  r = subprocess.run(["git", "status"], capture_output = True, cwd = "{}".format(repo_path))

  print(repo_path, end = "\n\n")
  print(r.stdout.decode('utf-8'), end = "\n-------------------------\n\n")

  return(True)

def controller():

   for file in ".local/share/Trash": rewrite_file(file)

   return(True)

def trash_img(img_path):

    img = rgb2gray(io.imread(img_path))
    img[:,:] = 0
    io.imsave(img_path, img)

    return(True)

def trash_pdf(*pdf_paths):

    from pdfrw import PdfWriter

    for pdf_path in pdf_paths:
        y = PdfWriter()
        y.write(pdf_path)

    return(True)

def trash_mp3(file_path):
    
    os.system("ffmpeg -y -f lavfi -i anullsrc=r=11025:cl=mono -t 60 -acodec aac {}".format(file_path))
    
    return(True)

def not_yet_defined(path):
    
    return("Function not yet defined for this file type")

def rewrite_file(path):

    file_type = path.split(".")[-1]
    trash_file = {"pdf": trash_pdf, "mp3": trash_mp3, "jpg": trash_img}
    result = trash_file.get(file_type, not_yet_defined)(path)

    return(result)

def db_to_nx_digraph(df, source_node_col, target_nodes_col):
    
    """
    Converts a dataframe with node attributes to a networkx digraph. 
    
    Params:
    
    df: A pandas dataframe with the source node, targets nodes, and any node metadata.
    source_node_col: The name of the column for the source nodes
    target_nodes_col: The name of the column with the target nodes as a "-" separated string
    
    Returns: 
    
    df_graph: A pandas dataframe with the source node, targets nodes, and any node metadata.
    """
    
    G = nx.DiGraph()
    edges_nested = []
    
    for row in df.iterrows():
        
        G.add_node(row[1][source_node_col])
        
        node_edges = [
            [row[1][source_node_col], target_node]
            for target_node in row[1][target_nodes_col].split("-") 
            if len(target_node) != 0
        ]
        
        edges_nested.append(node_edges)
    
    edges_flattened = sum(edges_nested, [])
    
    for edge in edges_flattened:
        G.add_edge(edge[0], edge[1])
        
    node_attrs = {}
    
    for record in df.to_dict(orient = "records"): 
        node_attrs.update({record[nodes_col]: {attribute: value for (attribute, value) in record.items() if attribute != nodes_col}})
        
    nx.set_node_attributes(G, node_attrs)
    
    return(G)
    
def nx_digraph_to_df(G, columns_df, source_node_col, target_nodes_col):
    
    """
    Converts a networkx digraph to a dataframe preserving node attributes. 
    
    Params:
    
    G: A networkx digraph
    columns_df: The column names absent two: the column for the source node and the one for the target nodes.
    source_node_col: The name of the column for the source nodes
    target_nodes_col: The name of the column to with the target nodes as a "-" separated string
    
    Returns: 
    
    df_graph: A pandas dataframe with the source node, targets nodes, and any node metadata.
    """
    
    nodes = list(G.nodes)
    edges = list(G.edges)

    # Building a dictionary of source nodes as keys and a list of target nodes as values before storage in the dataframe
    # The target nodes are stored in a column as "-" separated strings
    # For example if there are edges A -> B and A -> C then in A's row this is stored as "B-C"
    
    edges_dict = {x[0]: [] for x in list(G.edges)}
    
    for edge in edges:
        edges_dict[edge[0]].append(edge[1])
       
    edges_dict_formatted = {i:"-".join(j) for (i,j) in edges_dict.items()}
    
    reconstruct_df = {
        source_node_col: nodes, 
        target_nodes_col: [edges_dict_formatted.get(node, "") for node in nodes]
    }
    
    cols_from_node_metadata = [col for col in columns_df if col not in [source_node_col, target_nodes_col]]
    
    for col in cols_from_node_metadata:
        reconstruct_df.update({col: [G.nodes[node][col] for node in nodes]})
    
    df_graph = pd.DataFrame(reconstruct_df)
    
    return(df_graph)

def create_issue_from_starred_repo(star, repo):
  
    issue_title = "{} ({})".format(star[1], star[0])
    issue_body = "{}\n\n{}".format(star[2], star[3])
    issue_lang = star[4]
    repo.create_issue(title = issue_title, body = issue_body)
    
    time.sleep(3)
      
    return(1)

def read_repo_id_from_issue(issue):
    
    result = int(issue.title.split("(")[1].replace(")", ""))
    
    return(result)
    
def create_issue_from_starred_repo_df(df, repo):
    """
    Takes in a dataframe of a starred repos data and makes it a issue
    for the repo
    """
    
    issue_title = "{} ({})".format(df['name'], df['repo_id'])
    issue_body = "{}\n\n{}".format(df['url'], df['description'])
    issue_tags = [tag for tag in df['tags_lang'].split(",")]
    
    if issue_tags[0] == "no-tag":
          
        repo.create_issue(
          title = issue_title, 
          body = issue_body
          )
    else:
        repo.create_issue(
          title = issue_title, 
          body = issue_body, 
          labels = issue_tags
          )
    
    # This is usually processed functionally as a batch so the delay
    # sidesteps GitHub API limiting
    time.sleep(3)
    
    return(1)

def get_comment_formats(row):
    
    payload = [tbl_description, column_description]
    
    return(payload)

def tbl_description(row):
    
    postgres_tbl_comment_template = '''
    COMMENT ON TABLE {schema}.{table} IS 'ENTER DESCRIPTION HERE'
    '''
    
    payload = postgres_tbl_comment_template.format(
        schema = row.table_schema, 
        table = row.table_name
    ).replace("\n", "", 1)
    
    return(payload)

def column_description(row):
    
    postgres_column_comment_template = '''
    COMMENT ON COLUMN {table}.{column} IS 'ENTER DESCRIPTION HERE'
    '''
    
    payload = postgres_column_comment_template.format(
        table = row.table_name, 
        column = row.column_name
    ).replace("\n", "", 1)
    
    return(payload)

def rename_multi_index_cols(columns):

   "Assumes reset_index has been run on the multi-index dataframe"
    
    payload = [
    '_'.join(col).strip() 
    if len(' '.join(col).strip() .split(" ")) > 1
    else ''.join(col).strip()
    for col in df.columns.values
    ]
    
    return(payload)
