import discord
import os
import re
import logging
from discord.ext import commands as discord_commands
from discord.ext import tasks
from settings import Settings

settings = Settings('settings.json')
intents = discord.Intents.default()
intents.members = True

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
    pass
    # TODO: Do stuff

@tasks.loop(seconds=120, reconnect=True)
async def check_ping():
    pass
    # TODO: Do stuff

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