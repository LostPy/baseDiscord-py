from typing import Union
import asyncio

import discord
from discord.ext import commands
from discord_components import DiscordComponent


class BaseBot(commands.Bot):
	"""A BaseBot which implement some functionnality:
		- manage errors
		- can send errors in DM to the owner
	"""

	def __init__(self, token: str, *args, color: discord.Colour, color_error: discord.Colour, send_errors: bool = False, print_traceback: bool = True, permissions: int = 0, **kwargs):
		super().__init__(*args, **kwargs)
		self.token = str(token)
		self.send_errors = bool(send_errors)
		self.print_traceback = bool(print_traceback)
		self.permissions = int(permissions)


		if isinstance(color, discord.Colour):
			self.color = color
		elif isinstance(color, (tuple, list)):
			self.color = discord.Colour.from_rgb(*color)
		else:
			raise ValueError(f"")

		if isinstance(color_error, discord.Colour):
			self.color_error = color_error
		elif isinstance(color_error, (tuple, list)):
			self.color_error = discord.Colour.from_rgb(*color_error)
		else:
			raise ValueError(f"")

	async def on_ready(self):
		pass

	async def on_connect(self):
		pass

	async def on_disconnect(self):
		pass

	async def on_error(self, event, *args, **kwargs):
		pass

	async def on_command_error(self, ctx, exception):
		pass

	def get_invitation(self):
		return f"https://discord.com/api/oauth2/authorize?client_id={self.app_info.id}&permissions={self.permissions}&scope=applications.commands%20bot"

	def run(self):
		super().run(self.token)