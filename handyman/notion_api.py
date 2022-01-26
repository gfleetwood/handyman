def read_database():

  url = f"https://api.notion.com/v1/databases/{databaseId}/query"
  res = requests.request("POST", url, headers = headers)
  data = res.json()

  return(data)
