from subprocess import Popen, PIPE
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
import urllib
import numpy as np
import psycopg2

def get_file_paths(path):
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


def read_images(path):
  
    img_paths = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(path)
        for f in filenames
        if os.path.splitext(f)[1] == '.jpg'
    ]

    imgs_info = [(imread(img_path), img_path) for img_path in img_paths]

    return(imgs_info)

def read_files_in_dir():

  files = [
  "{}/{}".format(path.abspath("done"), file)
  for file in dir_list
  if ".sql" in file
  ]

  return(files)

def read_db_data_thru_tunnel(qry):

  cmd = [
    "ssh", 
    "-i",
    "C:", 
    "-N",
    "-L", 
    "localhost",
    "ec2"    
  ]

  p = Popen(cmd, stdout = PIPE, shell = False)
  con_str = "postgresql+psycopg2://UN:PW@localhost:5432/DB"
  eng = create_engine(con_str)
  df = pd.read_sql(qry, eng)
  p.kill()
  
  return(df)

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
