import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import dbapi
from bs4 import BeautifulSoup

# Selenium is used because Goat uses infinite scroll. By using chrome webdriver, we can simulate scrolling to get the full html before parsing.

#Neccessary for posting via selenium
goaturl = "https://www.goat.com/search?query="
prefixurl = "https://www.goat.com"
headers = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'

#Loads the database object into Goat
def __init__():
  global Goat
  Goat = dbapi.collectionobject("Goat")
  return Goat



async def monitor(col,margin,kw):
    #kw queries
    for k in kw:
      urlq = k.replace(" ","+")
      
      # Using Selenium to scroll to end of queried page
      
      #Initialize options (No window, post w headers)
      options = Options()
      options.add_argument('user-agent={0}'.format(headers))
      options.add_argument("--headless")
      driver = webdriver.Chrome('/tmp/chromedriver',options=options)
      #Post to build URL
      driver.get(goaturl+urlq)
      #Simulate scrolling
      last_height = driver.execute_script("return document.body.scrollHeight")
      while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(0.35)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height==last_height:
          break
        else:
          last_height = new_height
      await asyncio.sleep(1)
      #Grabbing full HTML
      page = driver.page_source
      soup = BeautifulSoup(page,'html.parser')
      productlist = soup.find_all('div',{'class' : "GridStyles__GridCellWrapper-sc-1cm482p-0 biZBPm"})
      retval = []
      
      #Method to process each product
      def getInfo(product,col,returnval):
        #linkdiv 
        linkdiv = product.a
        link = prefixurl+linkdiv["href"]
        #namediv
        namelist = product.find_all("div", {"class": "GridCellProductInfo__Name-sc-17lfnu8-3 hfCoWX"})
        name = namelist[0].contents[0]
        #imagediv
        image = product.find_all("img", {"class": "sc-eDvSVe fRZbbQ Image__StyledImage-sc-1qwz99p-0 cURopN GridCellProductImage__Image-sc-msqmrc-1 kjpMyF"})
        if len(image) == 0:
          image = "N/A"
        elif len(image) != 0:
          image = image[0]["src"]
        newlowestlist = product.find_all("div", {"class": "GridCellProductInfo__Price-sc-17lfnu8-6 gsZMPb"})[0].contents[0].contents[0]
        newlowest = int(newlowestlist.strip().replace('$','').replace(',',''))
        #If nonexist, add to db/identify with kw used to find
        if col.countgoat({"name": name}) == 0:
          post = {
            "name": name,
            "lowest": newlowest,
            "link": link,
            "img": image,
            "kw" : k
                  }
          col.insertgoat(post)
        #If exists, compare and swap
        elif col.countgoat({"name": name}) != 0:
          fetched = col.findgoat({"name": name})
          oldlowest = fetched["lowest"]
          src = fetched["img"]
          link = fetched["link"]
          percentage = (100-int(margin))/100
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
          col.updategoat({"name":name},{"$set":{"lowest":newlowest}})
          
      Futures = [asyncio.ensure_future(getInfo(item,col,retval) for item in productlist)]
      await asyncio.gather(*Futures)
      return retval