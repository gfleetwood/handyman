from os import system

def delete_tweets(num_tweets):

    auth = tweepy.OAuthHandler("CLIENT-ID", "CLIENT-SECRET")
    auth.set_access_token("ACCESS_ID", "ACCESS_SECRET")
    api = tweepy.API(auth)

    for i in range(num_tweets):
        for tweet in api.user_timeline(): 
            tweet.destroy()
            
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

