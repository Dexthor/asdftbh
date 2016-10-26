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
        You need the admin role '!' to execute this command
        -alan hi tnx bai"""        
        author = ctx.message.author    
        server = ctx.message.server  
        voicechannel = voicechannel.tolower()     
        if not voicechannel.permissions_for(server.me).move_members:    
            await self.bot.say("I don't have move members permission or That room is locked for me.")    
            return
        if voicechannel is None:    
            await self.bot.say('That channel cannot be found.')    
            return
        for user in ctx.message.mentions:
            await self.bot.move_member(user, voicechannel)
        memberlist = " , ".join(m.display_name for m in ctx.message.mentions)
        await self.bot.say('Moved **{0}** to `{1}`'.format(memberlist, voicechannel))          

def setup(bot):
    n = Move(bot)
    bot.add_cog(n)
