from typing import Union, List
import asyncio

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component
from discord_slash.model import ButtonStyle


dm_option = create_option(
				name="dm",
				option_type=5,  # Boolean
				required=False,
				description="If True, send help message in DM"
				)
categories_commands = []


class Help(commands.Cog):
	"""A cog to implement a help command.
	The base global help command generate all documentation of the bot.
		* Pages can be customizable:
			- first page (global informations)
			- other pages (commands)
	"""

	def __init__(self, bot: Union[discord.Client, commands.Bot], max_cmd_by_page: int = 8):
		super().__init__()
		if not isinstance(bot, (discord.Client, discord.ext.commands.Bot)):
			raise ValueError(f"bot must be an instance of 'discord.Client' or 'discord.ext.Bot', not an instance of {type(bot)}")
		self.bot = bot
		self.description = "Help commands. Commands to display informations on commands"
		self.max_cmd_by_page = max_cmd_by_page
		self._init_categories()

	def _init_categories(self):
		global categories_commands, commands
		print(self.bot.cogs)
		categories_commands = ['No category'] + [cog for cog in self.bot.cogs]

	def _base_embed(self, title: str, description: str = "", author: discord.User = None) -> discord.Embed:
		em = discord.Embed(title=title, description=description, color=self.bot.color)
		if author:
			em.set_author(name=author.name, icon_url=author.avatar_url)
		em.set_thumbnail(url=self.bot.avatar_url)
		return em

	def _command_base(self, cmd: commands.Command) -> str:
		return f"{cmd.description}\n**Name:** {cmd.name}\nhelp: {cmd.brief}"

	def _command_usage(self, cmd: commands.Command) -> str:
		return f"Usage: `{self.bot.command_prefix}{cmd.name} {cmd.usage}`"

	def _command_aliases(self, cmd: commands.Command) -> str:
		return f"""Aliases: {"`, `".join(cmd.aliases) + "`"}""" if len(cmd.aliases) > 0 else ""

	def _command_help_fmt(self, cmd: commands.Command) -> str:
		return "\n".join([self._command_base(cmd), self._command_usage(cmd) + self._command_aliases(cmd)])

	def first_page(self, author: discord.User = None) -> discord.Embed:
		desc_bot = f"""{self.bot.description}\n\nPrefix: {self.bot.command_prefix}\nAuthor: {self.bot.app_info.owner.name}"""
		em = self._base_embed(f"Help {self.bot.user.name}",
			description=desc_bot, author=author)
		msg_help = "To get this message, use the command `/help all`"

		em.add_field(name="Help command", value=msg_help)
		return em

	def commands_pages(self, group_cmd: Union[commands.Cog, List[commands.Command]], author: discord.User = None) -> List[discord.Embed]:
		"""Create the list of embeds with commands help.
		"""
		title = f"Help {group_cmd.__class__.__name__}" if isinstance(group_cmd, commands.Cog) else "No category"
		description = group_cmd.description if isinstance(group_cmd, commands.Cog) else ""
		em = self._base_embed(title, description, author=author)
		pages = [em]
		list_commands = group_cmd.get_commands() if isinstance(group_cmd, commands.Cog) else group_cmd

		nb_pages = 1
		nb_cmd = 0
		for cmd in list_commands:
			if nb_cmd == self.max_cmd_by_page:
				em = self.base_embed(title=title, description=description, author=author)
				pages.append(em)
				nb_cmd = 0
				nb_pages += 1
			if not cmd.hidden:
				em.add_field(name=f"Command {cmd.name}", value=self._command_help_fmt(cmd), inline=False)
				nb_cmd += 1

		return [em for em in pages if len(em.fields) > 0]

	def slash_commands_pages(self) -> List[discord.Embed]:
		raise NotImplemented

	def _help_command(self, cmd: commands.Command) -> discord.Embed:
		"""Create an embed with help for a specific command"""
		pass

	def _help_category(self, cmd: commands.Cog) -> List[discord.Embed]:
		"""Create a list of embeds for a Cog"""
		pass

	@cog_ext.cog_subcommand(base="help", name="all",
		base_description="Help commands",
		description="Show a help on all commands in an embed multi pages",
		options=[dm_option])
	async def help_all(self, ctx, dm: bool = False):
		"""Global command Help.
		Future: Add a Select component to naigate between pages.
		"""

		print(self.bot.commands)
		pages = [self.first_page(ctx.author)] + self.commands_pages(list(self.bot.commands), author=ctx.author)
		for cog in self.bot.cogs.values():
			pages += self.commands_pages(cog, author=ctx.author)
		
		nb_pages = len(pages)
		current_page = 1
		current_embed = pages[current_page-1]

		current_embed.set_footer(text=f"page: {current_page}/{nb_pages} - {current_embed.title}")
		
		components = create_actionrow(
				create_button(style=ButtonStyle.blue, emoji="◀️", custom_id='previous'),
				create_button(style=ButtonStyle.red, emoji="⏹️", custom_id='stop'),
				create_button(style=ButtonStyle.blue, emoji="▶️", custom_id='next'),
			) if nb_pages > 1 else create_actionrow(create_button(style=ButtonStyle.red, emoji="⏹️", custom_id='stop'))

		if dm:
			help_msg = await ctx.author.send(embed=current_embed, components=[components])
			ctx.send(content="The help message was send in DM!", hidden=True, delete_after=5)
		else:
			help_msg = await ctx.send(embed=current_embed, components=[components])

		while help_msg is not None:
			try:
				component_ctx = await wait_for_component(self.bot, messages=[help_msg], timeout=30)
				if component_ctx.custom_id == 'previous' and current_page > 1:
					current_page -= 1
				elif component_ctx.custom_id == 'previous':
					current_page = nb_pages
				elif component_ctx.custom_id == 'next' and current_page < nb_pages:
					current_page += 1
				elif component_ctx.custom_id == 'next':
					current_page = 1
				elif component_ctx.custom_id == 'stop':
					await help_msg.delete(delay=1)
					break

				current_embed = pages[current_page-1]
				current_embed.set_footer(text=f"page: {current_page}/{nb_pages} - {current_embed.title}")
				await component_ctx.edit_origin(embed=current_embed)

			except asyncio.TimeoutError:
				try:
					await component_ctx.edit_origin(components=[])
				except discord.Forbidden:
					pass
				break

			except discord.Forbidden:
				pass

	@cog_ext.cog_subcommand(base="help", name="command",
			description="Get help for a scpecific command",
			options = [
				create_option(
					name="name",
					option_type=3,  # string
					description="The name of command to get",
					required=True
				),
				dm_option]
		)
	async def help_command(self, ctx, name: str):
		pass


	@cog_ext.cog_subcommand(base="help", name="category",
			description="Get help for a category",
			options=[
				create_option(
						name="name",
						option_type=3, # string
						description="The name of category to get",
						choices=[
							create_choice(
							name=category,
							value=category,
							) for category in categories_commands
						],
						required=True
				),
				dm_option
			]
		)
	async def help_category(self, ctx, name: str):
		pass

	@classmethod
	def setup(cls, bot: commands.Bot, *args, **kwargs):
		bot.add_cog(cls(bot, *args, **kwargs))
