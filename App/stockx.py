import aiohttp
import asyncio
import dbapi
from bs4 import BeautifulSoup

#Uses Aiohttp to scrape Stockx asynchronously

#Neccessary for posting via Aiohttp
stockxurl = "https://stockx.com/search/recent-asks?s="
prefixurl = "https://stockx.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
 
#Loads the database object into Stockx
def init():
  global Stockx
  Stockx = dbapi.collectionobject("Stockx")
  return Stockx

#Aiohttp 
async def Grab(sess,fullurl):
  async with sess.get(fullurl,headers=headers) as response:
    return await response.text()
  
async def monitor(col,margin,kw):
  async with aiohttp.ClientSession() as session:
    #kw queries
    for k in kw:
      urlq = k.replace(" ","+")
      page = await Grab(session,stockxurl+urlq)
      soup = BeautifulSoup(page,'html.parser')
      # all product divs
      productlist = soup.find_all('div',{'class' : "css-pnc6ci"})
      retval = []
      
      #processing each product
      def getInfo(product,col,returnval):
        #linkdiv 
        linkdiv = product.a
        link = prefixurl+linkdiv["href"]
        #namediv
        namelist = product.find_all("p", {"class": "chakra-text css-3lpefb"})
        name = namelist[0].contents[0]
        #imagediv
        image = linkdiv.div.div.div.img["src"]
        newlowestlist = product.find_all("p", {"class": "chakra-text css-nsvdd9"})
        newlowest = int(newlowestlist[0].contents[0][1:].strip().replace(',',''))
        #if nonexist, add to db/identify with kw used to find
        if col.countstockx({"name": name}) == 0:
          post = {
            "name": name,
            "lowest": newlowest,
            "link": link,
            "img": image,
            "kw" : k
                  }
          col.insertstockx(post)
          print("Successfully stored "+name+"!")
        #If exists, compare and swap
        elif col.countstockx({"name": name}) != 0:
          fetched = col.findstockx({"name": name})
          oldlowest = fetched["lowest"]
          src = fetched["img"]
          link = fetched["link"]
          percentage = (100-int(margin.strip().replace("'","")))/100
          #If sale encountered, append to list
          if ((newlowest)/(oldlowest)) <= percentage:
            post = {
              "name":name,
              "lowest":newlowest,
              "prevlisting":oldlowest,
              "src":src,
              "link":link,
              "Margin": (100 - float(newlowest)/float(oldlowest))
              }
            returnval.append(post)
          col.updatestockx({"name":name},{"$set":{"lowest":newlowest}})
          
      Futures = [asyncio.ensure_future(getInfo(item,col,retval) for item in productlist)]
      await asyncio.gather(*Futures)
      return retval
      
 
