import sqlite3
from discord import Embed, Interaction

def connect():
    return sqlite3.connect("database.db")

def save(conn:sqlite3.Connection):
    conn.commit()

def close(conn:sqlite3.Connection):
    save(conn)
    conn.close()


# Case commands

def create_case(server_id:int, mod_id:int, user_id:int, type:str, reason:str) -> tuple:
    conn = connect()
    cursor = conn.execute("INSERT INTO cases (server_id, mod_id, user_id, type, reason) VALUES (?,?,?,?,?) RETURNING id", (server_id, mod_id, user_id, type.lower(), reason))
    data = cursor.fetchone()
    close(conn)
    return data

def get_cases(server_id, condition):
    conn = connect()
    cusor = conn.execute(f"SELECT * FROM cases WHERE server_id = ? AND {condition}", (server_id,))
    data = cusor.fetchall()
    close(conn)
    return data

def make_embed(case:tuple, interaction:Interaction) -> Embed:
    mod = interaction.guild.get_member(case[2])
    user = interaction.guild.get_member(case[3])
    embed = Embed(title=f"{case[4]} case", description=f"Moderator: {mod.mention}\nUser: {user.mention}\n Reason: {case[5]}", color=0xff0000)
    embed.set_footer(text=f"case id: {case[0]}")
    return embed

def edit_case(server_id:int, set:str, condition:str):
    conn = connect()
    conn.execute(f"UPDATE cases SET {set} WHERE server_id = ? AND {condition}", (server_id,))
    close(conn)




def delete_case(server_id, condition):
    conn = connect()
    conn.execute(f"DELETE FROM cases WHERE server_id = ? AND {condition}", (server_id,))
    close(conn)