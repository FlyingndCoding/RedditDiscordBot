import asyncio
import discord
from redditHandlerAPI import redditHandler
import os
import datetime

customCommands = []

client = discord.Client()
reddit = redditHandler(os.getenv("id"), os.getenv("secret") , os.getenv("us_agent"))

@client.event
async def on_ready():
  await client.change_presence(game=discord.Game(name='Finding posts on reddit!'))

@client.event
async def on_message(message):
  if message.content.startswith("!getredditpost"):
    args = message.content.split()
    try:
      arg = args[1]
      element = reddit.getPostFromSubreddit(arg)
      if element == False:
        await client.send_message(message.channel, "That subreddit does not exist.")
      else:
        msg = discord.embeds.Embed(title=element.title, type="rich", url=element.url, description=f"score of: {element.score}", color=0x0000FF)
        msg.set_image(url=element.url)
        msg.set_author(name=element.author.name)
        await client.send_message(message.channel, embed=msg)
    except IndexError:
      await client.send_message(message.channel, "You must provide the name of the subreddit from which you want the post.")
  elif message.content.startswith("!meme"):
    element = reddit.getPostFromSubreddit("memes")
    msg = discord.embeds.Embed(title=element.title, type="rich", url=element.url, description=f"score of: {element.score}", color=0x0000FF)
    msg.set_image(url=element.url)
    msg.set_author(name=element.author.name)
    await client.send_message(message.channel, embed=msg)
  elif message.content.startswith("!redditbot help"):
    await client.send_message(message.channel, "Commands:\n\n!getredditpost [subreddit name] sends a post from this subreddit in the channel where the command was executed.\n\n!addcustomsubreddit [subreddit name] makes a custom command for that subreddit. For example if I did !addcustomsubreddit Dankemer then !Dankemer would become a new command that when executed would send a post from that subreddit to the channel where it was executed.\n\n!meme sends a meme from r/memes to the channel where it was executed.\n\n!redditbot help shows this message.")
  elif message.content.startswith("!addcustomsubreddit"):
    args = message.content.split()
    try:
      arg = args[1]
      if reddit.subredditExists(arg):
        customCommands.append(arg)
        await client.send_message(message.channel, "Custom command added")
    except IndexError:
      await client.send_message(message.channel, "You must provide the name of the subreddit from which you want to add.")

  elif message.content.startswith("!"):
    for e in customCommands:
      if e == message.content[1:]:
        element = reddit.getPostFromSubreddit(message.content[1:])
        msg = discord.embeds.Embed(title=element.title, type="rich", url=element.url, description=f"score of: {element.score}", color=0x0000FF)
        msg.set_image(url=element.url)
        msg.set_author(name=element.author.name)
        await client.send_message(message.channel, embed=msg)

client.run(os.getenv("token"))
