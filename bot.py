from discord.ext import commands
from discord import Intents

from database import *
from cases.cases import Cases

import json



# custom class
class Bot(commands.Bot):


    async def setup_hook(self) -> None:
        print("Bot is online!")
        await self.add_cog(Cases())


# vars
bot = Bot(command_prefix='?', intents=Intents.all())
settings = json.load(open("settings.json"))
tree = bot.tree


# commands
@bot.command()
async def sync(ctx:commands.Context):
    await tree.sync()
    await ctx.send("Done!")





bot.run(settings['token'])