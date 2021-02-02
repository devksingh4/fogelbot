import discord
import os
from discord.ext import commands
from requests.api import delete
from latex import render_latex
import random

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
  try:
    start_marker = end_marker = '$'
    string = message.content
    start = string.index(start_marker) + len(start_marker)
    end = string.index(end_marker, start + 1)
    lc = string[start:end]
    id = render_latex(lc)
    if id != None:
      await message.reply(file=discord.File('{}.png'.format(id)))
      os.remove('{}.png'.format(id)) 
    else:
      await message.reply('Your LaTeX could not be rendered. Please, try again.')
      try:
        os.remove('{}.png'.format(id)) 
      except:
        pass
  except ValueError: # no latex command found
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
  id = ''
  async with ctx.typing():
    id = render_latex(latex)
    if id != None:
      await ctx.reply(file=discord.File('{}.png'.format(id)))
    else:
      await ctx.reply('Your LaTeX could not be rendered. Please, try again.')

  if id != None:
    os.remove('{}.png'.format(id))
  else:
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

@client.command()
async def quote(ctx):
  """Send a Fogel quote"""
  quote_template = """
> {}
~ Dr. Micah E. Fogel
  """
  with open('quotes.txt', 'rb') as file:
    quotes = list(map(lambda x: x.strip(), file.readlines()))
    random_index = random.randrange(len(quotes))
    await ctx.send(quote_template.format(str(quotes[random_index].decode("utf-8"))))


client.run(token)
