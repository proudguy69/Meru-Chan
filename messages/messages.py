from email import message
from discord.ext.commands import Cog
from discord import app_commands, TextChannel, Interaction

from database import *


class Messages(Cog):
    def __init__(self) -> None:
        print("Messages cog online!")
        super().__init__()
    
    message = app_commands.Group(name="message", description="a group of message related commands")




    @app_commands.command(name="messages", description="gets all the pre-made messages, or one if id is specified")
    async def messages(self, interaction:Interaction):
        data = get_messages(interaction.guild.id)
        embeds = []
        for message in data:
            channel_id = message[2]
            channel = interaction.guild.get_channel(channel_id).mention if channel_id else None
            content = message[3]
            embeds.append(Embed(title=f"Message {message[0]}", description=f"Content: `{content}`\nChannel: {channel}\nMessage Type: {message[4]}", color=0xffa1dc))
        if len(embeds) == 0: return await interaction.response.send_message("Your server has no messages created! consider using /message create")
        await interaction.response.send_message(embeds=embeds)


    @message.command(name="create", description="edits a message you have created with its given id")
    async def message_create(self, interaction:Interaction, content:str=None, channel:TextChannel=None, message_type:str=None):
        cid = channel.id if channel else None
        mention = channel.mention if channel else None
        data = create_message(interaction.guild_id, cid, content, message_type)
        embed = Embed(title="New message", description=f"Content: `{content}`\nChannel: {mention}\nMessage Type: {message_type}", color=0xffa1dc)
        embed.set_footer(text=f"You can preview this message with /preview {data[0]} and add an embed with /embed create {data[0]}")
        await interaction.response.send_message(embeds=[embed])

    
    
    @message.command(name="preview", description="previews pre made messages")
    async def message_preview(self, interaction:Interaction, id:int):
        data = get_messages(interaction.guild_id, f"id = {id}")[0]
        channel_id = data[2]
        channel = interaction.guild.get_channel(channel_id) if channel_id else None
        content = data[3]
        if not content: return await interaction.response.send_message("the message has no content so it cant be sent!", ephemeral=True)
        if channel:
            await channel.send(content = content)
            return await interaction.response.send_message(f"You have a channel set for this message! so it was sent in {channel.mention}", ephemeral=True)
        else:
            await interaction.channel.send(content)
            await interaction.response.send_message(f"The message was sent sent!", ephemeral=True)

    @message.command(name="edit", description="edits a message you have created with its given id")
    async def message_edit(self, interaction:Interaction, id:int, content:str=None, channel:TextChannel=None, message_type:str=None):
        # * Before Message
        data = get_messages(interaction.guild_id, f"id = {id}")[0]
        mention = interaction.guild.get_channel(data[2]).mention if data[2] else None
        before = Embed(title="Old Message", description=f"Content: `{data[3]}`\nChannel: {mention}\nMessage Type: {data[4]}", color=0xffa1dc)
        # * After message
        mention_2 = channel.mention if channel else None
        channel = "NULL" if not channel else channel
        edit_message(interaction.guild_id, set=f"content = '{content}', channel = {channel}, message_type = '{message_type}'", condition=f"id = {id}")
        after = Embed(title="New message", description=f"Content: `{content}`\nChannel: {mention_2}\nMessage Type: {message_type}", color=0xffa1dc)
        after.set_footer(text=f"You can preview this message with /preview {data[0]} and add an embed with /embed create {data[0]}")
        await interaction.response.send_message(embeds=[before, after])