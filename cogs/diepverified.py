import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import escape_mass_mentions
from __main__ import settings, send_cmd_help
from copy import deepcopy
import asyncio
import logging
import os

log = logging.getLogger("red.admin")


class Verified:
    """Diep.io chat verified system."""

    def __init__(self,bot):
        self.bot = bot
        self.role = Verified
        self.server = '195278167181754369'

    @commands.command(pass_context=True, no_pm =True)
    @checks.mod_or_permissions(manage_roles=True)
    async def verify(self, ctx, user: discord.Member=None):
        """verifies a user

        """
        author = ctx.message.author
        channel = ctx.message.channel 
        server = 195278167181754369
        role = self.role
        if server.id != 195278167181754369:
            return
        if not channel.permissions_for(server.me).manage_roles:
            await self.bot.say('I don\'t have manage_roles.')
            return
        await self.bot.add_roles(user, role)
        if ctx.message.server.id == '195278167181754369':
            await self.bot.send_message(self.bot.get_channel('195278167181754369'),"{} is now **verified** by **{}**. Welcome to **{}**\n".format(user.mention, author.name, server.name))

    @commands.command(no_pm=True, pass_context=True)
    async def selfverify(self, ctx):
        """Allows lvl 5+ users verfy themselves.
        """
        author = ctx.message.author
        role = self.role
        try:
            #
            level5 = discord.utils.find(lambda m: m.name == "Level +5", ctx.message.server.roles)
            verified = discord.utils.find(lambda m: m.name == "Verified", ctx.message.server.roles)
            if verified in ctx.message.author.roles:
                await self.bot.say("Already verified. -.-")
                return
            if level5 in ctx.message.author.roles:
                await self.bot.add_roles(author, role)
                await self.bot.say("Verified!")
                if ctx.message.server.id == '195278167181754369':
                    await self.bot.send_message(self.bot.get_channel('195278167181754369'),"{} is now **verified**. Welcome to **{}**\n".format(author.mention, server.name))
        #
        except discord.errors.Forbidden:
            log.debug("{} just tried to add a role but I was forbidden".format(
                author.name))
            await self.bot.say("I don't have permissions to do that.")
            #
            if level5 not in ctx.message.author.roles:
                await self.bot.say("Nope, manual verification needed.")

def setup(bot):
    n = Verified(bot)
    bot.add_cog(n)
