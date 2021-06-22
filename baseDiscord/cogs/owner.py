from typing import Union
import asyncio

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from ..utils import __logger_baseBot as logger
from ..utils.checks import is_app_owner_or_whitelist
from ..utils.manage_messages import safe_delete


class Owner(commands.Cog):
	"""A cog to implement a some commands utils for owner of Bot.
	List commands:
		- stopbot: a command to disconnect the bot
	"""

	def __init__(self, bot: Union[discord.Client, commands.Bot]):
		super().__init__()
		if not isinstance(bot, (discord.Client, discord.ext.commands.Bot)):
			raise ValueError(f"bot must be an instance of 'discord.Client' or 'discord.ext.Bot', not an instance of {type(bot)}")
		self.bot = bot
		self.description = "Utils commands for the owner of Bot."

	@commands.command("stopbot", aliases=('stopBot', 'stopB', 'StopBot', 'STOPBOT'), description="Command to stop the bot", hidden=True)
	@is_app_owner_or_whitelist()
	async def stop_bot(self, ctx, delay: int = 5):
		"""Command to stop the bot"""
		await safe_delete(ctx.message, delay=5)
		em = discord.Embed(title="Logout in progress...", color=self.bot.color)
		em.description = "The bot will be logout in 5 seconds."
		await ctx.send(embed=em, delete_after=delay-1)

		logger.warning(f"{ctx.author.name} disconnected the bot.")

		await asyncio.sleep(delay)
		await self.bot.logout()

	@classmethod
	def setup(cls, bot: commands.Bot, *args, **kwargs):
		bot.add_cog(cls(bot, *args, **kwargs))
