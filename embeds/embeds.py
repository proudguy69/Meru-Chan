from email import message
from discord.ext.commands import Cog
from discord import app_commands, TextChannel, Interaction

from database import *
from embeds.views.embed_view import EmbedEditView


class Embeds(Cog):
    def __init__(self) -> None:
        print("Embeds cog online!")
        super().__init__()

    embed = app_commands.Group(name="embeds", description="a group of embed related commands")

    @embed.command(name="create", description="creates an embed")
    async def embed_create(self, interaction:Interaction):
        embed = Embed(title="​", description="")
        await interaction.response.send_message(content="Interact with the buttons below to edit the button", embed=embed, view=EmbedEditView())

