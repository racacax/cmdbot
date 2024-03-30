import re

import discord
from discord import Option
from discord.ext.commands import has_permissions

from bot import CMDBot
from models import Command
from settings import db
from utils import Emoji, PageView


def register_cc_commands(bot: CMDBot):
    from commands_manager import exception_decorator, CMDApplicationContext
    cc = bot.create_group(
        name="cc", description="Commandes liées aux commandes personnalisées"
    )

    async def get_list_from_db(ctx: discord.AutocompleteContext):
        return sorted([e.__str__() for e in Command.filter(guild_id=ctx.interaction.guild_id)])


    @cc.command(description="Ajouter ou mettre à jour une commande", name="set")
    @has_permissions(administrator=True)
    @exception_decorator()
    async def set_(ctx: CMDApplicationContext, trigger: str,
                   message: str, channels: Option(str,
                                                  "Salons (#salon1 #salon2 ...). Discord propose les salons quand on met un #",
                                                  required=False), existing_command: Option(str, "Commande existante (pour la modifier)",
                                                                 autocomplete=get_list_from_db, required=False)):

        m = re.finditer('<#(.*?)>', channels or "")
        channel_ids = [a.group(1) for a in m]
        channel_ids = ",".join(channel_ids)
        if not existing_command:
            Command.create(command=trigger, guild_id=ctx.guild_id, channel_ids=channel_ids, response=message)
            message = "Commande créée avec succès"
        else:
            id = int(existing_command.split(")")[0])
            command = Command.get_or_none(guild_id=ctx.guild_id, id=id)
            command.command = trigger
            command.message = message
            command.channel_ids = channel_ids
            command.save()
            message = f"Commande {id} modifiée avec succès"

        await ctx.current_interaction.edit_original_response(content=message)

    @cc.command(description="Supprimer une commande")
    @has_permissions(administrator=True)
    @exception_decorator()
    async def delete(ctx: CMDApplicationContext, command: Option(str, "Commande",
                                                                 autocomplete=get_list_from_db)):
        id = int(command.split(")")[0])
        command = Command.get_or_none(guild_id=ctx.guild_id, id=id)
        if command:
            command.delete_instance()
            message = f"Commande n°{id} supprimée avec succès"
        else:
            message = f"La commande n°{id} n'existe pas"
        await ctx.current_interaction.edit_original_response(content=message)

    @cc.command(description="Afficher la liste des commandes", name="list")
    @has_permissions(administrator=True)
    @exception_decorator()
    async def list_(ctx: CMDApplicationContext, page: Option(int, default=1, required=False)):
        async def callback_fn(page: int, view):
            commands = Command.filter(guild_id=ctx.guild_id).count()
            embed = discord.Embed(title="Commandes")
            for c in Command.filter(guild_id=ctx.guild_id)[(page - 1) * 10:page * 10]:
                embed.add_field(name=f"{c.id}) ${c.command}", value=','.join(
                    [f'<#{ch}>' if ch != '' else '**TOUS**' for ch in c.channel_ids.split(',')]), inline=False)

            embed.add_field(name="Commandes",
                            value=f"n°{1 + (page - 1) * 10} à {min(page * 10, commands)} sur {commands}", inline=False)
            await ctx.current_interaction.edit_original_response(embed=embed, content="", view=view)

        await callback_fn(page, PageView(page, callback_fn))

