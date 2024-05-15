from discord.ext import commands
from discord import Intents

from database import *
from cases.cases import Cases
from nsfw import Nsfw

import json
import requests


# custom class
class Bot(commands.Bot):


    async def setup_hook(self) -> None:
        await self.add_cog(Cases())
        await self.add_cog(Nsfw(self))




# vars
bot = Bot(command_prefix='?', intents=Intents.all())
settings = json.load(open("settings.json"))
tree = bot.tree

@bot.event
async def on_ready():
    pass
    #chan = bot.get_channel(1184343577053118486)
    #await chan.send("Bot ready!")
    #await chan.send("Case cog ready!")
    #await chan.send("Nsfw cog ready!")

# commands
@bot.command()
async def sync(ctx:commands.Context):
    await tree.sync()
    await ctx.send("Done!")





bot.run(settings['token'])