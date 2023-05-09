import discord

def create_embed(mapping):
  embed = discord.Embed(
    title=mapping["name"],
    description="~~~~~~~~~~~~~~~~~~~~~~",
  )
  embed.add_field(
    name="Margin detected -> " + mapping["Margin"],
    value="Previous listing -> "+mapping["prevlisting"]+"\n"+"Newest listing -> "+mapping["lowest"],
    inline=True
  )
  return embed

def create_dash(conf):
  embed = discord.Embed(
    title="At A Glance",
    description="Stockx Margin -> "+conf["Smargin"]+"\n Goat Margin -> "+conf["Gmargin"]+"\n CURRENTLY TRACKING...",
  )
  for kw in conf["Keywords"]:
    embed.add_field(
      name="~~~~~~~~~~~~~",
      value=kw,
      inline=False
    )
    return embed