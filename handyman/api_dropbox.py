def get_dbx_con():
    
    dbx_con = dropbox.Dropbox(os.environ['DBox'])

    return(dbx_con) 

def get_dbx_files(folder: str):

    #_ = dbx.files_list_folder()
    files = [
       dbx.files_download(entry.path_lower)
       for entry in folder.entries
       if (isinstance(entry, dropbox.files.FileMetadata))
    ]

    return(files)

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

