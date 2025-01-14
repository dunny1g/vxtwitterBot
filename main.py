import discord
import json
import re
from logger import logger

with open('config.json') as f:
    config = json.load(f)

DISCORD_TOKEN: str = config['DISCORD_TOKEN']
REPLY_TO: int = config['REPLY_TO']
DELETE_OP: int = config['DELETE_OP']
PREAMBLE: str = config['PREAMBLE']
MATCH1: str = config['MATCH1']
MATCH2: str = config['MATCH2']
REPLACE: str = config['REPLACE']

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.id == bot.user.id:
        return

    # Only need to match once, message.content.replace replaces all
    twitter_link = re.findall('https://twitter.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)
    x_link = re.findall('https://x.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)
    
    if twitter_link:
        logger.info(f'{message.guild.name}: {message.author} {message.content}')
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(MATCH1, REPLACE)}'
        allowed_mentions = discord.AllowedMentions(
            everyone=message.mention_everyone,
            users=message.mentions,
            roles=message.role_mentions
            )
        if REPLY_TO == 1:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=message) 
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions) 
            
        if DELETE_OP == 1:
            await message.delete()

    if x_link:
        logger.info(f'{message.guild.name}: {message.author} {message.content}')
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(MATCH2, REPLACE)}'
        allowed_mentions = discord.AllowedMentions(
            everyone=message.mention_everyone,
            users=message.mentions,
            roles=message.role_mentions
            )
        if REPLY_TO == 1:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=message) 
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions) 
            
        if DELETE_OP == 1:
            await message.delete()

bot.run(DISCORD_TOKEN, log_handler=None)