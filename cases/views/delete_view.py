from typing import Coroutine
from discord.ui import View, Button, button
from discord import Member, Interaction, ButtonStyle
from database import delete_case


class DeleteView(View):
    def __init__(self, moderator:Member, interaction:Interaction, case_id:int):
        self.case_id = case_id
        self.mod = moderator
        self.interaction = interaction
        self.ended = False
        super().__init__(timeout=30)
    
    @button(label="Confirm Delete", style=ButtonStyle.red)
    async def confirm_delete(self, interaction:Interaction, button:Button):
        if interaction.user != self.mod: return interaction.response.send_message("You cant press this!", ephemeral=True)
        delete_case(interaction.guild_id, f"id = {self.case_id}")
        button.disabled = True

        self.ended = True
        await self.interaction.edit_original_response(view=self)
        await interaction.response.send_message("Case deleted!")
    
    async def on_timeout(self) -> None:
        if self.ended: return
        self.children[0].disabled = True
        await self.interaction.edit_original_response(view=self)
        await self.interaction.channel.send("This interaction has timed out!")