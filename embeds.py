import discord

def create_embed(mapping):
  embed = discord.Embed(
    title=mapping["name"],
    description="--------------------------------",
  )
  embed.add_field(
    name="Margin detected -> " + str(mapping["Margin"]) + "%",
    value="Previous listing -> $"+str(mapping["prevlisting"])+"\n"+"Newest listing -> $"+str(mapping["lowest"]) + "\n" + "Link -> "+ str(mapping["link"]),
    inline=True
  )
  if mapping["src"] != "N/A":
    embed.set_image(
      url=mapping["src"]
    )
  return embed

def create_dash(conf):
  embed = discord.Embed(
    title="At A Glance",
    description="Stockx Margin -> "+str(conf["Smargin"])+"%\n\n Goat Margin -> "+str(conf["Gmargin"])+"%\n\n CURRENTLY TRACKING ->",
  )
  if len(conf["Keywords"]) == 0:
    embed.add_field(
      name="~~~~~~~~~~~~~~",
      value="No keywords tracked yet!",
      inline=True
    )
  else:
    for kw in conf["Keywords"]:
      embed.add_field(
        name="~~~~~~~~~~~~~",
        value=kw,
        inline=False
      )
  return embed