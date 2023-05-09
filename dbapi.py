import pymongo

#db constructor
class collectionobject:
  def __init__(self,collectionname):
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    collectionobject = dbclient["Citrine"]
    self.collection = collectionobject[collectionname]
  def count(self,query):
    return self.collection.count_documents(query)
  def find(self,query):
    self.collection.find(query)
  def insert(self,query):
    if self.count(query) == 0:
      self.collection.insert_one(query)
  def remove(self,query):
    if self.count(query) != 0:
      self.collection.delete_one(query)
  def update(self,key,query):
    self.collection.update_one(key,query, upsert = False)