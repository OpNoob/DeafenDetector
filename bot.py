import discord, typing
from discord.ext import commands, tasks
from discord import app_commands
from discord.ext.commands import has_permissions
import asyncio

from datastore import *
from bot_functions import *

with open("private/discord.txt", "r") as key_f:
    TOKEN = key_f.read()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

loop = asyncio.get_event_loop()


@tree.command(name="track_deafen", description="Starts user tracking for deafen")
@has_permissions(administrator=True)
async def trackDeafen(interaction, user: discord.Member):
    await interaction.response.send_message(f"Start tracking {user.mention} ...", ephemeral=False)
    addDeafenTrack(interaction.guild.id, user.id)
    await interaction.edit_original_response(content=f"User {user.mention} is now tracked.")


@tree.command(name="untrack_deafen", description="Stops user tracking for deafen")
@has_permissions(administrator=True)
async def untrackDeafen(interaction, user: discord.Member):
    await interaction.response.send_message(f"Stop tracking {user.mention} ...", ephemeral=False)
    removeDeafenTrack(interaction.guild.id, user.id)
    await interaction.edit_original_response(content=f"User {user.mention} is no longer tracked.")


@tree.command(name="stats_deafen", description="Number of times user went deafen")
async def untrackDeafen(interaction, user: discord.Member):
    await interaction.response.send_message(f"Getting {user.mention} stats ...", ephemeral=False)

    deafen_data = getDeafenData(user.id)
    if deafen_data is None:
        msg = f"Error getting states of {user.mention}"
        await interaction.edit_original_response(content=msg)
    else:
        msg = f"--\n{user.display_name}\n--\n\nTimes deafen: {deafen_data}"
        # \nTotal tracked deafen time: {bot_functions.ms_to_str(deafen_data.time_taken*1000)}
        await interaction.edit_original_response(content=msg)


@tree.command(name="xon", description="Xon deafen stats")
async def xon(interaction):
    await interaction.response.send_message(f"<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3", ephemeral=False)

    user_id = 171982078320181249
    user = await client.fetch_user(user_id)

    if user is None:
        msg = f"Error getting user"
        await interaction.edit_original_response(content=msg)
    else:
        deafen_data = getDeafenData(user.id)
        if deafen_data is None:
            msg = f"Error getting stats of {user.mention}"
            await interaction.edit_original_response(content=msg)
        else:
            msg = f"--\n{user.display_name}\n--\n\nTimes deafen: {deafen_data}"
            # \nTotal tracked deafen time: {bot_functions.ms_to_str(deafen_data.time_taken*1000)}
            await interaction.edit_original_response(content=msg)


@client.event
async def on_ready():
    await tree.sync()

    print("Ready!")

    frequentJobs.start()


@tasks.loop(seconds=60)
async def frequentJobs():
    user_ids = getTrackedDeafenUsers()
    user_deafened_ids = set()

    for guild in client.guilds:
        members = guild.members
        for member in members:
            if not member.bot and member.id in user_ids:
                voice = member.voice
                if voice.self_deaf or voice.deaf:
                    user_deafened_ids.add(member.id)
                else:
                    # Check if alone in voice channel
                    vc_members = voice.channel.members
                    if len(vc_members) == 1 and vc_members[0].id == member.id:
                        user_deafened_ids.add(member.id)

    alert_dict = updateDeafenUsers(user_deafened_ids)

    # Send message
    # for guild_id, user_ids in alert_dict.items():
    #     guild = client.get_guild(guild_id)
    #     if guild is not None:
    #         channel = guild.system_channel  # getting system channel
    #         for user_id in user_ids:
    #             user = guild.get_member(user_id)
    #             if user is not None:
    #                 msg = f"User {user.mention} is deafen!!"
    #                 await channel.send(msg)


if __name__ == "__main__":
    client.run(TOKEN)
    # while True:
    #     try:
    #         client.run(TOKEN)
    #     except Exception as e:
    #         print(str(e))
