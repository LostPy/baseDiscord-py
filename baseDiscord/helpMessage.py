from typing import Union, Optional
from collections import Mapping

import discord
from discord.ext import commands, pages


categories_commands = []


class HelpMessage(pages.Paginator):
    """The help message content. It's a subclass of `discord.Paginator`"""

    def __init__(self,
                 bot: commands.Bot,
                 mapping: Mapping[Optional[commands.Cog], list[commands.Command]],
                 author: discord.User = None,
                 max_cmd_by_page: int = 8,
                 info_page: bool = False,
                 **kwargs):
        self.bot = bot
        self.max_cmd_by_page = max_cmd_by_page

        kwargs['pages'] = list()
        if info_page:
            kwargs['pages'].append(self.first_page())
        for cog, list_cmd in mapping.items():
            kwargs['pages'] += self.commands_pages(cog or list_cmd, author=author)

        super().__init__(kwargs.pop('pages'), **kwargs)

    def _init_categories(self):
        global categories_commands, commands
        categories_commands = ['No category'] + [cog for cog in self.bot.cogs]

    def _base_embed(self,
                    title: str,
                    description: str = "",
                    author: discord.User = None) -> discord.Embed:
        em = discord.Embed(title=title,
                           description=description,
                           color=self.bot.color)
        if author:
            em.set_author(name=author.name, icon_url=author.avatar)
        em.set_thumbnail(url=self.bot.avatar)
        return em

    def _command_base(self, cmd: commands.Command) -> str:
        return f"{cmd.description}\n**Name:** {cmd.name}\nhelp: {cmd.brief}"

    def _command_usage(self, cmd: commands.Command) -> str:
        if cmd.usage:
            return f"Usage: `{self.bot.command_prefix}{cmd.name} {cmd.usage}`"
        return "\r"

    def _command_aliases(self, cmd: commands.Command) -> str:
        if len(cmd.aliases) > 0:
            return f"""Aliases: {"`, `".join(cmd.aliases) + "`"}"""
        return "\r"

    def _command_help_fmt(self, cmd: commands.Command) -> str:
        return "\n".join([
            self._command_base(cmd),
            self._command_usage(cmd),
            self._command_aliases(cmd)
        ])

    def first_page(self, author: discord.User = None) -> pages.Page:
        desc_bot = f"{self.bot.description}\n\n"\
                   f"Prefix: {self.bot.command_prefix}\n"\
                   f"Author: {self.bot.app_info.owner.name}"
        em = self._base_embed(f"Help {self.bot.user.name}",
                              description=desc_bot,
                              author=author)
        msg_help = "To get this message, use the command `/help all`"

        em.add_field(name="Help command", value=msg_help)
        return pages.Page(embeds=[em])

    def commands_pages(self,
                       group_cmd: Union[commands.Cog, list[commands.Command]],
                       author: discord.User = None) -> list[pages.Page]:
        """Create the list of embeds with commands help.
        """
        if isinstance(group_cmd, commands.Cog):
            title = f"Help {group_cmd.__class__.__name__}"
        else:
            title = "No category"

        if isinstance(group_cmd, commands.Cog):
            description = group_cmd.description
        else:
            description = ""

        em = self._base_embed(title, description, author=author)
        pages = [em]
        if isinstance(group_cmd, commands.Cog):
            list_commands = group_cmd.get_commands()
        else:
            list_commands = group_cmd

        nb_cmd = 0
        for cmd in list_commands:
            if nb_cmd == self.max_cmd_by_page:
                em = self.base_embed(title=title,
                                     description=description,
                                     author=author)
                pages.append(pages.Page(embeds=[em]))
                nb_cmd = 0
            if isinstance(cmd, commands.Command) and not cmd.hidden:
                em.add_field(name=f"Command {cmd.name}",
                             value=self._command_help_fmt(cmd),
                             inline=False)
                nb_cmd += 1

        return [em for em in pages if len(em.fields) > 0]

    def slash_commands_pages(self) -> list[pages.Page]:
        raise NotImplemented

    def _help_command(self, cmd: commands.Command) -> discord.Embed:
        """Create an embed with help for a specific command"""
        pass

    def _help_category(self, cmd: commands.Cog) -> discord.Embed:
        """Create a list of embeds for a Cog"""
        pass
