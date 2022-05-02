import asyncio
import discord


async def safe_delete(message: discord.Message, delay: int = 0) -> None:
    if not isinstance(message, discord.Message):
        raise ValueError(
            "message must be an instance of "
            f"discord.Message, not of '{type(message)}'")
    try:
        await message.delete(delay=int(delay))
    except discord.Forbidden:
        pass
    except discord.NotFound:
        pass
