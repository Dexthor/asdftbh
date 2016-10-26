import discord
from discord.ext import commands
from discord import utils
from cogs.utils.dataIO import fileIO
from cogs.utils.chat_formatting import *
from __main__ import settings, send_cmd_help
import os
import re
import string

import datetime


class BotInfo:
    def __init__(self, bot):
        self.bot = bot


    @property
    def prefixes(self):
        '''ret = "["
        middle = "|".join(self.bot.command_prefix)
        return ret+middle+"]"'''
        return self.bot.command_prefix[0]

    @property
    def join_message(self):
        ret = bold("Hey there!") + "\n"
        ret += bold ("Read everthing carefully to have me working perfectly.\n")
        ret += "I'm x³ and I just got asked to join this server.\n"
        ret += "My current prefixes are " + self.prefixes
        ret += " and you can see all of my commands by running "
        ret += inline(self.prefixes + "help")
        ret += "I can do Music, Trivia, Custom Commands, Moderation, __Autoban mention spammers__,delete duplicate messages and much much more."
        ret += "\n\n"
        ret += bold("First things first, you need to set up and give me the perms i require for me to work as intended.\n")
        ret += "I listen to and obey to two roles `!` and `Bot Commander`\n"
        ret += "\n"
        ret += "`!` role grants **users** with all my **admin commands** and so be cautious who you give it to. (trusted people)\n"
        ret += "Admin commands : kick, ban, softban, addroles, remove roles, much more.\n "
        ret += "\n"
        ret += "`Bot Commander` role grants users with limited mod perms>"
        ret += "Mod commands : mute, move and few more. You basically need to see the help command for them."
        ret += "\n\n"
        ret += bold("Setting up mod-log\n")
        ret += "I have a mod log so make a channel named mod-log and only let me talk in there with all permissions to it.\n"
        ret += "Once you make mod-log, type `>modset modlog mod-log`"
        ret += "Now whenever you ban, kick, softban someone using my command or manually, i will post the mod action on that channel.\n"
        ret += "After you take a mod action, i recommend you type >reason reason, so i can update the mod log with which mod took the actions and why since it helps with transparency.\n"
        ret += "\n"
        ret += bold("Setting up mute\n")
        ret += "If the bot was given the required permissions then just type >mute @someuser 10s test \n"
        ret += "The bot will automatically set up the roles and role permissions for mute and muted users."
        ret += "For more help with mute command please type >mute \n"
        ret += "For help with any commands just type >help command-name \n"
        ret += "\n\n"
        ret += bold("If you need help you can contact Dex with >contact and please provide reason and invite link to your chat.\n")
        ret += "Please only use >contact if its necessarry and not just for small reasons. Thank you and i hope you people like me and i serve you good."
        ret += "Since i have many commands, it takes time for people to fully get used to me but after that you people will start liking me :).\n"
        return ret

    @property
    def leave_message(self):
        ret = "Phew low members! Due to server load and management i can only join on 100+ member servers. Bye~"
        return ret

    @commands.command()
    async def servercount(self):
        '''General global server information'''
        servers = sorted([server.name for server in self.bot.servers])
        ret = "I am currently in "
        ret += bold(len(servers))
        ret += " servers with "
        ret += bold(len(set(self.bot.get_all_members())))
        ret += " members.\n"
        await self.bot.say(ret)


    @commands.command()
    async def invite(self):
        """Invite me to a new server"""
        await self.bot.say("You must have manage server permissions in order"
                           " to add me to a new server. If you do, just click"
                           " the link below and select the server you wish for"
                           " me to join.\n"
                           "I only join servers with 100+ members for now.\n\n"
                           "https://discordapp.com/oauth2/authorize?client_id=181625801895051266&scope=bot&permissions=536083519")


    async def serverjoin(self, server):
        channel = server.default_channel
        if len(server.members) < 100:
            await self.bot.send_message(channel, self.leave_message)
            await self.bot.leave_server(server)
        else:
            print('Joined {} at {}'.format(server.name, datetime.datetime.now()))
            try:
                await self.bot.send_message(channel, self.join_message)
            except discord.errors.Forbidden:
                pass




def setup(bot):
    n = BotInfo(bot)
    bot.add_listener(n.serverjoin, "on_server_join")
    bot.add_cog(n)
