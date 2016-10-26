# import discord
from discord.ext import commands
from .utils import checks
from .utils.dataIO import fileIO
import os


class Afk:
    """Le afk cog"""
    def __init__(self, bot):
        self.bot = bot
        self.afk_data = 'data/afk/afk.json'

    async def listener(self, message):
        tmp = {}
        for mention in message.mentions:
            tmp[mention] = True
        if message.author.id != self.bot.user.id:
            data = fileIO(self.afk_data, 'load')
            for mention in tmp:
                if mention.mention in data:
                    if data[mention.mention]['MESSAGE'] is True:
                        msg = '{} is currently afk.'.format(mention.name)
                    else:
                        msg = '{} is currently afk, Message: ** {} **'.format(mention.name, data[mention.mention]['MESSAGE'])
                    await self.bot.send_message(message.channel, msg)

    async def autoafk(self, message):
        if message.author.id != self.bot.user.id:
            data = fileIO(self.afk_data, 'load')
            for author_mention in data:
                del data[author_mention]
                msg = 'You\'ew now back, removed you from afk.'



    @commands.command(pass_context=True, name="afk")
    @checks.mod_or_permissions(manage_messages=True)
    async def _afk(self, context, *message: str):
        """Tell the bot you're afk or online."""
        data = fileIO(self.afk_data, 'load')
        author_mention = context.message.author.mention
        if author_mention in data:
            del data[author_mention]
            msg = 'You\'re now back.'
        else:
            data[context.message.author.mention] = {}
            if message:
                data[context.message.author.mention]['MESSAGE'] = " ".join(context.message.clean_content.split()[1:])
                if len(str(message)) > 200:
                	await self.bot.say('**200 characters max**. Try again.')
                	return
            else:
                data[context.message.author.mention]['MESSAGE'] = True
            msg = 'You\'re now set as afk.'
        fileIO(self.afk_data, 'save', data)
        await self.bot.say(msg)


def check_folder():
    if not os.path.exists('data/afk'):
        print('Creating data/afk folder...')
        os.makedirs('data/afk')


def check_file():
    afk = {}
    f = 'data/afk/afk.json'
    if not fileIO(f, 'check'):
        print('Creating default afk.json...')
        fileIO(f, 'save', afk)


def setup(bot):
    check_folder()
    check_file()
    n = Afk(bot)
    bot.add_listener(n.listener, 'on_message')
    bot.add_listener(n.autoafk, 'on_message')
    bot.add_cog(n)
