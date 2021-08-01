import discord
from peewee import *
from discord.ext import commands, flags
from datetime import datetime
import math
import time
import logging

class General(commands.Cog):
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
    
    @commands.command(name='mvp', help=f'mvp list')
    async def mvp(self, ctx):
        out = ''
        index = 0

        if len(self.settings.mvps) <= 0:
            await ctx.send('No times')
            return
        
        for mvp in self.settings.mvps:
            index += 1
            out += f'{index}. {str(mvp)}\n'
        
        await ctx.send(out)

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
        # cogs.append(self.bot.get_cog('Ranking'))
        cogs.append(self.bot.get_cog('General'))
        # cogs.append(self.bot.get_cog('Admin'))

        embed = discord.Embed(colour=constants.COLOUR_NEUTRAL)
        embed.set_author(name=f'BMW Help')
        for cog in cogs:
            for command in cog.walk_commands():
                if await command.can_run(ctx):
                    embed.add_field(name=f'{self.settings.prefix}{command}{utility.get_aliases(command.aliases)}', value=command.help, inline=False)
        await ctx.send(embed=embed)