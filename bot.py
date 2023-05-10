import stockx
import config
import embeds
import discord
import json
import asyncio
import time
from discord.ext import commands

TOKEN = "MTEwNTMwNTg2NTM1NzExNTUwMw.GbE76-.yh0GFkaPP25Oa2Hlp1zO_2nafHYOxwET9t8Evs"

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='/',help_command=None,case_insensitive=True,intents=intents)

#Init Boot
@bot.event
async def on_ready():
  global channel
  channel = bot.get_channel(1105583257690579014)
  print("channel grabbed!")
  global conf
  conf = config.init()
  print("config grabbed!")
  global sxcol
  sxcol = stockx.init()
  print("Sx db grabbed!")
  global conffile
  conffile = conf.collection.find_one({})
  kwsize = conf.collection.find_one({"Keywords": {"$gt":1}})
  print(kwsize)
  while kwsize != None:
    print("scraping...")
    pducts = await stockx.monitor(sxcol,conffile["Smargin"],conffile["Keywords"])
    if len(pducts) != 0:
      await channel.send(bot.default_role.mention)
      for entry in pducts:
        emb = embeds.create_embed(entry)
        await channel.send(embed=emb)
    time.sleep(15)
  print("Starting up...")


#Commands
@bot.command()
async def setmargin(ctx,*args):
  if len(args) != 2:
    await channel.send("Invalid number of args!")
  else:
    if args[0] == "s":
      conffile.update({"$set":{"Smargin":args[1]}})
      x = conf.count({})
      print(x)
    if args[0] == "g":
      conffile.update({"$set":{"Gmargin":args[1]}})
    await channel.send("Margins set successfully! Restart to see changes...")

@bot.command()
async def addquery(ctx,*args):
  s = " ".join(args[:])
  if s in conffile["Keywords"]:
    await channel.send("Keyword already tracked!")
  else:
    conffile.update({"$push": {"Keywords":s}})
    await channel.send(s + " added to tracking!")
    
@bot.command()
async def removequery(ctx,*args):
  s = " ".join(args[:])
  if s in conffile["Keywords"]:
    l = conffile["Keywords"]
    for ind,x in enumerate(l):
      if x == s:
        l.pop(ind)
      conffile.update({"$set": {"Keywords":l}})
      print("Properly removed keyword!")
    await channel.send("Removed keyword successfully!")
  else:
    await channel.send("Keyword does not exist!")
    
@bot.command()
async def dash(ctx):
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
      value="Removes keyword from monitor"
    )
    embed.add_field(
      name="/SetMargin",
      value="Sets margin of interest based on last sale made\nSet Stockx -> 's %'\nSet Goat -> 'g %'",
      inline=True
    )
    await channel.send(embed=embed)

#Run Bot
bot.run(TOKEN)