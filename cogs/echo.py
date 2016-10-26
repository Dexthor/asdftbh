import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.chat_formatting import escape_mass_mentions
from __main__ import set_cog, send_cmd_help, settings
import importlib
import traceback
import logging
import asyncio
import threading
import datetime
import glob
import os
import time

log = logging.getLogger("red.owner")

class CogNotFoundError(Exception):
    pass

class CogLoadError(Exception):
    pass

class NoSetupError(CogLoadError):
    pass

class CogUnloadError(Exception):
    pass

class OwnerUnloadWithoutReloadError(CogUnloadError):
    pass

class echo:
    """I'll repeat what you said."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def say(self,ctx,*text):
        """I'll repeat what you said."""
        message = ctx.message
        channel = ctx.message.channel
        if "discord.gg/" in message.content.lower():
            return
        if "discord.me/" in message.content.lower():
            return
        if "https://discordapp.com/invite/" in message.content.lower():
            return
        text = " ".join(text)
        await self.bot.send_message(channel,escape_mass_mentions("\u200b{}".format(text)))

    @commands.command()
    @checks.is_owner()
    async def sonar(self, serverid, *, text):
        """I'll repeat what you said and where you want it.
        
        A modified version of the debug command, with help from Calebj."""

        #Your code will go here
        text = "".join(text)
        text = text.replace("\'", "\\\'")
        local_vars = locals().copy()
        local_vars['bot'] = self.bot
        code = "bot.send_message(bot.get_channel(serverid),'"+text+"')"
        python = '```py\n{}\n```'
        result = None

        try:
            result = eval(code, globals(), local_vars)
        except Exception as e:
            await self.bot.say(python.format(type(e).__name__ + ': ' + str(e)))
            return
                    
        if asyncio.iscoroutine(result):
            result = await result

        result = python.format(result)

def setup(bot):
    bot.add_cog(echo(bot))
