from os import environ
import discord

from baseDiscord import BaseBot


# Setting
TOKEN = environ['DISCORD_BOT']
COLOR = discord.Colour.green()
COLOR_ERROR = discord.Colour.red()
PERMISSIONS = 335007542336
PREFIX = '$'


# Init
bot = BaseBot(TOKEN,
              debug_guilds=[],  # guilds id to debug slash commands
              command_prefix=PREFIX,
              color=COLOR,
              color_error=COLOR_ERROR,
              permissions=PERMISSIONS)

bot.load_extension("baseDiscord.cogs.owner")
bot.load_extension("baseDiscord.cogs.help")

bot.run()
