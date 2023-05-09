import stockx
import discord
import json
import asyncio
from discord.ext import commands

TOKEN = "MTEwNTMwNTg2NTM1NzExNTUwMw.GbE76-.yh0GFkaPP25Oa2Hlp1zO_2nafHYOxwET9t8Evs"

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='/',help_command=None,case_insensitive=True,intents=intents)

#Init Boot
@bot.event
async def on_ready():
  await stockx.init()
  print("Starting up...")

  
#Commands
@bot.command()
async def help(ctx):
    embed = discord.Embed(
      title="Citrine",
      description="Commands for Citrine!",
      color="#E4D00A"
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
    await ctx.send(embed=embed)

#Run Bot
bot.run(TOKEN)