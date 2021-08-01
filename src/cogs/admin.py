import discord
import logging
from datetime import datetime, date, timedelta
from discord.ext import commands, flags

import constants

class Admin(commands.Cog):
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
    
    def is_admin():
        def predicate(ctx):
            return ctx.message.author.id in constants.ADMIN_LIST
        return commands.check(predicate)
    
    @commands.command(name='delmvp', help=f'Delete mvp time')
    @is_admin()
    async def del_mvp(self, ctx, index: int):
        # print(f'del_mvp: {index} | {len(self.settings.mvps)}')
        count = 0
        for mvp in self.settings.mvps:
            count += 1
            if count == index:
                self.settings.mvps.remove(mvp)
                await ctx.channel.send(f'deleted: {mvp}')