import asyncio
import os
import json
import discord
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from discord.ext import commands
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


class Read(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def _read_roles(self, ctx, config):
        role_configs = []
        for role in self.roles:
            role_config = {}
            role_config['name'] = role.name
            role_config['id'] = role.id
            role_config['permissions'] = \
                [perm[0] for perm in iter(role.permissions) if perm[1]]
            role_configs.append(role_config)
        config['roles'] = role_configs

    def _get_role_perms_in_ch(self, ctx, config, ch):
        '''
        get the set of permissions after merging role permissions and
        channel permissions, where channel permissions take precedence
        '''
        for role_config in config['roles']:
            role_id = role_config['id']
            role = discord.utils.get(ctx.guild.roles, id=role_id)
            perms = dict(ch_or_cat.permissions_for(role)).items()
            for perm_name, perm_val in perms:
                if config['roles'][perm_name] == perm_val:
                    continue
                cat_role_perms[perm_name]


        role_perms
        role_perms_in_cat
        pass

    def _get_role_perms_in_cat(self, ctx, config, cat):
        role_perms = {}
        for role_config in config['roles']:
            role_id = role_config['id']
            role = discord.utils.get(ctx.guild.roles, id=role_id)
            perms = dict(ch_or_cat.permissions_for(role)).items()
            for perm_name, perm_val in perms:
                if config['roles'][perm_name] == perm_val:
                    continue
                cat_role_perms[perm_name] = perm_val
        return role_perms

    def _add_ch_config(self, ctx, config, cat_config, ch):
        text_based_ch_configs = []
        voice_based_ch_configs = []
        ch_config = {
            'name': ch.name,
            'id': ch.id,
            'channel_type': get_ch_type_from_ch(ctx, ch),
            'permissions': self._get_role_perms_in_ch(ctx, config, ch)
        }
        if is_text_based_ch(ctx, ch):
            text_based_ch_configs.append(ch_config)
        else:
            voice_based_ch_configs.append(ch_config)
        cat_config['text_based_channels'] = text_based_ch_configs
        cat_config['voice_based_channels'] = voice_based_ch_configs

    def _read_default_cat(self, ctx, config, cat_configs, cats_and_ch_lists):
        default_cat_config = {
            'name': None,
            'id': None,
            'permissions': None,
        }
        default_cat_and_ch_list = cats_and_ch_lists[0]
        _, default_cat_chs = default_cat_and_ch_list
        for ch in default_cat_chs:
            self._add_ch_config(ctx, config, default_cat_config, ch)
        cat_configs.append(default_cat_config)

    def _read_cat(self, ctx, config, cat_configs, cats_and_ch_lists):
        for cat, ch_list in cats_and_ch_lists:
            cat_config = {
                'name': cat.name,
                'id': cat.id,
                'permissions': self._get_role_perms_in_cat(ctx, config, cat)
            }
            for ch in ch_list:
                self._add_ch_config(ctx, config, cat_config, ch)
            cat_configs.append(cat_config)

    def _read_cats(self, ctx, config):
        cat_configs = []
        # cats_and_ch_lists = ctx.guild.by_category()
        # role = self.roles[2]
        # ch = cats_and_ch_lists[0][1][0]
        # perms = dict(ch.permissions_for(role))
        # print('channel name', ch.name)
        # print('role name', role.name)
        # print(json.dumps(perms, indent=4))
        # return

        self._read_default_cat(ctx, config, cat_configs, cats_and_ch_lists)
        self._read_cat(ctx, config, cat_configs, cats_and_ch_lists)

        for cat, chs in cats[1:]:
            cat_config = {
                'name': cat.name,
                'id': cat.id,
                'permissions': self._get_role_perms_in_cat(ctx, config, cat)
            }
            cat_configs.append(cat_config)

        config['categories'] = cat_configs
        return

    @commands.command()
    async def read_server(self, ctx):
        '''
        Reads the server.
        '''
        config = {}
        self.roles = await ctx.guild.fetch_roles()
        self._read_roles(ctx, config)
        self._read_cats(ctx, config)
        return
        print(json.dumps(config, indent=4))


async def setup(bot):
    await bot.add_cog(Read(bot))
