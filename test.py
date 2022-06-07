import discord
from discord.ext import commands, tasks
import config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix= config.prefix, description='Relatively simple BOT', intents = intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    
bot.run(config.token)