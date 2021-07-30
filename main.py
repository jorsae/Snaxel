import discord
import os
import re
import logging
import string
from datetime import datetime, timedelta
from discord.ext import commands as discord_commands
from discord.ext import tasks
from settings import Settings

settings = Settings('settings.json')

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

    await process_times(message)

async def process_times(message):
    content = message.content.lower()
    location = ''
    for line in content.split('\n'):
        if line.startswith('ch'):
            loc = get_location(line)
            if loc is not None:
                location = loc
                print(location)
        else:
            time = get_time(line)

def get_location(line):
    return re.search(r'.+ •', line).group()[:-2]

def get_time(line):
    if 'local time' in line:
        now = datetime.now()
        
        hours = int(re.search(r'\d+:', line).group()[:-1])
        mins = int(re.search(r':\d+', line).group()[1:])
        d = datetime(now.year, now.month, now.day, hours, mins, 0, 0)

        if now > d:
            d = d + timedelta(days=1)
        return d
    else:
        print('NO local time')
        print(line)

@tasks.loop(seconds=120, reconnect=True)
async def check_ping():
    pass # TODO: Do stuff

@bot.event
async def on_ready():
    check_ping.start()

def setup_logging():
    logFolder = 'logs'
    logFile = 'snaxel.log'
    if not os.path.isdir(logFolder):
        os.makedirs(logFolder)
    handler = logging.FileHandler(filename=f'{logFolder}/{logFile}', encoding='utf-8', mode='a+')
    logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s %(levelname)s:[%(filename)s:%(lineno)d] %(message)s')

if __name__ == '__main__':
    setup_logging()
    settings.parse_settings()
    print('running')
    print(settings.token)

    bot.run(settings.token)