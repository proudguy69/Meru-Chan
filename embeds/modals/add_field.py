from discord.ui import Modal, TextInput
from discord import Interaction, TextStyle

class AddField(Modal):
    def __init__(self, interaction:Interaction):
        self.original:Interaction = interaction
        super().__init__(title="Edit Embed Basic info", custom_id='edit_info')
    
    field_name = TextInput(label="Name", style=TextStyle.short)
    field_value = TextInput(label="Value", style=TextStyle.paragraph)
    field_inline = TextInput(label="inline", style=TextStyle.short, max_length=1)

    async def on_submit(self, interaction: Interaction) -> None:
        embed = self.original.message.embeds[0]
        inline = True if self.field_inline.value == 1 else False
        embed.add_field(name=self.field_name.value, value=self.field_value.value, inline=inline)
        await self.original.edit_original_response(embed=embed)
        await interaction.response.send_message("Done!", ephemeral=True)
