from typing import Union
import asyncio

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_components import Button


class Help(commands.Cog):
	"""A cog to implement a help command.
	The base global help command generate all documentation of the bot.
		* Pages can be customizable:
			- first page (global informations)
			- other pages (commands)
	"""

	def __init__(self, bot: Union[discord.Client, commands.Bot]):
		super().__init__()
		if not isinstance(bot, (discord.Client, discord.ext.Bot)):
			raise ValueError(f"bot must be an instance of 'discord.Client' or 'discord.ext.Bot', not an instance of {type(bot)}")
		self.bot = bot
		self.description = "Help commands. Commands to display informations on commands"

	def first_page(self) -> discord.Embed:
		pass

	def commands_page(self) -> discord.Embed:
		pass

	@cog_ext.cog_subcommand(base="help", name="all", base_description="Help commands", description="Show a help on all commands in an embed multi pages")
	async def help_all(self, ctx):
		pass

	@cog_ext.cog_subcommand(base="help", name="command",
			description="Get help for a scpecific command",
			options = [create_option(
					name="name",
					type=3,  # string
					description="The name of command to get",
					choices=[],
					required=True
				)]
		)
	async def help_command(self, ctx, name: str):
		pass


	@cog_ext.cog_subcommand(base="help", name="groupcommands",
			description="Get help for a group commands",
			otpions=[
				create_option(
						name="name",
						type=3, # string
						description="The name of group commands to get",
						choices=[],
						required=True
					)
			]
		)
	async def help_groupscommands(self, ctx, name: str):
		pass

