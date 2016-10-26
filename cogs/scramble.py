from random import randint,sample
import asyncio
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
from discord.errors import *
import time
import aiohttp
import sys
import random
import os

class Scramble():
	"""Scamble game"""
	def __init__(self,bot):
		self.bot = bot
		self.scramble_sessions = []
		self.settings = fileIO("data/scramble/settings.json", "load")
			
	@commands.command(pass_context=True)
	async def scramble(self, ctx):
		"""Scramble game! """
		with open("data/scramble/5 letter words.txt", "r") as f:
			data = f.read()
		data = data.split("\n")
		i = randint(1, 2)
		word = data[i-1]
		print(word)
		scrambled = sample(word, len(word))
		scrambled = ''.join(scrambled)
		await self.bot.say("The word scramble is: {}!".format(scrambled))
		await self.bot.wait_for_message(content=word)
		await self.bot.say("Nice job! You solved the scramble")

def check_folders():
	if not os.path.exists("data/scramble"):
		print("Creating scramble folder...")
		os.makedirs("data/noads")

def check_files(bot):
	settings = {"ENABLED" : True}
	settings_path = "data/scramble/settings.json"

	if not os.path.isfile(settings_path):
	 	print("creating default scramble settings.json...")
	 	fileIO(settings_path, "save", settings)

def setup(bot):
	check_folders()
	check_files(bot)
	bot.add_cog(Scramble(bot))

