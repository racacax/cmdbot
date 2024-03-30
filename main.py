import os

import discord
from discord.ext import commands

from bot import CMDBot
from commands_manager import register_commands
from settings import DISCORD_TOKEN

intents = discord.Intents._from_value(3276543)
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = CMDBot(intents=intents)
register_commands(bot)
bot.run(DISCORD_TOKEN)
