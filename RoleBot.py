#!/usr/bin/env python3.7
# Selects Python version

# Variable declarations, replace [insert number] with appropriate ID, without []
# Change roleCName to appropriate role name
# Guild = Server

roleAId = [replace_with_id]
roleBId = [replace_with_id]
roleCId = [replace_with_id]
roleCName = "Replace With Role Name"

guildId = [replace_with_id]
channelId = [replace_with_id]

# Prefix declaration, though slash commands are all that is used

prefix = "Prefix" 

# Imports

import boto3
import base64
from botocore.exceptions import ClientError
import json
import os
from dotenv import load_dotenv

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

# Even listener to update roles when needed if there is a role change

@bot.event
async def on_member_update(before, after):
    if len(before.roles) < len(after.roles):
        newRole = next(role for role in after.roles if role not in before.roles) # checks which role was gained
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

# Load token with Secrets Manager AWS

def get_secret():

    secret_name = "secret_name"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])


secretValues = get_secret() # get secrets str
secret = json.loads(secretValues) # convert SecretString value to JSON
token = secret['TOKEN'] # declare the token

# Load token with .env

# load_dotenv()
# token = os.environ.get('TOKEN')

# Run the bot

bot.run(token) # Token template, do not share. Must be replaced with what is acquired from Discord Developer Portal