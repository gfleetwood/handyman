def aws():

  s3_client = boto3.client('s3')
  s3 = boto3.resource('s3')

  s3_client.list_buckets()
  bucket = s3.Bucket(os.environ["S3_BUCKET"])
  objs = bucket.objects.filter(Prefix = '')

  session = boto3.Session(profile_name = '')
  #for bucket in s3.buckets.all(): print(bucket.name)

  for obj in objs:
    s3_client.download_file(
      os.environ["S3_BUCKET"],
      obj.key,
      "/home/USER/Downloads" + obj.key
    )

  files = [obj.key for obj in s3.Bucket(bucket_name).objects.filter(Prefix = '/')]
    
  for file in files:
    s3.Bucket(bucket_name).download_file(file, "/home/" + os.path.split(file)[1])
