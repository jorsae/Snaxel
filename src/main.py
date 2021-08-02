import discord
import os
import re
import logging
from datetime import datetime, timedelta
from discord.ext import commands as discord_commands
from discord.ext import tasks

import constants
import utility
import cogs
from settings import Settings
from mvp import MVP

settings = Settings('../settings.json')

bot = discord_commands.Bot(command_prefix='.')
bot.remove_command('help')

@bot.event
async def on_message(message: discord.Message):
    await bot.wait_until_ready()
    message.content = (
        message.content
        .replace("—", "--")
        .replace("'", "′")
        .replace("‘", "′")
        .replace("’", "′")
    )
    if message.author.id == settings.bot_id:
        return

    await bot.process_commands(message)
    
    if message.channel.id == settings.mvp_channel:
        if message.author.id in settings.admin:
            mvps = await process_times(message)
            if len(mvps) <= 0:
                await message.channel.send("No MVP times added")
                logging.warning(f'[{message.author}]No MVP times added: {message.content}')
                return
    
            m = ''
            for mvp in mvps:
                m += f'{str(mvp)}\n'
                settings.mvps.append(mvp)
            
            logging.info(f'[{message.author}] MVP times added: {len(mvps)}/{len(settings.mvps)}')
            await message.channel.send(m)

async def process_times(message):
    content = message.content.lower()
    mvps = []
    location = None
    for line in content.split('\n'):
        if line.startswith('ch'):
            loc = get_location(line)
            if loc is not None:
                location = loc
        else:
            time = get_time(line)
            if location is not None and time is not None:
                mvps.append(MVP(location, time))
    return mvps

def get_location(line):
    try:
        return re.search(r'.+ •', line).group()[:-2]
    except Exception as e:
        logging.error(e)
        return None

def get_time(line):
    try:
        now = datetime.now()
        if 'local time' not in line:
            line = re.search(r'cest - .+ ae[s|d]t', line).group()[7:-5]
        
        hours = int(re.search(r'\d+:', line).group()[:-1])
        mins = int(re.search(r':\d+', line).group()[1:])
        if 'pm' in line:
            hours += 12
        d = datetime(now.year, now.month, now.day, hours, mins, 0, 0)

        if now > d:
            d = d + timedelta(days=1)
        return d
    except Exception as e:
        logging.error(e)
        return None

@tasks.loop(seconds=10, reconnect=True)
async def check_ping():
    now = datetime.now()
    for mvp in settings.mvps:
        total = (mvp.dt - now).total_seconds()
        if total <= constants.WARNING_TIME:
            ch = bot.get_channel(settings.ping_channel)
            time_left = mvp.dt - now
            await ch.send(f'mvp in {utility.format_timedelta(time_left)}: {mvp.location}')
            settings.mvps.remove(mvp)

@bot.event
async def on_ready():
    check_ping.start()

def setup_logging():
    logFolder = '../logs'
    logFile = 'snaxel.log'
    if not os.path.isdir(logFolder):
        os.makedirs(logFolder)
    handler = logging.FileHandler(filename=f'{logFolder}/{logFile}', encoding='utf-8', mode='a+')
    logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s %(levelname)s:[%(filename)s:%(lineno)d] %(message)s')

if __name__ == '__main__':
    setup_logging()
    settings.parse_settings()
    print('running')

    bot.add_cog(cogs.General(bot, settings))
    bot.add_cog(cogs.Admin(bot, settings))

    bot.run(settings.token)