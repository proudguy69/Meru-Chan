from discord.ext.commands import Cog
from discord import Embed, app_commands, Interaction, Member

from cases.views.delete_view import DeleteView

from database import *

class Cases(Cog):
    def __init__(self) -> None:
        super().__init__()

    case = app_commands.Group(name="case", description="Case commands for case modifcation")

    # stand alone commands
    @app_commands.command(name="cases", description="gets cases of a given the user")
    @app_commands.describe(
        user = "The user you want to fetch cases from",
    )
    @app_commands.default_permissions(manage_messages=True)
    async def cases(self, interaction:Interaction, user:Member=None, case_id:int=None):
        if not user and not case_id: return await interaction.response.send_message("You must provide a user or a case id!!")
        if user and case_id:
            cases = get_cases(interaction.guild.id, f"user_id = {user.id}")
        elif case_id and not user:
            cases = get_cases(interaction.guild.id, f"id = {case_id}")
        else:
            cases = get_cases(interaction.guild.id, f"user_id = {user.id}")

        embeds = []
        for case in cases:
            embed = make_embed(case, interaction)
            embeds.append(embed)
        if len(embeds) == 0:
            return await interaction.response.send_message("no cases found!")
        await interaction.response.send_message(embeds=embeds)



    case = app_commands.Group(name="case", description="Case commands for case modifcation")

    @case.command(name="create", description="command to create a case")
    @app_commands.describe(
        user = "The user you want to create a case against",
        reason = "The reason for the case creation",
        type = "the type of case, ban/kick/warn/custom",
    )
    @app_commands.default_permissions(manage_messages=True)
    async def case_create(self, interaction:Interaction, user:Member=None, reason:str="", type:str=""):
        if user: user_id = user.id; mention= user.mention
        else: user_id = 0; mention = None
        case_id = create_case(interaction.guild_id, interaction.user.id, user_id, type, reason)[0]
        embed = Embed(title=f"New {type} Case | #{case_id}", description=f"Moderator: {interaction.user.mention}\nUser: {mention}\n Reason: {reason}", color=0xff0000)
        await interaction.response.send_message(embed=embed)


    @case.command(name="edit", description="command to create a case")
    @app_commands.describe(
        case_id = "the id of the case you want to edit",
    )
    @app_commands.default_permissions(manage_messages=True)
    async def case_edit(self, interaction:Interaction, case_id:int, user:Member=None, reason:str=None):
        # get the case
        case = get_cases(interaction.guild_id, f"id = {case_id}")[0]
        embed_1:Embed = make_embed(case, interaction)
        embed_1.title = f"Before: Case {case[4]}"
        if not user: user = interaction.guild.get_member(case[3])
        if not reason: reason = case[5]
        edit_case(interaction.guild_id, f"user_id = {user.id}, reason = '{reason}'", f"id = {case_id}")
        case2 = get_cases(interaction.guild_id, f"id = {case_id}")[0]
        embed_2:Embed = make_embed(case2, interaction)
        embed_2.title = f"After: Case {case[4]}"
        await interaction.response.send_message(embeds=[embed_1, embed_2])
    

    @case.command(name="delete", description="command to create a case")
    @app_commands.default_permissions(manage_messages=True)
    async def case_delete(self, interaction:Interaction, case_id:int):
        case = get_cases(interaction.guild_id, f"id = {case_id}")[0]
        embed = make_embed(case, interaction)
        await interaction.response.send_message(content="Are you sure you want do delete this case?", embed=embed, view=DeleteView(interaction.user, interaction, case_id))

    # case note commands
    notes = app_commands.Group(name="notes", description="case note related commands", parent=case)

    @notes.command(name="add", description="adds a note to a case")
    @app_commands.default_permissions(manage_messages=True)
    async def notes_add(self, interaction:Interaction):
        await interaction.response.send_message('test')