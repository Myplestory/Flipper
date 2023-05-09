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
  conffile = conf.collection.find_one({})
  kwsize = conf.collection.find_one({"Keywords": {"$gt":1}})
  print(kwsize)
  while kwsize != None:
    pducts = await stockx.monitor(sxcol,conffile["Smargin"],conffile["Keywords"])
    if pducts.len != 0:
      await channel.send(bot.default_role.mention)
      for entry in pducts:
        emb = embeds.create_embed(entry)
        await channel.send(embed=emb)
    time.sleep(300)
  print("Starting up...")

  
#Commands
@bot.command()
async def addquery(ctx,*args):
  s = " ".join(args[:])
  if s in conf["Keywords"]:
    await channel.send("Keyword already tracked!")
  else:
    conf.update({"Smargin"},{"$push": {"Keywords":s}})
    await channel.send(s + " added to tracking!")
  
@bot.command()
async def dash(ctx):
  emb = embeds.create_dash(conf)
  await channel.send(embed=emb)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
      title="Citrine",
      description="Commands for Citrine!",
      color=16244057
    )
    embed.add_field(
      name="!Help",
      value="List of Citrine Commands",
      inline=True
    )
    embed.add_field(
      name="!Dash",
      value="Aggregated configs",
      inline=True
    )
    embed.add_field(
      name="!AddQuery",
      value="Adds specific keyword to monitor",
      inline=True
    )
    embed.add_field(
      name="!RemoveQuery",
      value="Removes keyword from monitor"
    )
    embed.add_field(
      name="!SetMargin",
      value="Sets margin of interest based on last sale made",
      inline=True
    )
    await channel.send(embed=embed)

#Run Bot
bot.run(TOKEN)