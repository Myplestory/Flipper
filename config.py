import asyncio
import dbapi

def init():
  global config
  config = dbapi.collectionobject("Config")
  if config.count({}) == 0:
    config.insert({"Smargin": 20,"Gmargin": 20,"Keywords":[]})
    print("created default config!")
  else:
    print("config found!")
  return config