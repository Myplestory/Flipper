import pymongo

#db constructor
class collectionobject:
  def __init__(self):
    dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
    collectionobject = dbclient["Citrinev4"]
    self.stockx = collectionobject["Stockx"]
    self.goat = collectionobject["Goat"]
    self.config = collectionobject["Config"]
  # default configure
  def configure(self,query):
    self.insertconfig(query)
  # counts
  def countstockx(self,query):
      return self.stockx.count_documents(query)
  def countgoat(self,query):
      return self.goat.count_documents(query)
  def countconfig(self,query):
      return self.config.count_documents(query)
  # finds
  def findstockx(self,query):
      return self.stockx.find(query)
  def findgoat(self,query):
      return self.goat.find(query)
  def findconfig(self,query):
      return self.config.find_one(query)
  # config
  def insertstockx(self,query):
      self.stockx.insert_one(query)
  def insertgoat(self,query):
      self.goat.insert_one(query)
  def insertconfig(self,query):
      self.config.insert_one(query)
  # Remove
  def removestockx(self,query):
    self.stockx.delete_one(query)
  def removegoat(self,query):
    self.goat.delete_one(query)
  def removeconfig(self,query):
    self.config.delete_one(query)
  # updates
  def updatestockx(self,key,query):
      self.stockx.find_one_and_update(key,query, upsert = False)
  def updategoat(self,key,query):
      self.goat.find_one_and_update(key,query, upsert = False)
  def updateconfig(self,key,query):
      self.config.find_one_and_update(key,query)
    