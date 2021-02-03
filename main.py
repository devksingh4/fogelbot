import discord
import os
from discord.ext import commands
from latex import render_latex
import random
import json
import praw
from discord.ext.tasks import loop

client = commands.AutoShardedBot(command_prefix='?')
# startup_extensions = ["Music"]
# if __name__ == "__main__":
#   for extension in startup_extensions:
#     try:
#       client.load_extension(extension)
#     except Exception as e:
#       exc = '{}: {}'.format(type(e).__name__, e)
#       raise SystemExit('Failed to load extension {}\n{}'.format(extension, exc))


token = os.environ['FogelBotDiscordKey']
reddit_token = os.environ['RedditKey']


reddit = praw.Reddit(client_id='ZOkK-ZCFJpcWCQ', client_secret=reddit_token,
                     user_agent='FogelBot by AsyncSGD', username='androstudios')


def createRandomSortedList(num, start=1, end=50):
  arr = []
  tmp = random.randint(start, end)

  for _ in range(num):
      while tmp in arr:
          tmp = random.randint(start, end)
      arr.append(tmp)

  arr.sort()

  return arr


@loop(seconds=150)
async def refreshCache():
  global cache
  global cache_funny
  cache = [i for i in reddit.subreddit('memes').new() if not i.stickied]
  cache_funny = [i for i in reddit.subreddit('funny').new() if not i.stickied]


@client.event
async def on_ready():
  global cache
  global cache_funny
  cache = [i for i in reddit.subreddit('memes').new() if not i.stickied]
  cache_funny = [i for i in reddit.subreddit('funny').new() if not i.stickied]
  print('Logged in as: ' + str(client.user.name) + ' ' + str(client.user.id))
  activity = discord.Game(name='silently judging Hatikvah | ?help')
  await client.change_presence(activity=activity)


@client.event
async def on_message(message):
  try:
    start_marker = end_marker = '$$'
    string = message.content
    start = string.index(start_marker) + len(start_marker)
    end = string.index(end_marker, start + 1)
    lc = string[start:end]
    if lc:
      async with message.channel.typing():
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
  except ValueError:  # no latex command found
    await client.process_commands(message)


class Main_Commands():
  def __init__(self, client):
    self.client = client


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
async def quote(ctx, num=1):
  """Send a Fogel quote"""
  quote_template = """
> {}
~ Dr. Micah E. Fogel
  """
  with open('quotes.txt', 'rb') as file:
    quotes = list(map(lambda x: x.strip(), file.readlines()))
  if num > len(quotes):
    await ctx.send("There are not enough unique quotes to fufill this request.")
    return
  while num > 0:
    random_index = random.randrange(len(quotes))
    await ctx.send(quote_template.format(str(quotes[random_index].decode("utf-8"))))
    del quotes[random_index]
    num -= 1


@client.command()
async def mathbio(ctx):
  """Send a biography about a famous mathematician"""
  bio_template = """
***{}***
**Born:** {} ({})
**Died:** {} ({})

**Summary:** {}

**Read more:** {}
  """
  files = os.listdir('bios')
  random_index = random.randrange(len(files))
  with open('bios/{}'.format(files[random_index])) as f:
    data = json.load(f)
    await ctx.send(bio_template.format(data["name"], data["born"], data["born_place"], data["died"], data["died_place"], data["summary"], data["link"]))


@client.command()
async def meme(ctx, numMemes=1):
  """Sends a number of memes to a channel."""
  try:
    if (int(numMemes) > 20 or int(numMemes) < 1):
      await ctx.send("Please provide a reasonable number of memes.")
      return
  except:
    await ctx.send("Please provide a reasonable number of memes.")
    return
  x = int(numMemes)
  randomlist = createRandomSortedList(x)
  for i in randomlist:
    selectedpost = cache[i]
    if "i.redd.it" in selectedpost.url or 'imgur' in selectedpost.url:
      await ctx.send("Here is a meme from r/memes: https://reddit.com{}".format(selectedpost.permalink), embed=discord.Embed(title=selectedpost.title).set_image(url=selectedpost.url))
    else:
      await ctx.send("Here is a meme from r/memes: {} \n\n*This post is a video. Please click on the link to see the full video*".format(selectedpost.url))


@client.command()
async def funny(ctx, numMemes=1):
  """Sends a number of memes to a channel."""
  try:
    if (int(numMemes) > 5 or int(numMemes) < 1):
      await ctx.send("Please provide a reasonable number of posts to retrieve from r/funny.")
      return
  except:
    await ctx.send("Please provide a reasonable number of posts to retrieve from r/funny.")
    return
  x = int(numMemes)
  randomlist = createRandomSortedList(x)
  for i in randomlist:
    selectedpost = cache_funny[i]
    if "i.redd.it" in selectedpost.url or 'imgur' in selectedpost.url:
      await ctx.send("Here is a post from r/funny: https://reddit.com{}".format(selectedpost.permalink), embed=discord.Embed(title=selectedpost.title).set_image(url=selectedpost.url))
    else:
      await ctx.send("Here is a post from r/funny: https://reddit.com{} \n\n *This post is a video. Please click on the link to see the full video*".format(selectedpost.permalink))

refreshCache.start()
client.run(token)
