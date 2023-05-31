import stockx
import goat
import embeds
import discord
import asyncio
import dbapi
from discord.ext import commands

#Discord token
TOKEN = ""

#Setting Intents
intents = discord.Intents.default()
intents.messages = True
 
#Set bot command prefix ->
bot = commands.Bot(command_prefix='',help_command=None,case_insensitive=True,intents=intents)

#Init Boot 
@bot.event
async def on_ready():
  global channel
  channel = bot.get_channel() # Channel ID for user bot interaction
  postedchannels = bot.get_channel() # Channel ID to post Stockx finds
  postedchannelg = bot.get_channel() # Channel ID to post Goat finds
  #First, we initialize the database object
  global colobj
  colobj = dbapi.collectionobject()
  #Once initialized, we can start configuring the config document/initialize it
  if colobj.countconfig({}) == 0:
    colobj.insertconfig({"Smargin": 20,"Gmargin": 20,"Keywords":[]})
  print("Configs found ... " + str(colobj.findconfig({})))
  #Once configured, we can begin the main loop
  while True:
    kwsize = colobj.findconfig({})
    kwsize = len(kwsize["Keywords"])
    conf = colobj.findconfig({})
    #If keywords found, monitor
    if kwsize != 0:
      margin = conf["Smargin"]
      margin2 = conf["Gmargin"]
      kw = colobj.findconfig({})["Keywords"]
      pducts1 = await stockx.monitor(colobj,margin,kw)
      pducts2 = await goat.monitor(colobj,margin2,kw)
      #Posting Stockx finds
      if len(pducts1) != 0:
       await postedchannels.send(content="@here")
       for entry in pducts1:
         emb = embeds.create_embed(entry)
         await postedchannels.send(embed=emb)
      #Posting Goat finds
      if len(pducts2) != 0:
        await postedchannelg.send(content="@here")
        for entry in pducts2:
          emb = embeds.create_embed(entry)
          await postedchannelg.send(embed=emb)
      await asyncio.sleep(60)
    await asyncio.sleep(60)
    
    
    
  


#Commands
@bot.command()
async def setmargin(ctx,*args):
  if len(args) != 2:
    await channel.send("Invalid number of args!")
  else:
    if args[0] == "s":
      colobj.updateconfig({},{"$set":{"Smargin":args[1]}})
    if args[0] == "g":
      colobj.updateconfig({},{"$set":{"Gmargin":args[1]}})
    await channel.send("Margins set successfully!")

@bot.command()
async def addquery(ctx,*args):
  s = " ".join(args[:])
  conffile = colobj.findconfig({})
  if s in conffile["Keywords"]:
    await channel.send("Keyword already tracked!")
  else:
    colobj.updateconfig({},{"$push": {"Keywords":s}})
    await channel.send(s + " added to tracking!")
    
@bot.command()
async def removequery(ctx,*args):
  s = " ".join(args[:])
  conffile = colobj.findconfig({})
  if s in conffile["Keywords"]:
    l = conffile["Keywords"]
    for ind,x in enumerate(l):
      if x == s:
        l.pop(ind)
        colobj.purgestockx({"kw":s})
        colobj.purgegoat({"kw":s})
      colobj.updateconfig({},{"$set": {"Keywords":l}})
    await channel.send("Removed keyword successfully!")
  else:
    await channel.send("Keyword does not exist!")
    
@bot.command()
async def dash(ctx):
  conffile = colobj.findconfig({})
  mapping = {
    "Smargin":conffile["Smargin"],
    "Gmargin":conffile["Gmargin"],
    "Keywords":conffile["Keywords"]
  }
  emb = embeds.create_dash(mapping)
  await channel.send(embed=emb)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
      title="Citrine",
      description="Commands for Citrine!",
      color=16244057
    )
    embed.add_field(
      name="/Help",
      value="List of Citrine Commands",
      inline=True
    )
    embed.add_field(
      name="/Dash",
      value="Aggregated configs",
      inline=True
    )
    embed.add_field(
      name="/AddQuery",
      value="Adds specific keyword to monitor",
      inline=True
    )
    embed.add_field(
      name="/RemoveQuery",
      value="Removes keyword from monitor, and purges products from database"
    )
    embed.add_field(
      name="/SetMargin",
      value="Sets margin of sale based on last sale made\nSet Stockx -> 's %'\nSet Goat -> 'g %'",
      inline=True
    )
    await channel.send(embed=embed)

#Run Bot
if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(bot.run(TOKEN))