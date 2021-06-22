from typing import Union
import asyncio

import discord
from discord.ext import commands
from discord_slash.utils.manage_commands import remove_all_commands

from .utils import new_logger


class BaseBot(commands.Bot):
	"""A BaseBot which implement some functionnality:
		- manage errors
		- can send errors in DM to the owner
	"""

	def __init__(self, token: str, *args, color: discord.Colour, color_error: discord.Colour, send_errors: bool = False, print_traceback: bool = True, permissions: int = 0, logger=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.token = str(token)
		self.send_errors = bool(send_errors)
		self.print_traceback = bool(print_traceback)
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

	def message_on_ready(self):
		self.logger.info(f"Logged in as {self.user.name} - {self.user.id}")
		self.logger.info('-'*10 + '\n')

	async def init_on_ready(self):
		self.app_info = await self.application_info()
		self.avatar_url = self.user.avatar_url

	async def on_ready(self):
		await self.init_on_ready()
		self.message_on_ready()

	async def on_connect(self):
		self.logger.debug('connected!')

	async def on_disconnect(self):
		self.logger.debug("disconnected!")

	async def on_error(self, event, *args, **kwargs):
		await super().on_error(event, *args, **kwargs)
		pass

	async def on_command_error(self, ctx, exception):
		await super().on_command_error(ctx, exception)
		pass

	def get_invitation(self):
		return f"https://discord.com/api/oauth2/authorize?client_id={self.app_info.id}&permissions={self.permissions}&scope=applications.commands%20bot"

	def run(self):
		super().run(self.token)