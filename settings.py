import os

from peewee import *
from dotenv import load_dotenv
from playhouse.shortcuts import ReconnectMixin

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

DATABASE_NAME = os.getenv("DATABASE_NAME", "cmdbot")
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "doweneedpasswordindocker")
DATABASE_HOST = os.getenv("DATABASE_HOST", "db")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 3306))


class ReconnectMySQLDatabase(ReconnectMixin, MySQLDatabase):
    pass


db = ReconnectMySQLDatabase(DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD,
                            host=DATABASE_HOST, port=DATABASE_PORT)
