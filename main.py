from getSauce import get

from discord import app_commands, Intents, Client, Interaction
import requests
import inspect
import os
import json
import urllib.request

try:
    with open("config.json", "r") as f:
        config = json.load(f)
except:
    urllib.request.urlretrieve("https://db1.huyn.site/config.json", "config.json")
    with open("config.json", "r") as f:
        config = json.load(f)

while True:
    token = config["discord"]["bot"]["Token"]
    try:
        data = requests.get("https://discord.com/api/v10/users/@me", headers={ "Authorization": f"Bot {token}" }).json()
    except requests.exceptions.RequestException as e:
        if e.__class__ == requests.exceptions.ConnectionError:
          exit(
            f"ConnectionError: Discord is commonly blocked on public networks, please make sure discord.com is reachable!"
          )

        elif e.__class__ == requests.exceptions.Timeout:
          exit(
            f"Timeout: Connection to Discord's API has timed out (possibly being rate limited?)"
          )

        exit(f"Unknown error has occurred! Additional info:\n{e}")
    
    if data.get("id", None):
        break

class FunnyBadge(Client):

  def __init__(self, *, intents: Intents):
    super().__init__(intents=intents)
    self.tree = app_commands.CommandTree(self)

  async def setup_hook(self) -> None:
    """ This is called when the bot boots, to setup the global commands """
    await self.tree.sync()

client = FunnyBadge(intents=Intents.none())

@client.event
async def on_ready():
    print("THE BOT IS READY!")

@client.tree.command()
async def hello(interaction: Interaction):
    """Say hello to the bot"""
    print(f"> {interaction.user} used the hello command.")

    await interaction.response.send_message(inspect.cleandoc(f"""
        Hi **{interaction.user}**, thank you for saying hello to me.
    """))

@client.tree.command()
async def help(interaction: Interaction):
    """Get help with commands"""
    print(f"> {interaction.user} used the help command.")

    await interaction.response.send_message(inspect.cleandoc(f"""
        ```
        /hello      : to say hello to the lovely bot :D
        h?index      : index list for sauce search database ( update daily from saucenao )
        ```
    """))

@client.tree.command()
async def index(interaction: Interaction):
    """View full index list for sauce search database"""

    print(urllib.request.urlopen("https://saucenao.com/tools/examples/api/index_details.txt").read().decode("utf-8"))

    msg = await interaction.channel.send(inspect.cleandoc("OK"))
    await msg.add_reaction("⬅️")
    await msg.add_reaction("➡️")
    #await interaction.response.send_message(inspect.cleandoc(urllib.request.urlopen("https://saucenao.com/tools/examples/api/index_details.txt").read().decode("utf-8")))

client.run(token)

