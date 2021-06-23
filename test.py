import discord
from discord_slash import SlashCommand

from baseDiscord import BaseBot, Help, Owner



# Setting

TOKEN = "ODUzMDI5MjQxODU5NzM1NjEy.YMPbYw.Ch6QA0t4nDDH1jjXReneFAqzBFA"
COLOR = discord.Colour.green()
COLOR_ERROR = discord.Colour.red()
PERMISSIONS = 2147608640
PREFIX = 'test!'


# Init

bot = BaseBot(TOKEN, command_prefix=PREFIX, color=COLOR, color_error=COLOR_ERROR, permissions=PERMISSIONS, intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

Help.setup(bot)
Owner.setup(bot)

bot.run()
