import discord
import os
from discord.ext import commands
from requests.api import delete
from latex import render_latex

client = commands.AutoShardedBot(command_prefix= '?')
# startup_extensions = ["Music"]
# if __name__ == "__main__":
#   for extension in startup_extensions:
#     try:
#       client.load_extension(extension)
#     except Exception as e:
#       exc = '{}: {}'.format(type(e).__name__, e)
#       raise SystemExit('Failed to load extension {}\n{}'.format(extension, exc))
      

token = os.environ['DiscordKey']

@client.event
async def on_ready():
  print('Logged in as: ' + str(client.user.name) + ' ' + str(client.user.id))
  activity = discord.Game(name='?help')
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
async def tex(ctx, latex): 
  """Render LaTeX code and reply with an image"""
  async with ctx.typing():
    id = render_latex(latex)
    if id != None:
      await ctx.reply(file=discord.File('{}.png'.format(id)))
      os.remove('{}.png'.format(id)) 
    else:
      await ctx.reply('Your LaTeX could not be rendered. Please, try again.')
      try:
        os.remove('{}.png'.format(id)) 
      except:
        pass
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
