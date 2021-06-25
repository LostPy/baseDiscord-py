from typing import Union
import asyncio
import traceback
from datetime import datetime

import discord
from discord.ext import commands
from discord_slash.utils.manage_commands import remove_all_commands

from .utils import new_logger


class BaseBot(commands.Bot):
	"""A BaseBot which implement some functionnality:
		- manage errors
		- can send errors in DM to the owner
	"""

	def __init__(self, token: str, *args, color: discord.Colour, color_error: discord.Colour = discord.Colour.red(), send_errors: bool = False, permissions: int = 0, logger=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.token = str(token)
		self.send_errors = bool(send_errors)
		self.permissions = int(permissions)
		self.app_info = None  # load in on_ready event
		self.avatar_url = None  # load in on_ready event
		self.logger = logger if logger else new_logger(self.__class__.__name__)


		if isinstance(color, discord.Colour):
			self.color = color
		elif isinstance(color, (tuple, list)):
			self.color = discord.Colour.from_rgb(*color)
		else:
			raise ValueError(f"color must be an instance of discord.Colour or a tuple (RGB), not '{type(color)}'")

		if isinstance(color_error, discord.Colour):
			self.color_error = color_error
		elif isinstance(color_error, (tuple, list)):
			self.color_error = discord.Colour.from_rgb(*color_error)
		else:
			raise ValueError(f"color_error must be an instance of discord.Colour or a tuple (RGB), not '{type(color_error)}'")

		self.remove_command('help')

	def messages_on_ready(self):
		self.logger.info(f"Logged in as {self.user.name} - {self.user.id}")
		self.logger.info('-'*10 + '\n')

	async def init_on_ready(self):
		self.app_info = await self.application_info()
		self.avatar_url = self.user.avatar_url

	async def on_ready(self):
		await self.init_on_ready()
		self.messages_on_ready()

	async def on_error(self, event, *args, **kwargs):
		await super().on_error(event, *args, **kwargs)
		pass

	async def on_command_error(self, ctx, exception):

		await ctx.message.delete(delay=1)

		em_error = None

		if isinstance(exception, commands.errors.CommandNotFound):
			return

		elif isinstance(exception, commands.errors.BadArgument):
			em_error = discord.Embed(title="Bad Argument Error", color=self.color_error)
			em_error.description = "One or several arguments are not of type asked. Use the help command for more details."

		elif isinstance(exception, commands.errors.MissingRequiredArgument):
			em_error = discord.Embed(title="Missing Required Argument", color=self.color_error)
			em_error.description = "Missing one or several argument required. Use the help command for more details"

		elif isinstance(exception, commands.errors.MissingPermissions):
			em_error = discord.Embed(title="Missing Permissions Error", color=self.color_error)
			em_error.description = f"You have not the permissions to use this command: {exception.missing_perms}"

		elif isinstance(exception, commands.errors.MissingRoles):
			em_error = discord.Embed(title="Missing Roles Error", color=self.color_error)
			em_error.description = f"You missing roles to use this command: {exception.missing_roles}"

		elif isinstance(exception, commands.errors.BotMissingPermissions):
			em_error = discord.Embed(title="Bot Missing Permissions Error", color=self.color_error)
			em_error.description = f"I missing permissions: {exception.missing_perms}"

		elif isinstance(exception, commands.errors.BotMissingRole):
			em_error = discord.Embed(title="Bot Missing Roles Error", color=self.color_error)
			em_error.description = f"I missing roles: {exception.missing_roles}"

		else:
			if self.send_errors:
				em = discord.Embed(title="Exception raised", color=self.color_error)
				em.description = f"A exception was raised in a command:\n{traceback.format_exc(chain=False)}"
				em.set_thumbnail(url=self.avatar_url)
				em.set_footer(text=datetime.now().strftime("%Y-%m-%d at %H:%M:%S"))
				self.logger.exception(f"A exception was raised: {type(exception)}")
				await self.app_info.owner.send(embed=em)

		if em_error:
			try:
				em_error.set_thumbnail(url=self.avatar_url)
				return await ctx.send(embed=em_error, delete_after=8)
			except discord.Forbidden:
				try:
					return await ctx.author.send(content="I have not the permission to send message in this channel", embed=em_error, delete_after=10)
				except discord.Forbidden:
					pass

		await super().on_command_error(ctx, exception)

	def get_invitation(self, permissions: int = None):
		return f"https://discord.com/api/oauth2/authorize?client_id={self.app_info.id}&permissions={permissions if permissions else self.permissions}&scope=applications.commands%20bot"

	def run(self):
		super().run(self.token)