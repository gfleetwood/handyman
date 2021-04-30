client = MongoClient(os.environ.get("MONGODB_CONNECTION_STRING"))
db = client["opentrons"]

# db.drop_collection
# collection.remove
# collection.drop

for collection in ["r", "st", "w", "op"]:
    db[collection].remove()

# Mongo

# https://docs.mongodb.com/manual/reference/sql-comparison/
# https://realpython.com/introduction-to-mongodb-and-python/

# mongoengine is a higher level of abstraction on top of pymongo (syntactic sugar)

# database ~ database
# table ~ collection
# row ~ document or BSON document
# column ~ field
# index	~ index
# table joins ~ $lookup, embedded documents
# primary key ~ primary key

for db in client.list_databases():
    print(db)
    
db = client["op"]

for col in db.list_collection_names(): 
    print(col)
    
for x in db["opt"].find(): 
    print(x.keys())
    
for x in db["b"].find(): 
    print(x.keys())

pd.DataFrame(list(db["tbl"].find()))
