import datetime
from typing import Union

import discord
import peewee
from discord.abc import GuildChannel
from peewee import Model, BigIntegerField, CharField, IntegerField, ForeignKeyField, TextField, BooleanField, \
    DateTimeField, DateField, ManyToManyField

from settings import db


class BaseModel(Model):
    class Meta:
        database = db


class Command(BaseModel):
    guild_id = BigIntegerField()
    channel_ids = TextField(default="")
    command = CharField()
    response = TextField()

    def __str__(self):
        return f"{self.id}) {self.command}"