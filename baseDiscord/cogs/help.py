import asyncio

import discord
from discord.ext import commands

from .. import HelpMessage


private_option = discord.Option(
    bool,
    name="private",
    default=True,
    required=False,
    description="If True, send help message in private"
)
categories_commands = []


class SlashHelp(commands.Cog):
    """A cog to implement a help command.
    The base global help command generate all documentation of the bot.
        * Pages can be customizable:
            - first page (global informations)
            - other pages (commands)
    """

    help_group = discord.SlashCommandGroup("help", "Useful help commands.")

    def __init__(self, max_cmd_by_page: int = 8):
        super().__init__()
        self.description = "Help commands. Commands to display informations on commands"
        self.max_cmd_by_page = max_cmd_by_page

    @help_group.command(name="all", description="Show a help on all commands.")
    async def help_all(self, ctx, private: private_option):
        """Global command Help.
        """
        paginator = HelpMessage(ctx.bot, ctx.bot.cogs,
                                author=ctx.author,
                                max_cmd_by_page=self.max_cmd_by_page,
                                info_page=True)
        await paginator.respond(ctx.interaction, ephemeral=private)


def setup(bot: commands.Bot, *args, **kwargs):
    bot.add_cog(SlashHelp(bot, *args, **kwargs))
