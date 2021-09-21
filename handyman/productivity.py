from os import system

def compress_pdf(input_path, output_path):

  template = "gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dBATCH  -dQUIET -sOutputFile={} {}"
  system(template.format(output_path, input_path))

  return(1)

def password_generator():

  template = 'echo $(grep "^[^\']\{3,5\}$" /usr/share/dict/words|shuf -n 4)'
  system(template)

  return(1)

def gpg_encrypt(file_path): 

  system("gpg -c {}".format(file_path))

  return(1)

def gpg_decrypt(file_path): 

  system("gpg -d {}".format(file_path))

  return(1)

def delete_tweets(num_tweets):

    auth = tweepy.OAuthHandler("CLIENT-ID", "CLIENT-SECRET")
    auth.set_access_token("ACCESS_ID", "ACCESS_SECRET")
    api = tweepy.API(auth)

    for i in range(num_tweets):
        for tweet in api.user_timeline(): 
            tweet.destroy()
            
    return(True)

def extract_audio_from_video(video_path):

  import os
  template = "ffmpeg -i {} -q:a 0 -map a output.mp3"
  cmd = template.format(video_path)
  os.system(cmd)

  return(True)

def md_tbl_to_csv(md_tbl: str) -> pd.DataFrame:
    
    remove_empty_strs = lambda row: [val.strip() for val in row if val != ""]
    
    rows_as_list = [
        remove_empty_strs(line.split("|"))
        for line in md_tbl.split("\n") 
        if "--" not in line
    ]
    
    result = pd.DataFrame(rows_as_list)
    result.columns = result.iloc[0]
    result = result[1:]
    
    return(result)

