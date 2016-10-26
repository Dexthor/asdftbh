import discord
from discord.ext import commands
from .utils import checks
import asyncio
import logging

log = logging.getLogger("red.move")

class Move:
    """Moves users to another voice channel"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(no_pm=True, pass_context=True) 
    @checks.admin_or_permissions(manage_channels=True)
    async def move(self, ctx, voicechannel: discord.Channel, *user: discord.Member):
        """Moves a bunch of users to another voice channel 
        Need to maintain Capitalization
        Channel name must be in quotes if there are spaces.
        You need the admin role '!' to execute this command"""        
        author = ctx.message.author
        server = ctx.message.server
        try:
            for user in ctx.message.mentions:
                await self.bot.move_member(user, voicechannel)
        except discord.Forbidden:
            await self.bot.say("I do not have permission to move members to voice channels ):")
        except discord.InvalidArgument:
            await self.bot.say("Channel must be a Voice Channel and not a Text Channel")
        except discord.HTTPException:
            await self.bot.say("An Error Occured. Couldn't move the member to the Voice Channel")
        else:
            memberlist = " , ".join(m.display_name for m in ctx.message.mentions)
            await self.bot.say('Moved **{0}** to `{1}`'.format(memberlist, voicechannel))          

def setup(bot):
    n = Move(bot)
    bot.add_cog(n)
