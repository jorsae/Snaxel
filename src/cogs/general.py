import discord
from peewee import *
from discord.ext import commands
from datetime import datetime
import math
import time
import logging

import constants
import utility

class General(commands.Cog):
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
    
    @commands.command(name='mvp', aliases=['mvps'], help=f'mvp list')
    async def mvp(self, ctx):
        embed = discord.Embed(colour=constants.COLOUR_NEUTRAL)
        embed.set_author(name=f'MVP times')
        
        index = 0
        for mvp in self.settings.mvps:
            index += 1
            embed.add_field(name=f'{index}. {mvp.location}', value=f'<t:{int(mvp.dt.timestamp())}>', inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='ping', help="Checks the bot's latency")
    async def ping(self, ctx):
        start = time.monotonic()
        message = await ctx.send('Pong!')
        ping = (time.monotonic() - start) * 1000
        await message.edit(content=f'Pong! {int(ping)} ms')

    @commands.command(name='help', help='Displays this help message')
    async def help(self, ctx):
        author = ctx.message.author
        
        cogs = []
        cogs.append(self.bot.get_cog('General'))
        cogs.append(self.bot.get_cog('Admin'))

        embed = discord.Embed(colour=constants.COLOUR_NEUTRAL)
        embed.set_author(name=f'Help')
        for cog in cogs:
            for command in cog.walk_commands():
                if await command.can_run(ctx):
                    embed.add_field(name=f'.{command}{utility.get_aliases(command.aliases)}', value=command.help, inline=False)
        await ctx.send(embed=embed)