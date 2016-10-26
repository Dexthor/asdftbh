import discord
from discord.ext import commands
import os
from .utils.dataIO import fileIO
from .utils import checks
from datetime import datetime
from threading import Thread
from time import sleep
import asyncio

default_settings = {"SERVER": {"DEFAULT": False}}

class Noads:
    """Deletes discord invite links, disabled by default."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/noads/settings.json", "load")
        self.RX_MESSAGE_THRESHOLD = 1           # number of messages rx before consider spam
        self.RX_MESSAGE_DELTA_THRESHOLD = 1.5   # messages rx with 1.5 or less seconds between
        self.message_history = {}
        self.spam_levels = {}
        self.shitlist = []
        self.role_name = 'Timeout'

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def noads(self, ctx):
        """Toggle discord invite links delete for a server"""
        server = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = True
        else:
            self.settings[server.id] = not self.settings[server.id]
        if self.settings[server.id]:
            await self.bot.say('```diff\n+Invite links delete enabled in {}```'.format(server.name))
            fileIO("data/noads/settings.json", "save", self.settings)
        else:
            await self.bot.say('```diff\n-Invte links delete disabled in {}```'.format(server.name))
            fileIO("data/noads/settings.json", "save", self.settings)

    async def check_noads(self, message):
        enabled = self.settings.get(message.server.id, False)
        if message.server.id == '133049272517001216': #red's server
            return
        if message.author.id == '107248022945058816': #dex id
        	return            
        if message.author.id == '135288293548883969': #rh1n0 bots id to avoid log delete loop if the bot can see rh1nos mod logs channel
            return
        if message.author.id == '192332211549241344': #vonodosh
            return               
        else:
            if message.author.id != self.bot.user.id:
                if "discord.gg/" in message.content.lower():
                    if enabled:
                        await self.bot.delete_message(message)
                        await self.bot.send_message(message.channel, "{0.author.mention} **Please dont post invites in this server, thanks!**".format(message))
                elif "discord.me/" in message.content.lower():
                    if enabled:
                        await self.bot.delete_message(message)
                        await self.bot.send_message(message.channel, "{0.author.mention} **Please dont post invites in this server, thanks!**".format(message))
                elif "https://discordapp.com/invite/" in message.content.lower():
                    if enabled:
                        await self.bot.delete_message(message)
                        await self.bot.send_message(message.channel, "{0.author.mention} **Please dont post invites in this server, thanks!**".format(message))
                elif "discord.gg\u200b/" in message.content.lower():
                    if enabled:
                        await self.bot.delete_message(message)
                        await self.bot.send_message(message.channel, "{0.author.mention} **special character? meh...**".format(message))
                #elif "\u200b" in message.content.lower():
                    #if enabled:
                       #await self.bot.delete_message(message)
                       #await self.bot.send_message(message.channel, "boobot?")
                #elif "enter the code" in message.content.lower():
                    #if enabled:
                        #await self.bot.delete_message(message)
                        #await self.bot.send_message(message.channel, "{0.author.mention} **cant hide (;**".format(message))

    async def on_message(self, message):
        timestamp = datetime.now().timestamp()
        author = message.author.display_name

        # don't detect bot messages as spam
        if message.author.id == self.bot.user.id:
            return

        # if it's the user's first message, add a timestamp
        # otherwise if we have an entry for the user, merge the new message
        role = self.role_name

        if not self.message_history:
            self.message_history[author] = [timestamp]
        elif not author in self.message_history:
            self.message_history[author] = [timestamp]
        else:
            self.message_history[author] = self.message_history[author] + [timestamp]
            is_spam = self.check_for_spam(author)
            if is_spam:
                self.shitlist.append(author)
                self.message_history[author] = []
                self.spam_levels[author] = 1
                try:
                    await self.bot.add_roles(user, role)
                    m = "ads detected from " + author + ". Silencing this filthy peasant."
                    await self.bot.send_message(message.channel, m)
                except discord.errors.Forbidden:
                    pass
                    #await self.bot.send_message(message.channel, "I'm not allowed to do that.")

    def check_for_spam(self, author):
        message_timestamps = self.message_history[author]
        num_messages = len(message_timestamps)

        print("num messages =", num_messages)

        # if they haven't sent enough messages total to be considered spam,
        # we can stop right here
        if num_messages < self.RX_MESSAGE_THRESHOLD:
            return

        # compare self.RX_MESSAGE_THRESHOLD total messages from the message history
        # if enough flags found for RX Messages (sent too fast), globally
        # mute the user for 5 minutes.
        if author in self.spam_levels:
            spamlevel = self.spam_levels[author]
        else:
            spamlevel = 1

        print("num messages = ", num_messages)
        print("spam level = ", spamlevel)

        for i in range (0, num_messages-1,1):
            try:
                if message_timestamps[i+1] - message_timestamps[i] <= self.RX_MESSAGE_DELTA_THRESHOLD:
                    spamlevel += 1
            except:
                pass

        self.spam_levels[author] = spamlevel

        if self.spam_levels[author] >= self.RX_MESSAGE_THRESHOLD:
            message = "spam detected from [" + author + "], spamlevel=" + str(spamlevel)
            print(message)
            return True

        return False                                    

def check_folders():
    if not os.path.exists("data/noads"):
        print("Creating noads folder...")
        os.makedirs("data/noads")


def check_files(bot):
    settings = {"ENABLED" : False}
    settings_path = "data/noads/settings.json"

    if not os.path.isfile(settings_path):
        print("Creating default noads settings.json...")
        fileIO(settings_path, "save", settings)

def setup(bot):
    check_folders()
    check_files(bot)
    n = Noads(bot)
    bot.add_listener(n.check_noads, "on_message")
    bot.add_cog(n)
