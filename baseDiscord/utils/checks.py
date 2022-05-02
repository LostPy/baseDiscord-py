from discord.ext import commands


def is_app_owner_or_whitelist(*ids: int):
    """Decorator to check if a user of command is app owner or \
    a user in whitelist.
    """
    def predicate(ctx):
        return ctx.bot.is_owner(ctx.author) or ctx.author.id in ids
    return commands.check(predicate)
