def dbx_get_files(folder):

    #_ = dbx.files_list_folder()
    files = [
       dbx.files_download(entry.path_lower)
       for entry in folder.entries
       if (isinstance(entry, dropbox.files.FileMetadata))
    ]

    return(files)

def get_dbx_con():
    
    result = dropbox.Dropbox(os.environ['DBox'])

    return(result) 

def dbx_move_file():

  dbx.files_move(
    img_metadata.path_display,
    img_metadata.path_display.replace("0_raw", "3_processed")
  )
  
  return(True)

def access_dbx_file():
  
  img_metadata = files_new_info[0]
  img_bytes = img_new_info[1].content
  img_pil = Image.open(BytesIO(img_to_process_bytes))
  img_np = np.asanyarray(img_to_process_pil)

  return(img_np)

def convert_img_np_to_bytes(img_np):
    
    # Work around for limitations of PIL library:
    # https://stackoverflow.com/a/47292141
    img_pil = Image.fromarray((img_np * 255).astype(np.uint8), mode = 'L')
    img_bytes = io2.BytesIO()
    #img_pil = img_pil.convert("") 
    img_pil.save(img_bytes, format = 'JPEG')
    img_bytes = img_bytes.getvalue()
    
    return(img_bytes)

def save_image(img, fname, dbx):
    
    img_bytes = convert_img_np_to_bytes(img)
    dbx.files_upload(img_bytes, fname)

    return(True)s


