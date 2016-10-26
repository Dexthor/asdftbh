import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from .utils.dataIO import fileIO
from __main__ import send_cmd_help
from discord.ext import commands
import asyncio

import calendar
import discord
import time
import os
import numpy as np

cog_name = 'activity'
data_name = 'activity'

class Activity:
	def __init__(self, bot):
		self.bot = bot

	async def listener(self, message):
		if not message.channel.is_private and self.bot.user.id != message.author.id:
			author = message.author
			server = message.server
			timestamp = message.timestamp
			file_name = 'data/{}/{}.json'.format(cog_name, author.id)
			if not fileIO(file_name, 'check'):
				data = {}
				data['HOUR'] = {}
				for i in range(1, 25):
					data['HOUR'][str(i)] = 0
				fileIO(file_name, 'save', data)
			else:
				data = fileIO(file_name, 'load')
			if str(timestamp.year) not in data:
				data[str(timestamp.year)] = {}
				for i in range(1, 13):
					data[str(timestamp.year)][str(i)] = 0
			data['HOUR'][str(timestamp.hour)] += 1
			data[str(timestamp.year)][str(timestamp.month)] += 1
			fileIO(file_name, 'save', data)

	@commands.group(pass_context=True, no_pm=True, name='activity', aliases=['ac'])
	async def _activity(self, context):
		if context.invoked_subcommand is None:
			await send_cmd_help(context)

	@_activity.command(pass_context = True, name='hour', aliases=['hr'])
	async def _hour(self, context, username: discord.Member):
		server = context.message.server
		author = username
		file_name = 'data/{}/{}.json'.format(cog_name, author.id)
		if not fileIO(file_name, 'check'):
			message = 'Who?'
		else:
			data = fileIO(file_name, 'load')
			t = str(time.time())
			hours = [int(hours) for hours in data['HOUR']]
			messages = [message for message in data['HOUR'].values()]

			plt.bar(hours, messages, width=1.0, facecolor='black', edgecolor='black', align='center')
			plt.title('Hourly activity of {} - Total Messages: {}'.format(username.display_name, sum(messages)), y=1.04)
			plt.xlabel('Hour (UTC)')
			plt.xticks(np.arange(24))
			plt.yticks([])
			plt.xlim([0,23])
			plt.savefig('{}.png'.format(t))
			plt.clf()
			try:
				await self.bot.send_file(context.message.channel, '{}.png'.format(t))
			except discord.Forbidden:
				await self.bot.say('I don\'t have any permissions to attach files!')
			os.remove('{}.png'.format(t))

	@_activity.command(pass_context = True, name='year', aliases=['yr'])
	async def _year(self, context, year: str, username: discord.Member):
		server = context.message.server
		author = context.message.author
		file_name = 'data/{}/{}.json'.format(cog_name, author.id)
		if not fileIO(file_name, 'check'):
			message = 'Who?'
		else:
			data = fileIO(file_name, 'load')
			if year in data:
				t = str(time.time())
				months = [int(months) for months in data[year]]
				messages = [message for message in data[year].values()]
				plt.bar(months, messages, width=1.0, facecolor='black', edgecolor='black', align='center')
				plt.title('Monthly activity of {} for {}'.format(username.display_name, server.name, str(year)), y=1.04)
				plt.ylabel('Messages')
				plt.xlabel('Total Messages: {}'.format(sum(messages)))
				plt.xticks(np.arange(13), calendar.month_abbr[0:13])
				plt.xlim([1,12])
				plt.yticks([])
				plt.savefig('{}.png'.format(t))
				plt.autoscale(enable=False, axis="x")
				plt.clf()
				try:
					await self.bot.send_file(context.message.channel, '{}.png'.format(t))
				except discord.Forbidden:
					await self.bot.say('I don\'t have any permissions to attach files!')
				os.remove('{}.png'.format(t))

def check_folder():
	if not os.path.exists('data/{}'.format(cog_name)):
		print('Creating data/{}'.format(cog_name))
		os.makedirs('data/{}'.format(cog_name))

def setup(bot):
	check_folder()
	n = Activity(bot)
	bot.add_listener(n.listener, 'on_message')
	bot.add_cog(n)
