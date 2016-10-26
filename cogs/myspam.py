import discord
from discord.ext import commands
from .utils import checks

#weird lil spam script of dex

class Spam:
    """Spams users dm 10 timessss"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def spam(self, ctx, User : discord.Member):
        """Spams users dm 10 times"""

        #I am new to this Shit!!
        for x in range(0,10):

        	await self.bot.send_message(User,"(づ⚆v⚆)づ **SPAM BOMBS** (づ⚆v⚆)づ by" +ctx.message.author.mention)

def setup(bot):
    bot.add_cog(Spam(bot))
