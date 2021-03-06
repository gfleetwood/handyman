# Set repo labels

import handyman.github as ghub

labels = ["feature", "enhancement", "bug", "backlog", "documentation"]

g = Github(os.environ.get("GHUB"))
g_usr = g.get_user()
repos = list(g_usr.get_repos())
vader_repos = [x for x in repos if "vader" in x.full_name]
_ = [normalize_repo_labels(repo) for repo in vader_repos]

'''
g = Github(os.environ.get('GHUB'))
con_str = "sqlite:////repo_issues.db" 
eng = create_engine(con_str)
repo = g.get_repo(os.environ.get('EXAMPLE_REPO'))  
issues = [x for x in repo.get_issues()]

issues_df = pd.DataFrame([get_issue_data(issue) for issue in issues])
issues_df.to_sql("TBL", con = eng, index = False, if_exists = "replace")
'''

'''
eng = create_engine("sqlite://experimental_conditions.db" )

# DB To Nx

df = pd.read_sql("SELECT * FROM experimental_conditions", con = eng)
edges = []
G = nx.DiGraph()

for row in df.iterrows():
    
    G.add_node(
    row[1]["database_num"], 
    experiment_num = row[1]["experiment_num"],
    bay_num = row[1]["bay_num"],
    strain = row[1]["strain"],
    function = row[1]["function"],
    media = row[1]["media"],
    carbon_source = row[1]["carbon_source"],
    cells_added = row[1]["cells_added"],
    cells_source = row[1]["cells_source"]
    )
    
    node_edges = [
        [row[1]["database_num"],j]
        for j in row[1]["edges_out"].split("-") 
        if len(j) != 0
    ]
    
    edges.append(node_edges)

edges_flattened = sum(edges, [])

for edge in edges_flattened:
    G.add_edge(edge[0], edge[1])
'''
