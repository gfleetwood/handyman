personal_access_token = os.environ.get("ASANA_PAT")
client = asana.Client.access_token(personal_access_token)
asana_uids = list(client.users.get_users(workspace = os.environ.get("ASANA_WORKSPACE_ID")))

# #client.projects.find_by_id("0000").items()
