import functools
import logging
from datetime import datetime
from enum import Enum
from typing import Optional

import discord
from discord import VoiceClient, ApplicationContext
from discord.ui import Item


def whitelisted(function):
    @functools.wraps(function)
    async def wrapper(ctx: ApplicationContext, *args, **kwargs):
        pass

    return wrapper


class Emoji:
    BEN = "<:ben:1196941108631056545>"
    ALERT = "<a:ALERT:1198969863125872640>"
    XDDDINKDONK = "<a:xddDinkDonk:1198608299495526520>"
    STARE = "<:stare:1129034123638476810>"
    PEPEPOINT = "<:PepePoint:1196957325827784805>"
    YEK = "<:YEK:1198608508757745694>"
    OWO = "<:owo:1198627822290345984>"
    OKAYGEBUSINESS = "<:OkaygeBusiness:1198631447104335872>"
    SADCATCRYING = '<:SadCatCrying:1157472413173415966>'
    DINKDONK = '<a:dinkDonk:1198613866951753778>'
    OWOWIGGLE = "<a:owoWiggle:1193246031282974740>"
    NOOOO = "<a:NOOOOO:1136430908342272000>"


class ConfirmDeleteView(discord.ui.View):
    def __init__(self, delete_fn, *items: Item):
        super().__init__(*items)
        self.delete_fn = delete_fn

    @discord.ui.button(label="Oui", style=discord.ButtonStyle.danger)
    async def delete_callback(self, button, interaction):
        await self.delete_fn()

    @discord.ui.button(label="Non", style=discord.ButtonStyle.primary)
    async def cancel_callback(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(content="La suppression a été annulée.", view=discord.ui.View())


class PageView(discord.ui.View):
    def __init__(self, current_page, callback_fn, *items: Item):
        super().__init__(*items)
        self.current_page = current_page
        self.callback_fn = callback_fn

    @discord.ui.button(label="⏮️ Précédent", style=discord.ButtonStyle.primary)
    async def previous_callback(self, button, interaction):
        if self.current_page > 1:
            self.current_page -= 1
        await interaction.response.edit_message(view=self)
        await self.callback_fn(self.current_page, self)

    @discord.ui.button(label="Suivant ⏭️", style=discord.ButtonStyle.primary)
    async def next_callback(self, button, interaction: discord.Interaction):
        self.current_page += 1
        await interaction.response.edit_message(view=self)
        await self.callback_fn(self.current_page, self)
