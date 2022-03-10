#!/usr/bin/env python3.7
# Selects Python version

# Variable declarations, replace [insert number] with appropriate ID
# Change roleCName to appropriate role name
# Guild = Server

roleAId = [insert number]
roleBId = [insert number]
roleCId = [insert number]
roleCName = "Name of role to be added or removed"

guildId = [insert number]
channelId = [insert number]

# Prefix declaration, though slash commands are all that is used

prefix = "Prefix" 

# Imports

import discord
from discord.utils import get
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

# Initialise the bot

intents = discord.Intents().all() # Declares intents
bot = commands.Bot(command_prefix=prefix, intents=intents) # Creates bot
slash = SlashCommand(bot, sync_commands=True) # Enables slash commands

# Slash Command for checking roles

@slash.slash(name="role_check", description=f"Checks all current users to see if {roleCName} needs to be added")
async def test(ctx: SlashContext):
    await ctx.send("Checking now...")
    guild = bot.get_guild(guildId)
    roleAddCounter = 0
    roleLossCounter = 0
    for member in guild.members:
        roleIds = []
        for i in member.roles:
            roleIds.append(i.id)
        if roleAId in roleIds and roleBId in roleIds and roleCId not in roleIds:
            role = get(bot.get_guild(guildId).roles, id=roleCId)
            await member.add_roles(role)
            roleAddCounter += 1
        if roleCId in roleIds and roleAId not in roleIds or roleCId in roleIds and roleBId not in roleIds:
            role = get(bot.get_guild(guildId).roles, id=roleCId)
            await member.remove_roles(role)
            roleLossCounter += 1

    if roleAddCounter != 0 and roleLossCounter == 0:
        await ctx.send(f"Added {roleCName} to: {roleAddCounter} user(s)\nDid not remove {roleCName} from any users")
    elif roleAddCounter != 0 and roleLossCounter != 0:
        await ctx.send(f"Added {roleCName} to: {roleAddCounter} user(s)\nRemoved {roleCName} from: {roleLossCounter} user(s)")
    elif roleAddCounter == 0 and roleLossCounter != 0:
        await ctx.send(f"Did not add {roleCName} to any users\nRemoved {roleCName} from: {roleLossCounter} user(s)")
    elif roleAddCounter == 0 and roleLossCounter == 0:
        await ctx.send(f"No action was taken. Roles are accurate.")

# Event listener to update roles when needed if there is a role change

@bot.event
async def on_member_update(before, after):
    if len(before.roles) < len(after.roles):
        newRole = next(role for role in after.roles if role not in before.roles) # Checks which role was gained
        if newRole.id == roleAId or newRole.id == roleBId:
            roleIds = []
            for i in after.roles:
                roleIds.append(i.id)
            if roleAId in roleIds and roleBId in roleIds and roleCId not in roleIds:
                role = get(bot.get_guild(guildId).roles, id=roleCId)
                await after.add_roles(role)
    elif len(before.roles) > len(after.roles):
        lostRole = next(role for role in before.roles if role not in after.roles)
        if lostRole.id == roleAId or lostRole.id == roleBId:
            roleIds = []
            for i in after.roles:
                roleIds.append(i.id)
            if roleCId in roleIds:
                role = get(bot.get_guild(guildId).roles, id=roleCId)
                await after.remove_roles(role)

# Run the bot

bot.run("TOKEN") # Token template, do not share. Must be replaced with what is acquired from Discord Developer Portal
