from typing import Union
import asyncio

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_components import Button


class Owner(commands.Cog):
	"""A cog to implement a some commands utils for owner of Bot.
	List commands:
		- stopbot: a command to disconnect the bot
	"""

	def __init__(self, bot: Union[discord.Client, commands.Bot]):
		super().__init__()
		if not isinstance(bot, (discord.Client, discord.ext.Bot)):
			raise ValueError(f"bot must be an instance of 'discord.Client' or 'discord.ext.Bot', not an instance of {type(bot)}")
		self.bot = bot
		self.description = "Utils commands for the owner of Bot."

	@cog_ext.cog_slash(name="stopbot", description="Command to stop the bot",
			options=[create_option(
					name="delay",
					description="Delay in seconds before stop the bot. Default: 5 seconds",
					type=4, # integer
					required=False
				)]
		)
	async def stop_bot(self, ctx, delay: int = 5):
		pass