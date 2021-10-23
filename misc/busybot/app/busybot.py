#!/usr/bin/env python3.8

import os
import discord
import json
from cowpy import cow
from base64 import b64encode, b64decode
from discord.ext import commands
from discord.ext.commands import dm_only
from dotenv import load_dotenv

ENV_FILE = "/tmp/.env"

load_dotenv(ENV_FILE)

TOKEN = os.getenv("DISCORD_TOKEN")
RIDDLES_FILE = "riddles.json"
HELP_MSG = '''\
```
base64   encodes a string using Base64
  Usage:    ?base64 <string>
  Example:  ?base64 abcd
caesar   en(de)crypts a string using Caesar cipher
  Usage:    ?caesar <key> <string>
  Example:  ?caesar 10 abcd
calc     evaluates an arithmetic expression
  Usage:    ?calc <expression>
  Example:  ?calc 1+1
cowsay   configurable speaking cow (and a bit more cowacters)
  Usage:    ?cowsay <cowacter> <string>
  Example:  ?cowsay default moooo
help     Shows this message
  Usage:    ?help
ping     play ping pong with the bot
  Usage:    ?ping
riddle   print a riddle or its answer
  Usage:    ?riddle <riddle_id> <attribute=["problem", "answer"]>
  Example:  ?riddle 1 problem
rot13    en(de)crypts a string using rot13
  Usage:    ?rot13 <string>
  Example:  ?rot13 abcd
unbase64 decodes a Base64 encoded string
  Usage:    ?unbase64 <string>
  Example:  ?unbase64 YWJjZAo=
```\
'''

with open(RIDDLES_FILE) as f:
    riddles = json.load(f)

bot = commands.Bot(command_prefix="?")
bot.remove_command("help")

def caesar(message, key=13):
    y = lambda x: 65 if x.isupper() else 97
    return "".join(chr((ord(i) - y(i) + key) % 26 + y(i)) if i.isalpha() else i for i in message)

def multiwrap(message):
     return f"```{message}```" if message else ""

def wrap(message):
    return f"`{message}`" if message else ""

def spoiler(message):
    return f"||{message}||" if message else ""

@bot.event
async def on_ready():
    print(f"{bot.user.name} connection to Discord established.")
    for guild in bot.guilds:
        print(f"[+] {bot.user} connected to {guild}")
    await bot.change_presence(activity=discord.Game(name="?help"))

    os.environ.pop("DISCORD_TOKEN", None)
    os.remove(ENV_FILE)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(multiwrap('Missing one or more positional arguments.\n?help <command> for more information.'))
        return

    if isinstance(error, commands.CommandNotFound):
        await ctx.send(multiwrap('Command does not exist.\n?help for more information about the available commands.'))
        return

    if isinstance(error, commands.PrivateMessageOnly):
        await ctx.send(multiwrap(':lock: DMs only\nThis bot is only available in direct messages'))
        return

@bot.command(name="help", help="Show this message")
async def help(ctx):
    dm_channel = await ctx.author.create_dm()
    await dm_channel.send(HELP_MSG)

@bot.command(name="ping", help="play ping pong with the bot")
@dm_only()
async def pong(ctx):
    await ctx.send(wrap(f"Pong! time={round(bot.latency * 1000, 2)} ms"))

@bot.command(name="cowsay", brief="configurable speaking cow (and a bit more)",
    help=f"available cowacters: {', '.join(i for i in cow.COWACTERS)}"
)
@dm_only()
async def ascii(ctx, character, string):
    if character.lower() not in cow.COWACTERS:
        await ctx.send(wrap("This character has not been recruited yet."))
    else:
        ascii_art = cow.COWACTERS[character.lower()]().milk(string)
        await ctx.send(multiwrap(ascii_art))

@bot.command(name="riddle", brief=f"print a riddle or its answer",
    help=f"riddle_id can be one of the values in [1-{len(riddles)}].\nattribute can be either 'problem' or 'answer'."
)
@dm_only()
async def riddle(ctx, riddle_id: int, attribute):
    if attribute not in ["problem", "answer"]:
        await ctx.send(wrap(f"Invalid attribute field: {attribute}"))
        return

    riddle_id = str((riddle_id - 1) % len(riddles) + 1)
    if attribute == "problem":
        await ctx.send(multiwrap(riddles[riddle_id]["riddle"]))
    else:
        dm_channel = await ctx.author.create_dm()
        await dm_channel.send(spoiler(riddles[riddle_id]["answer"]))

@bot.command(name="base64", help="encodes a string using Base64")
@dm_only()
async def base64_encode(ctx, string):
    await ctx.send(wrap(b64encode(string.encode()).decode()))

@bot.command(name="unbase64", help="decodes a Base64 encoded string")
@dm_only()
async def base64_decode(ctx, string):
    await ctx.send(wrap(b64decode(string).decode()))

@bot.command(name="rot13", help="en(de)crypts a string using rot13")
@dm_only()
async def rot13_cipher(ctx, string):
    await ctx.send(wrap(caesar(string)))

@bot.command(name="caesar", help="en(de)crypts a string using Caesar cipher")
@dm_only()
async def caesar_cipher(ctx, key: int, string):
    await ctx.send(wrap(caesar(string, key)))

@bot.command(name="calc", help="evaluates an arithmetic expression")
@dm_only()
async def calc(ctx, expression):
    try:
        result = eval(expression)
    except:
        result = "Something went wrong..."

    await ctx.send(wrap(result))
    return

if __name__ == "__main__":
    bot.run(TOKEN)
