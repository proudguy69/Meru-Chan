from discord.ui import View, Button, button
from discord import ButtonStyle, Interaction

from embeds.modals.add_field import AddField
from embeds.modals.edit_basic import EditInfo



class EmbedEditView(View):
    def __init__(self):
        super().__init__()

    @button(label="Edit info", style=ButtonStyle.red)
    async def edit_info(self, interaction:Interaction, button:Button):
        await interaction.response.send_modal(EditInfo(interaction))

    @button(label="Add Field", style=ButtonStyle.red)
    async def add_field(self, interaction:Interaction, button:Button):
        await interaction.response.send_modal(AddField(interaction))

    