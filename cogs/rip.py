import discord
from discord.ext import commands

class Other:
    """Rip"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def rip(self, ctx, name=None):
        """rip you"""

        server = ctx.message.server
		
        if name:
            name = name.strip()
            if "ripme.xyz/" not in name:
                name = "http://ripme.xyz/" + name
            await self.bot.say("**" + name + "**")
            

def setup(bot):
    bot.add_cog(Other(bot))
