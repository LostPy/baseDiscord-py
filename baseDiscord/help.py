import discord
from discord.ext import commands

from . import HelpMessage


class BaseDiscordHelp(commands.HelpCommand):

    def __init__(self, max_cmd_by_page: int = 8, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_cmd_by_page = max_cmd_by_page

    async def send_bot_help(self, mapping):
        paginator = HelpMessage(self.context.bot, mapping,
                                author=self.context.author,
                                max_cmd_by_page=self.max_cmd_by_page,
                                info_page=True)
        await paginator.respond(self.context, ephemeral=False)
