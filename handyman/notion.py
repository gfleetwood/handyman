import requests
import json
from flatten_json import flatten
from pandas import DataFrame
from os import environ
from functools import reduce

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

token = environ["NOTION_DISPLAY_WS_TOKEN"]
databaseId = environ["NOTION_DISPLAY_DB_ID"]

def read_database(databaseId):

  url = f"https://api.notion.com/v1/databases/{databaseId}/query"
  res = requests.request("POST", url, headers = headers)
  data = res.json()

  return(data)

def read_tbl():

  data = DataFrame(read_database(databaseId)['results'])[["properties"]]
  columns = data.head(1)["properties"].values[0].keys()

  result = (
  reduce(read_column_info, columns, data)
  [columns]
  #.assign(time = lambda x: [y["Time Created"]["created_time"] for y in x.properties])
  )

  return(result)
  
def read_workspace():
  
  response = requests.post('https://api.notion.com/v1/search', headers = headers)s
  result = res.json()

  return(result)

def read_page():
  
  url = f"https://api.notion.com/v1/pages/{page_id}"
  res = requests.request("GET", url, headers = headers)
  data = res.json()

  return(data)

def read_database(db_id):

  url = f"https://api.notion.com/v1/databases/{databaseId}/query"
  res = requests.request("POST", url, headers = headers)
  data = res.json()

  return(data)

def read_child_page_content(child_page):
  
  result = ""
  
  for x in child_page.json()["results"]:
    plain_text = read_plain_text(x)
    result = result + plain_text + "\n\n" 
    
  return(result)

def read_plain_text(x):

  x_flat = flatten(x)
  relevant_key = [key for key in list(x_flat.keys()) if "plain_text" in key]
  payload = x_flat[relevant_key[0]] if len(relevant_key) > 0 else ""

  return(payload)

def read_column_info(df, col_name)

  df.assign(**{col_name: lambda x: [[val for key, val in flatten(y[col_name]).items() if "plain_text" in key][0] for y in x.properties]})
