# helpers.py
from discord import Embed
import discord
import asyncio
import os
import json
from src import errors

# Creating the create embed function. This fuction takes a title, colour and a list of values. 
# It returns a discord Embed type.



def get_channel(bot, channel_id):
    if channel_id[:2] == "<#":
        channel_id = channel_id[2:-1]

    try:
        return bot.get_channel(int(channel_id))
    except:
        raise errors.ContentError("I can't find that channel! Please re-do the command.")

def create_embed(title_value, colour_value, values):
    new_embed = Embed(title=title_value, colour = colour_value)
    for a in values:
        new_embed.add_field(name=a[0],value=a[1],inline=a[2])
    return new_embed

# Create the function get message. This function returns the discord message type.
async def get_message(bot, message_id, channel = None):
    
    if not isinstance(channel, discord.channel.TextChannel):
        channel = get_channel(bot, channel)
    try:
        msg = await channel.fetch_message(int(message_id))
    except ValueError:
        raise errors.ContentError("I can't find that message! Please re-do the command.")
    return msg

# Create the function that create an embed for the message commands.
async def send_message_info_embed(ctx, command_type, author, content, message):
    title = 'Sent'
    list_content = [

        ["Author", author.mention, True],
        ["Channel", message.channel.mention, True],  
        ["Content", content, False]
    ]
    if command_type == 'edit':
        title = "Edited"
        list_content.insert(2, ["Original Content",message.content,False])
        list_content[3][0] = 'New Content'
        list_content[0][0] = "Editor"
    elif command_type == 'delete':
        title = 'Deleted'
        list_content[0][0] = "Deleter"
    elif command_type == 'fetch':
        title = 'Fetched'
        del list_content[1:2]
        del list_content[2:3]

    embed = create_embed(
        f"{title} the message!",
        discord.Colour(0xc387c1),
        list_content
    )
    if len(content) >=900 or len(message.content) >= 900:
        f = open('content.txt','w+')
        if command_type == 'edit':
            f.write(f'Original Content:\n\n{message.content}\n\nNew Content:\n\n{content}')
            del list_content[2:4]
        elif command_type == 'fetch':
            f.write(f'Cotent:\n\n{content}')
            del list_content[2:3]
        else:
            f.write(f'Content:\n\n{content}')
            del list_content[2:3]
        embed = create_embed(
            f'{title} the message!',
            discord.Colour(0xc387c1),
            list_content
        )
        f.close()
        fx = open('content.txt','r')
        await ctx.send(embed=embed, file = discord.File(fx, "Content.txt"))
        os.remove('content.txt')
    else:
        await ctx.send(embed=embed)
        

    



async def check_channel_id(ctx, channel_id, bot):
    def is_correct(m):
        return m.author == ctx.author
    if channel_id == None:
        message = await ctx.send(
            embed = create_embed(
                "What is the id of the channel?",
                discord.Color.blue(),
                []
            )
        )
        get_channel_id = await bot.wait_for('message', check=is_correct)
        try:
            await get_channel_id.delete()
            await message.delete()   
        except discord.errors.Forbidden:
            pass
        
        return get_channel_id.content
    else:
        return channel_id

async def check_message_id(ctx, message_id, bot):
    def is_correct(m):
        return m.author == ctx.author
    if message_id == None:
        message = await ctx.send(
            embed = create_embed(
                "What is the id of the message?",
                discord.Color.blue(),
                []
            )
        )
        get_message_id = await bot.wait_for('message', check=is_correct)
        
        try:
            await get_message_id.delete()
            await message.delete()
        except discord.errors.Forbidden:
            pass  
        return get_message_id.content
    else:
        return message_id

async def check_content(ctx, content, bot):
    def is_correct(m):
        return m.author == ctx.author
    if content == None or content == '':
        message = await ctx.send(
            embed = create_embed(
                "What is the content of the message to be?",
                discord.Color.blue(),
                []
            )
        )
        get_content= await bot.wait_for('message', check=is_correct)
        content = get_content.content
        try:
            await get_content.delete()
            await message.delete()   
        except discord.errors.Forbidden:
            pass 
        return content
    else:
        return content

if __name__ == "__main__":
    print("Im afraid you ran the wrong file, please run main.py instead.")

def setup(bot):
    print('    Misc functions!')