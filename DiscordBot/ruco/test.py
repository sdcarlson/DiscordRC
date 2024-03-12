import asyncio
import os
import json
import discord
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from discord.ext import commands
# from ruco.read import Read
# from ruco.write import Write
# from ruco.permissions import Channel, is_text_based_ch
# from ruco.permissions import get_ch_type_from_str, get_ch_type_from_ch
# from ruco.permissions import \
#     role_perm_names, set_role_perm, \
#     cat_perm_names, set_cat_perm_overwrite, \
#     text_ch_perm_names, set_text_ch_perm_overwrite, \
#     voice_ch_perm_names, set_voice_ch_perm_overwrite, \
#     forum_ch_perm_names, set_forum_ch_perm_overwrite, \
#     announcement_ch_perm_names, set_announcement_ch_perm_overwrite, \
#     stage_ch_perm_names, set_stage_ch_perm_overwrite, \
#     rules_ch_perm_names, set_rules_ch_perm_overwrite, \
#     updates_ch_perm_names, set_updates_ch_perm_overwrite
from DiscordBot.ruco.read import Read
from DiscordBot.ruco.write import Write
from DiscordBot.ruco.permissions import Channel, is_text_based_ch
from DiscordBot.ruco.permissions import get_ch_type_from_str, get_ch_type_from_ch
from DiscordBot.ruco.permissions import \
    role_perm_names, set_role_perm, \
    cat_perm_names, set_cat_perm_overwrite, \
    text_ch_perm_names, set_text_ch_perm_overwrite, \
    voice_ch_perm_names, set_voice_ch_perm_overwrite, \
    forum_ch_perm_names, set_forum_ch_perm_overwrite, \
    announcement_ch_perm_names, set_announcement_ch_perm_overwrite, \
    stage_ch_perm_names, set_stage_ch_perm_overwrite, \
    rules_ch_perm_names, set_rules_ch_perm_overwrite, \
    updates_ch_perm_names, set_updates_ch_perm_overwrite


class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.read = self.bot.get_cog('Read')
        self.write = self.bot.get_cog('Write')

    @commands.command()
    async def clear(self, ctx):
        '''
        Sets the server type to default and clears the server
        '''
        await ctx.guild.edit(community=False)
        bot_role = ctx.guild.get_member(self.bot.user.id).top_role
        for ch in ctx.guild.channels:
            try:
                await ch.delete()
            except discord.errors.HTTPException as e:
                if e.code == 50074:
                    print(f"Skipped deletion of essential community channel: {channel.name}")
                else:
                    raise
        for role in ctx.guild.roles:
            if role != bot_role and ctx.guild.get_role(role.id):
                try:
                    await role.delete()
                except discord.errors.HTTPException as e:
                    if e.code == 50028:
                        print(f"Skipped deletion of essential role: {role.name}")
                    else:
                        raise

    def _convert_json(self, json_file_path):
        config = None
        try:
            with open(json_file_path, 'r') as json_file:
                config = json.load(json_file)
        except FileNotFoundError:
            print(f"File not found: {json_file_path}")
        return config

    @commands.command()
    async def test(self, ctx):
        await self.clear(ctx)
        config_file_path = '../tests/default.json'
        # config_file_path = '../tests/community.json'
        config = self._convert_json(config_file_path)
        config = await self.write.write_server(ctx, config)
        new_config_file_path = config_file_path[:-5] + '_v2.json'
        fp = open(new_config_file_path, 'w')
        json_config = json.dump(config, fp, indent=4)


async def setup(bot):
    await bot.add_cog(Ruco(bot))
