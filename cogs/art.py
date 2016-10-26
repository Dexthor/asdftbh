from discord.ext import commands
from cogs.utils.chat_formatting import box

try:
    from pyfiglet import figlet_format
except:
    figlet_format = None


class art(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="art")
    async def _art(self, *, text):
        msg = str(figlet_format(text, font='standard'))
        if msg[0] == " ":
            msg = "." + msg[1:]
        error = figlet_format('LOL, that\'s a bit too long.',
                              font='standard')
        if len(msg) > 2000:
            await self.bot.say(box(error))
        else:
            await self.bot.say(box(msg, lang="fix"))


def setup(bot):
    if figlet_format is None:
        raise NameError("You need to run `pip3 install pyfiglet`")
    n = art(bot)
    bot.add_cog(n)
