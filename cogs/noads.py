import discord
from discord.ext import commands
import os
from .utils.dataIO import fileIO
from .utils import checks

default_settings = {"SERVER": {"DEFAULT": False}}

class Noads:
    """Deletes discord invite links, disabled by default."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/noads/settings.json", "load")

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
