import asyncio

import discord
from discord.commands import permissions
from discord.ext import commands


class Owner(commands.Cog):
    """A cog to implement a some commands utils for owner of Bot.
    List commands:
        - stopbot: a command to disconnect the bot
    """

    def __init__(self):
        super().__init__()
        self.description = "Utils commands for the owner of Bot."

    @discord.slash_command(name="stopbot")
    @permissions.is_owner()
    async def stop_bot(self, ctx, delay: int = 5):
        """Command to stop the bot"""
        em = discord.Embed(title="Logout in progress...", color=ctx.bot.color)
        em.description = f"The bot will be logout in {delay} seconds."
        await ctx.respond(embed=em, ephemeral=True)

        try:
            ctx.bot.logger.warning(f"{ctx.author.name} disconnected the bot.")
        except AttributeError:
            print(f"{ctx.author.name} disconnected the bot.")

        await asyncio.sleep(delay)
        await ctx.bot.close()


def setup(bot: commands.Bot, *args, **kwargs):
    bot.add_cog(Owner(*args, **kwargs))
