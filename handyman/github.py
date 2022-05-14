from os import environ
from github import Github

def github():

  '''
  # Examples

  # Set repo labels

  labels = ["feature", "enhancement", "bug", "backlog", "documentation"]

  g = Github(os.environ.get("GHUB"))
  g_usr = g.get_user()
  repos = list(g_usr.get_repos())
  vader_repos = [x for x in repos if "vader" in x.full_name]
  _ = [normalize_repo_labels(repo) for repo in vader_repos]

  # Save issues to db

  g = Github(os.environ.get('GHUB'))
  con_str = "sqlite:////repo_issues.db" 
  eng = create_engine(con_str)
  repo = g.get_repo(os.environ.get('EXAMPLE_REPO'))
  issues = [x for x in repo.get_issues()]
  issues_df = pd.DataFrame([get_issue_data(issue) for issue in issues])
  issues_df.to_sql("TBL", con = eng, index = False, if_exists = "replace")
  '''

  rand_color = lambda: random.randint(0,255)
  rand_hex_color = lambda: '%02X%02X%02X' % (rand_color(), rand_color(), rand_color())

def get_issue_data(issue):
    
    result =     {
        "title": issues[0].title, 
        "body": [issues[0].body],
        "state": [issues[0].state],
        "assignees": ["|||".join(issues[0].assignees)],
        "comments": ["|||".join([x.body for x in issues[0].get_comments()])],
        'created_at': [issues[0].created_at.isoformat()],
        "labels": ["|||".join([x.name for x in issues[0].get_labels()])]
    }
    
    return(result)

def normalize_repo_labels(repo):
    
    repo_labels = [x for x in repo.get_labels()]
    repo_label_names = [x.name for x in repo_labels]
    _ = delete_unneeded_labels(repo_labels)
    _ = create_new_labels(repo, repo_label_names)
    
    return(True)
    
def delete_unneeded_labels(repo_labels):
    
    for x in repo_labels:
        if x.name not in labels:
            x.delete()
    
    return(True)

def create_new_labels(repo, repo_label_names):
    
    for x in labels:
        if x not in repo_label_names:
            repo.create_label(x, rand_hex_color().lower())
        
    return(True)

def create_repo_labels():
  labels = ["backlog", "bug", "documentation", "enhancement", "feature"]
  g = Github(environ["GHUB"])
  user_info = g.get_user()
  a = user_info.get_repos()[0] 
  #for label in a.get_labels(): label.delete()
  #for label in labels: a.create_label(label, color = "0000FF")
  
  return(True)
  
  

