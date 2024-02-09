# bot.py
import discord
from discord.ext import commands
import os

GUILD = 'The H Train'
CHANNEL_ID = 1175662274237693992 # pam
MESSAGE_ID = 1205606369139494972
ROLE_ID = 1205595007981981766 # train-conductor
TOKEN = # see .token file
intents = discord.Intents().default()
intents.members = True
bot = commands.Bot(
    command_prefix="!",
    description="I am a bot! Type !help in any channel for more info " + \
        "or ask a moderator.",
    intents=intents
)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != MESSAGE_ID or payload.event_type != 'REACTION_ADD':
        return

    guild = None
    for guild_i in bot.guilds:
        if guild_i.name == GUILD:
            guild = guild_i
    if guild is None:
        raise ValueError(f"Guild name {GUILD} missing from bot permissions")

    channel = None
    for channel_i in guild.channels:
        if channel_i.id == CHANNEL_ID:
            channel = channel_i
    if channel is None:
        raise ValueError(f"Channel ID {CHANNEL_ID} missing from {GUILD}")

    try:
        message = await channel.fetch_message(MESSAGE_ID)
    except NotFoundError:
        raise ValueError(f"Message ID {MESSAGE_ID} not found in channel {channel.name}")

    role = guild.get_role(ROLE_ID)

    for reaction in message.reactions:
        async for user in reaction.users():
            if user.id != payload.user_id:
                await reaction.remove(user) # Remove everyone else's reacts
                await user.remove_roles(role) # Remove roles from everyone else
    await guild.get_member(payload.user_id).add_roles(role) # Give you the role!


bot.run(TOKEN)
