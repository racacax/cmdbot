import asyncio
from abc import ABC

import discord

from models import Command
from settings import db
from utils import  Emoji


class CMDBot(discord.Bot, ABC):

    async def on_ready(self):
        activity = discord.Game(name="Créé par racacax")

        await self.change_presence(status=discord.Status.do_not_disturb, activity=activity)
        print(f'We have logged in as {self.user}')

        async def keep_alive():
            while True:
                try:
                    print("keep alive sql connection")
                    print(Command.get_or_none(id=0))
                except Exception as e2:
                    print(e2)
                await asyncio.sleep(3600)

        loop = asyncio.get_event_loop()
        task = loop.create_task(keep_alive())

    async def on_guild_join(self, guild: discord.Guild):
        pass

    @db.atomic()
    async def on_message(self, message: discord.Message):
        if message.guild is None:
            return
        if message.content.startswith("$"):
            commands = Command.select().where(
                Command.channel_ids.contains(f"{message.channel.id}") | Command.channel_ids.__eq__(""),
                Command.guild_id.__eq__(message.guild.id),
                Command.command.__eq__(message.content[1:]))
            for command in commands: # multiple triggers are possible
                await message.channel.send(command.response)

    async def on_raw_message_delete(self, payload):
        # NotYetUseful
        pass
