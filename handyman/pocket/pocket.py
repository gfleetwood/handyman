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
