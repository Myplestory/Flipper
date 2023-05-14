import aiohttp
import asyncio
import json
import dbapi
from bs4 import BeautifulSoup

stockxurl = "https://stockx.com/search/recent-asks?s="

def init():
  global Stockx
  Stockx = dbapi.collectionobject("Stockx")
  print("Stockx collection loaded! "+ str(Stockx.count({})) +" Items in Stockx")
  return Stockx
  
async def monitor(col,margin,kw):
  async with aiohttp.ClientSession() as session:
    #kw queries
    for k in kw:
      urlq = k.replace(" ","+")
      page = await Grab(session,stockxurl+urlq)
      print("Page grabbed!")
      soup = BeautifulSoup(page,'html.parser')
      print("Soup created!")
      productlist = soup.find_all('div',{'class' : "css-cp13gg"})
      retval = []
      #processing each product
      def getInfo(product,col,returnval):
        name = product.find("p", {"class": "chakra-text css-3lpefb"})
        newlowest = product.find("p", {"class": "chakra-text css-nsvdd9"})
        #if nonexist, add to db/identify with kw used to find
        if col.count({"name": name},"stockx") == 0:
          post = {
            "name": name,
            "lowest": newlowest,
            "kw" : k
                  }
          col.insert(post)
          print("Successfully stored "+name+"!")
        #if exists
        elif col.count({"name": name},"stockx") != 0:
          fetched = col.stockx.find({"name": name})
          if (newlowest/fetched["lowest"]) <= 100-margin:
            post = {
              "name":name,
              "lowest":newlowest,
              "prevlisting":fetched["lowest"], "Margin":newlowest/fetched["lowest"]
              }
            returnval.append(post)
          col.update({"name":name},{"lowest":newlowest})
      Futures = [asyncio.ensure_future(getInfo(item,col,retval) for item in productlist)]
      print("Gathering futures...")
      await asyncio.gather(*Futures)
      return retval
      
 
async def Grab(sess,fullurl):
  async with sess.get(fullurl) as response:
    return await response.text()