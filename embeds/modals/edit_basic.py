from discord.ui import Modal, TextInput
from discord import Interaction, TextStyle

class EditInfo(Modal):
    def __init__(self, interaction:Interaction):
        self.original:Interaction = interaction
        super().__init__(title="Edit Embed Basic info", custom_id='edit_info')
    
    embed_title = TextInput(label="Title", style=TextStyle.short, custom_id='title')
    embed_description = TextInput(label="Description", style=TextStyle.paragraph)
    embed_color = TextInput(label="Color", style=TextStyle.short, max_length=6)

    async def on_submit(self, interaction: Interaction) -> None:
        embed = self.original.message.embeds[0]
        embed.title = self.embed_title.value.format(user=interaction.user)
        embed.description = self.embed_description.value.format(user=interaction.user)
        embed.color = int(self.embed_color.value,base=16)
        await self.original.edit_original_response(embed=embed)
        await interaction.response.send_message("Done!", ephemeral=True)
