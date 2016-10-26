import discord
from discord.ext import commands
from cogs.utils import checks
import os
import asyncio


class FileManager:
    """Handy file manager for bot owners."""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command(name="fm", pass_context=True)
    async def fm_command(self, ctx, command: str=None, path: str=None, url: str=None):
        """The file manager command itself."""
        if command is None:
            await self.bot.say("You need to specify an argument.\n"
                               "Try fm help for help")
        elif command == "help":
            await self.bot.say("Current commands available:```\n"
                               "ls      List files in the specified directory\n"
                               "wget    Downloads a file to the specified directory\n"
                               "rm      Deletes the specified file\n"
                               "```")
        elif command == "ls":
            ls = ""
            for i in os.listdir(path):
                ls = ls + "\n" + i
            await self.bot.say(ls)
        elif command == "rm":
            try:
                os.remove(path)
                await self.bot.say("Removed.")
            except FileNotFoundError:
                await self.bot.say("404: File Not Found")
            except:
                await self.bot.say("An unspecified error occurred.")
        elif command == "wget":
            await self.bot.say("That command is currently under construction.")
        elif command == "get":
            try:
                await self.bot.upload(path)
            except:
                await self.bot.say("That file might not exist or might be too big.")
        else:
            await self.bot.say("That isn't a valid command.")


def setup(bot):
    n = FileManager(bot)
    bot.add_cog(n)
