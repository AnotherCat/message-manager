# main.py
import os
import discord
import platform
import datetime
import helpers
from dotenv import load_dotenv
from discord.ext import commands

# load all the enviromental variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER = os.getenv('OWNER_ID')
prefix = os.getenv('PREFIX')
allowed_server = os.getenv('SERVER_ID')
management_role = os.getenv('MANAGEMENT_ROLE')

# Creating the bot class
bot = commands.Bot(command_prefix = prefix, case_insensitive = True)

# Removing the default help command
bot.remove_command('help')

#creating the check that checks if the bot is being used the server that is specified in env.
def check_if_right_server(ctx):
    if allowed_server == 'None':
        return True
    elif ctx.message.guild.id == int(allowed_server):
        return True
    else:
        return False

# Creating the check for the management role.
def check_if_manage_role(ctx):
    if management_role == "None":
        return True
    elif True:
        for role in ctx.author.role:
            if int(management_role) == role.id:
                return True
    else:
        return False

# Defining the on_ready event
@bot.event
async def on_ready():
    # Print the bot invite link
    print("https://discord.com/api/oauth2/authorize?client_id={0}&permissions=519232&scope=bot".format(bot.user.id))
    print("Logged on as {0}!".format(bot.user))
    
    await bot.change_presence(
        activity = discord.Game(name="Watching our important messages!")
    ) # Change the presence of the bot

# Create the bot command help. 
@bot.command(name='help', help='Responds with an embed with all the commands and options')
@commands.check(check_if_right_server)
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

# Create the info command.
@bot.command(name = 'info')
@commands.check(check_if_right_server)
async def info(ctx):
    embed_content = [
         ["Username", bot.user, True],
         ["Prefix", prefix, True],
         ["Developer",'<@684964314234618044>', True], # The developer (me), Must not be changed, as per the LICENSE
         ["Discord.py Version", platform.python_version(), True],
         ["Number of Servers",len(bot.guilds), True]
     ]
    if OWNER != 'None':
        embed_content.insert(3,["Owner", f"<@{OWNER}>", True]) # Check if the env OWNER is not "None", then if not adding the field to the embed.

    embed=helpers.create_embed(
        "Info about the Bot",
        discord.Colour(0xc387c1),
        embed_content
    )    
    embed.set_thumbnail(url=f"{bot.user.avatar_url}")
    embed.set_footer(text = datetime.datetime.now())
    await ctx.send(embed=embed)

# Create the send command. This command will send a message in the specificed channel.
@bot.command(name="send", rest_is_raw = True)
@commands.check(check_if_right_server)
@commands.check(check_if_manage_role)
async def send(ctx, channel_id, *, content):
    channel = bot.get_channel(int(channel_id)) # Get the channel.
    await msg = channel.send(content)
    embed = helpers.create_message_info_embed('Send', ctx.author, content, msg)
    await ctx.send(embed=embed)

# Create the edit command. This command will edit the specificed message. (Message must be from the bot)
@bot.command(name="edit", rest_is_raw=True)  # rest_is_raw so that the white space will not be cut from the content.
@commands.check(check_if_right_server)
@commands.check(check_if_manage_role)
async def edit(ctx, channel_id, message_id, *, content):
    #ctx.rest_is_raw = True
    msg = helpers.get_message(channel_id, message_id)
    if msg.author != bot.user:
        raise SyntaxError # Checks if the author of the message is the bot, if not raises an error (will customise error later)

    original_content = msg.content    
    embed = helpers.create_message_info_embed('edit', ctx.author, content, msg)
    await msg.edit(content=content)
    await ctx.send(embed=embed)

# Create the command delete. This will delete a message from the bot. 
@bot.command(name = 'delete')
async def delete(ctx, channel_id, message_id):
    msg = helpers.get_message(channel_id, message_id)

    if msg.author != bot.user: # Check if the message author is the bot. 
        raise SyntaxError
    
    embed = helpers.create_message_info_embed('delete', ctx.author, msg.content, msg)
    await.msg.delete()
    await ctx.send(embed=embed)

#  Returns the bot side latency
@bot.command (name = "ping")
@commands.check(check_if_right_server)
async def ping(ctx):
    await ctx.send(f"**ping** {round(bot.latency*100)}ms")   # get the bot latency in seconds then conver it into milli seconds.

bot.run(TOKEN)
