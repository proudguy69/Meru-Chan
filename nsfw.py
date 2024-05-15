from discord.ext.commands import Cog
from discord.ext import tasks
from discord import app_commands, Interaction

import requests
import json
import random


settings = json.load(open("settings.json"))
headers = {'authorization': settings['fluxpoint']}
data = requests.get("https://api.fluxpoint.dev/swagger/v1/swagger.json").json()
endpoints:list = data['paths']['/nsfw/img/{imageType}']['get']['parameters'][0]['schema']['enum']
endpoints_gif:list = data['paths']['/nsfw/gif/{imageType}']['get']['parameters'][0]['schema']['enum']

endpoints_1 = []
endpoints_2 = []
for i, endpoint in enumerate(endpoints):
    if i < 24:
        endpoints_1.append(app_commands.Choice(name=endpoint, value=endpoint))
    if i > 24:
        endpoints_2.append(app_commands.Choice(name=endpoint, value=endpoint))


endpoints_gif = [app_commands.Choice(name=endpoint, value=endpoint) for endpoint in endpoints_gif]


r = requests.get(f'https://api.fluxpoint.dev/nsfw/img/{endpoints[random.randint(0, len(endpoints))]}', headers=headers).json()
print(r)
class Nsfw(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.send_image.start()
        super().__init__()
        

    nsfw = app_commands.Group(name="nsfw", description="A collection of NSFW commands", nsfw=True)
    

    @nsfw.command(name="image_1", description="Sends an nsfw image with the given peram")
    @app_commands.choices(imagetype=endpoints_1)
    async def img1(self, interaction:Interaction, imagetype:app_commands.Choice[str]):
        response = requests.get(f'https://api.fluxpoint.dev/nsfw/img/{imagetype.value}', headers=headers).json()
        await interaction.response.send_message(response['file'])
    
    @nsfw.command(name="image_2", description="Sends an nsfw image with the given peram")
    @app_commands.choices(imagetype=endpoints_2)
    async def img2(self, interaction:Interaction, imagetype:app_commands.Choice[str]):
        response = requests.get(f'https://api.fluxpoint.dev/nsfw/img/{imagetype.value}', headers=headers).json()
        await interaction.response.send_message(response['file'])

    @nsfw.command(name="gif", description="Sends an nsfw gif with the given peram")
    @app_commands.choices(imagetype=endpoints_gif)
    async def gif(self, interaction:Interaction, imagetype:app_commands.Choice[str]):
        response = requests.get(f'https://api.fluxpoint.dev/nsfw/gif/{imagetype.value}', headers=headers).json()
        await interaction.response.send_message(response['file'])

    @tasks.loop(seconds=2.5)
    async def send_image(self):
        try:
            guild = self.bot.get_guild(1184343577053118486)
            channel = guild.get_channel(1240085335590047826)
            r = requests.get(f'https://api.fluxpoint.dev/nsfw/img/{endpoints[random.randint(0, len(endpoints))]}', headers=headers).json()
            await channel.send(r['file'])
        except: pass
        #await channel.send('test')


    