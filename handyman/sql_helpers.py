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
