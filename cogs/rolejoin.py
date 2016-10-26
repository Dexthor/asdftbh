import discord
from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks
import os

JSON = 'data/rolejoin/settings.json'


class RoleJoin:

    def __init__(self, bot):
        self.bot = bot
        self.role_name = 'Pedestrian'
        self.settings = dataIO.load_json(JSON)

    @checks.admin_or_permissions(manage_server=True)
    @commands.command(pass_context=True, no_pm=True)
    async def rolejoin(self, ctx):
        server = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = False
        self.settings[server.id] = not self.settings[server.id]
        if self.settings[server.id]:
            await self.bot.say("%s role will be added to new members."
                               % self.role_name)
        else:
            await self.bot.say("%s role won't be added to new members."
                               % self.role_name)
        dataIO.save_json(JSON, self.settings)

    async def on_member_join(self, member):
        server = member.server
        if server.id not in self.settings:
            self.settings[server.id] = False
            dataIO.save_json(JSON, self.settings)
        if not self.settings[server.id]:
            return
        else:
            role = discord.utils.get(server.roles, name=self.role_name)
            if role:
                await self.bot.add_roles(member, role)


def check_folders():
    dirname = os.path.dirname(JSON)
    if not os.path.exists(dirname):
        print("Creating rolejoin data folder...")
        os.makedirs(dirname)


def check_files():
    if not dataIO.is_valid_json(JSON):
        print("Creating rolejoin settings.json...")
        dataIO.save_json(JSON, {})


def setup(bot):
    check_folders()
    check_files()
    n = RoleJoin(bot)
    bot.add_cog(n)
