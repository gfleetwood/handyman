from os import environ

def aws():

  s3_client = boto3.client('s3')
  s3 = boto3.resource('s3')

  s3_client.list_buckets()
  bucket = s3.Bucket(os.environ["S3_BUCKET"])
  objs = bucket.objects.filter(Prefix = '')

  session = boto3.Session(profile_name = '')
  #for bucket in s3.buckets.all(): print(bucket.name)

  for obj in objs:
    s3_client.download_file(
      os.environ["S3_BUCKET"],
      obj.key,
      "/home/USER/Downloads" + obj.key
    )

  files = [obj.key for obj in s3.Bucket(bucket_name).objects.filter(Prefix = '/')]
    
  for file in files:
    s3.Bucket(bucket_name).download_file(file, "/home/" + os.path.split(file)[1]) 

def get_pocket_data():

  params = {
    "consumer_key": os.environ.get("POCKETKEY"), 
    "access_token": os.environ.get("POCKETTOKEN"),
    "detailType": "complete", 
    "state": "archive"
  }

  pocket_items = requests.post("https://getpocket.com/v3/get", data = params)
  pocket_items_list = list(pocket_items.json()['list'].items())

  data = [
  [x[1]['given_title'], x[1]['given_url'], ' ~ '.join(list(x[1]['tags'].keys()))] 
  for x in pocket_items_list
  ]

  df = pd.DataFrame(data, columns = ['title', 'url', 'tags'])

  return(df)

def get_dbx_con():
    
    dbx_con = dropbox.Dropbox(os.environ['DBox'])

    return(dbx_con) 

def get_dbx_files(folder: str):

    files = dbx.files_list_folder("folder")
    results = [
       dbx.files_download(entry.path_lower)
       for entry in files.entries
       if (isinstance(entry, dropbox.files.FileMetadata))
    ]

    return(results)

def update_dbx_rename_or_move_file(old_file_path: str, new_file_path: str) -> bool:

  dbx.files_move(
    img_metadata.path_display,
    img_metadata.path_display.replace(old_file_path, new_file_path)
  )
  
  return(True)

def access_dbx_file():
  
  img_metadata = files_new_info[0]
  img_bytes = img_new_info[1].content
  img_pil = Image.open(BytesIO(img_to_process_bytes))
  img_np = np.asanyarray(img_to_process_pil)

  return(img_np)

def convert_img_np_to_bytes(img_np):
    
    # Work around for limitations of PIL library: https://stackoverflow.com/a/47292141
    img_pil = Image.fromarray((img_np * 255).astype(np.uint8), mode = 'L')
    img_bytes = io2.BytesIO()
    #img_pil = img_pil.convert("") 
    img_pil.save(img_bytes, format = 'JPEG')
    img_bytes = img_bytes.getvalue()
    
    return(img_bytes)

def save_image(dbx, img, fname):
    
    img_bytes = convert_img_np_to_bytes(img)
    dbx.files_upload(img_bytes, fname)

    return(True)

def get_img_info_dbx(dbx, entry):

    img_info = dbx.files_download(entry.path_lower)
    img_to_process_metadata = img_info[0]
    img_to_process_bytes = img_info[1].content
    img_to_process_pil = Image.open(BytesIO(img_to_process_bytes))
    img_to_process_np = np.asanyarray(img_to_process_pil)
    result = (img_to_process_np, img_to_process_metadata.name)

    return(result)

def save_img_dbx(dbx, new_img_path, img):

    img_pil = Image.fromarray(img)
    img_bytes = io2.BytesIO()
    img_pil.save(img_bytes, format = 'JPEG')
    img_bytes = img_bytes.getvalue()
    dbx.files_upload(img_bytes, os.path.join(new_img_path, img_name))

    return(True)

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
