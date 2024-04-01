import datetime
import functools
from io import StringIO

import discord
from discord import ApplicationContext, File

from bot import CMDBot
from commands.cc import register_cc_commands
from settings import db
from utils import whitelisted, Emoji
import traceback


class CMDApplicationContext(ApplicationContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_interaction: discord.Interaction | None = None


LOADING_STR = f"{Emoji.OWOWIGGLE} Chargement en cours... {Emoji.OWOWIGGLE}"


# Permet de catch toutes les exceptions et de les logger

def exception_decorator(ephemeral=False):
    def inner(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            message: discord.Interaction | None = None
            ctx: CMDApplicationContext = args[0]
            if ctx.guild_id is None:
                await ctx.respond("Le bot CMD ne peut que être utilisé sur serveur, pas en MP "
                                  f"{Emoji.DINKDONK}.")
                return
            try:
                message = await ctx.respond(LOADING_STR, ephemeral=ephemeral)
                ctx.current_interaction = message
                db.reconnect_if_lost()
                with db.atomic():
                    return await func(*args, **kwargs)
            except Exception as e:
                traceback.print_exc()
                msg_content = f"Une erreur inconnue est survenue {Emoji.NOOOO} !"
                if message:
                    await message.edit_original_response(content=msg_content)
                else:
                    await ctx.channel.send(content=msg_content)

        return wrapped

    return inner


def register_commands(bot: CMDBot):
    register_cc_commands(bot)
