from __main__ import send_cmd_help
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils import chat_formatting
import subprocess
import sys


class HelpfulUtils:
    def __init__(self, bot):
        self.bot = bot
        self.version = "2016-08-31 v.1"

    @checks.is_owner()
    @commands.group(name="utils", pass_context=True, invoke_without_command=True)
    async def group_cmd(self, ctx):
        """A bunch of useful commands all in one!"""
        await send_cmd_help(ctx)

    @checks.is_owner()
    @group_cmd.command(name="listcogs")
    async def list_cogs(self):
        """A command to list the currently active cogs."""
        cogs = dataIO.load_json("data/red/cogs.json")

        # So IDEA shuts up:
        # noinspection PyProtectedMember
        existing_cogs = self.bot.cogs['Owner']._list_cogs()
        enabled_cogs = []
        disabled_cogs = []

        for cog in cogs:
            if cogs.get(cog) and cog in existing_cogs:
                enabled_cogs.append(cog)
            elif cog in existing_cogs:
                disabled_cogs.append(cog)

        enabled_str = "Enabled cogs:"

        for cog in sorted(enabled_cogs):
            enabled_str = enabled_str + "\n+ " + str(cog)

        disabled_str = "Disabled cogs:"

        for cog in sorted(disabled_cogs):
            disabled_str = disabled_str + "\n- " + str(cog)

        assembled_str = "```diff\n" + enabled_str + "\n\n" + disabled_str + "```"

        await self.bot.say(assembled_str)

    @checks.is_owner()
    @group_cmd.command()
    async def update(self, hard: bool=False):
        """Update the bot. Defaults to regular git pull."""
        if sys.platform == "linux":
            if not hard:
                command = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
                output = command.stdout.read().decode()
                await self.bot.say("```" + output + "```")
                if "Already up-to-date." not in output:
                    await self.bot.say("I recommend restarting your bot now to apply the changes.")
            else:
                command = subprocess.Popen(["git", "fetch --force"], stdout=subprocess.PIPE)
                output = command.stdout.read().decode()
                await self.bot.say("```" + output + "```")
                command = subprocess.Popen(["git", "reset --hard"], stdout=subprocess.PIPE)
                output = command.stdout.read().decode()
                await self.bot.say("```" + output + "```")
                command = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
                output = command.stdout.read().decode()
                await self.bot.say("```" + str(output) + "```")
        else:
            await self.bot.say("Incompatible OS. This usually means you are running Windows, which does not allow "
                               "for files to be changed while they are open.")

    @checks.is_owner()
    @group_cmd.command()
    async def terminal(self, *, command: str=None):
        """Run a terminal command."""
        if command is not None:
            command = command.split()
            command_run = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = command_run.stdout.read().decode()
            paged = chat_formatting.pagify(output, delims="\n")
            for page in paged:
                await self.bot.say("```{0}```".format(page))
        else:
            await self.bot.say("You *do* realize you need to enter a command, right?")

    @checks.is_owner()
    @group_cmd.command(name="listprefixes")
    async def list_prefixes(self):
        """List the bot's prefixes."""
        prefixes = ""
        for i in self.bot.command_prefix:
            prefixes += "\"" + i + "\" "
        await self.bot.say("My current prefixes: {0}".format(prefixes))

    @checks.is_owner()
    @group_cmd.command(name="version")
    async def version_cmd(self):
        """Check the helpful utils version."""
        await self.bot.say("I am currently running helpful utils version {0}.".format(self.version))


def setup(bot):
    n = HelpfulUtils(bot)
    bot.add_cog(n)
