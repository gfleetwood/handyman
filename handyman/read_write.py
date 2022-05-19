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
  
from subprocess import Popen, PIPE
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
import urllib
import numpy as np
import psycopg2

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
