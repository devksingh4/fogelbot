import discord
from discord import TextChannel
import sys
import os
from discord.ext import commands
from discord import Game, Embed
from discord.voice_client import VoiceClient
import asyncio as asyncio
import time
from discord.ext.tasks import loop

client = commands.AutoShardedBot(command_prefix= '?')
startup_extensions = ["Music"]
debug_users = []
if __name__ == "__main__":
  for extension in startup_extensions:
    try:
      client.load_extension(extension)
    except Exception as e:
      exc = '{}: {}'.format(type(e).__name__, e)
      raise SystemExit('Failed to load extension {}\n{}'.format(extension, exc))
      

token = os.environ['DiscordKey']

@client.event
async def on_ready():
  print('Logged in as: ' + str(client.user.name) + ' ' + str(client.user.id))
  activity = discord.Game(name='?help)
  await client.change_presence(activity=activity)

@client.event
async def on_message(message):
  await client.process_commands(message)

class Main_Commands():
  def __init__(self,client):
    self.client=client

@client.command()
async def ping(ctx): 
  await ctx.send('Pong!')

@client.command()
async def clear(ctx, amount=0):
  if (amount == 0):
    await ctx.send("Please specify how many messages are to be deleted.")
  else:
    try:
      realNum = amount + 1
      await ctx.channel.purge(limit=realNum)
    except discord.errors.Forbidden:
      await ctx.send("Bot does not have neccessary permissions to delete messages.")


client.run(token)
