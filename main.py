# main.py
import os
import discord
import platform
import datetime
import helpers
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER = os.getenv('OWNER_ID')
prefix = os.getenv('PREFIX')

bot = commands.Bot(command_prefix = prefix, case_insensitive = True)

bot.remove_command('help')

@bot.event
async def on_ready():
    print("https://discord.com/api/oauth2/authorize?client_id={0}&permissions=519232&scope=bot".format(bot.user.id))
    print("Logged on as {0}!".format(bot.user))
    
    await bot.change_presence(
        activity = discord.Game(name="Watching for messages!")
    )

@bot.command(name='help', help='Responds with an embed with all the commands and options')
async def help(ctx):
    embed=helpers.create_embed(
    "Help with commands for the bot",
    16761035,
     [
         [f"`{prefix}ping`", "Replys with the latency of the bot", True],
         [f"`{prefix}help`", "Displays this view.", True],
         [f'`{prefix}info`', 'Displays info about the bot', True],
         [
             f'`{prefix}edit channel_id message_id new_content`',
             'Edits a message, message **must** be from the bot for it to work',
             True
         ],
        [
            f"`{prefix}send channel_id content`",
            "Sends a message from the bot in the specificed channel",
            True
        ]

     ]
)    
    await ctx.send(embed=embed)


@bot.command(name = 'info')
async def info(ctx):
    embed_content = [
         ["Username", bot.user, True],
         ["Prefix", prefix, True],
         ["Developer",'<@684964314234618044>', True],
         ["Discord.py Version", platform.python_version(), True],
         ["Number of Servers",len(bot.guilds), True]
     ]
    if OWNER != 'None':
        embed_content.insert(3,["Owner", f"<@{OWNER}>", True])
    embed=helpers.create_embed(
        "Info about the Bot",
        discord.Colour(0xc387c1),
        embed_content
    )    
    embed.set_thumbnail(url=f"{bot.user.avatar_url}")
    embed.set_footer(text = datetime.datetime.now())
    await ctx.send(embed=embed)

@bot.command(name="send")
async def send(ctx, channel_id, *args):
    content_list = []
    for a in args:
        content_list.append(a+" ")
    content = ''.join(content_list)
    channel = bot.get_channel(int(channel_id))
    await channel.send(content)
    embed = helpers.create_embed(
        f"Sent the message!",
         discord.Colour(0xc387c1),
          [
              ["Author", ctx.author.mention, True],
              ["Channel", channel.mention, True],            
              ["Content",content,False]
            ]
        )
    await ctx.send(embed=embed)

@bot.command(name="edit")
async def edit(ctx, channel_id, message_id, *args):
    channel = bot.get_channel(int(channel_id))
    msg = await channel.fetch_message(int(message_id))
    original_content = msg.content    
    content_list = []
    for a in args:
        content_list.append(a+" ")
    content = ''.join(content_list)
    await msg.edit(content=content)
    embed = helpers.create_embed(
        f"Edited the message!",
         discord.Colour(0xc387c1),
          [
              ["Author", ctx.author.mention, True],
              ["Channel", channel.mention, True],            
              ["Original Content",original_content,False],
              ["New Content", content, False]
            ]
        )
    await ctx.send(embed=embed)

#  Returns the bot side latency
@bot.command (name = "ping")
async def ping(ctx):
    await ctx.send(f"**ping** {round(bot.latency*100)}ms")   # get the bot latency in seconds then conver it into milli seconds.

bot.run(TOKEN)
