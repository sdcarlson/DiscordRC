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


class Write(commands.Cog):

    def __init__(self, bot, config=None):
        self.bot = bot
        self.config = config
        self.roles = None
        self.role_ids = None
        self.rules_ch_pos = -1
        self.updates_ch_pos = -1
        self.rules_ch_idcs = None
        self.updates_ch_idcs = None

    async def _write_role(self, ctx, role_config):
        role_id = role_config['id']
        name = role_config['name']
        if role_id == None:
            role = await ctx.guild.create_role(name=name)
            role_id = role.id
            role_config['id'] = role_id
        else:
            role = discord.utils.get(ctx.guild.roles, id=role_id)
    
        permissions = discord.Permissions()
        for role_perm_name in role_perm_names:
            role_perm_val = False # default to False
            if role_perm_name in set(role_config['permissions']):
                role_perm_val = True
            set_role_perm(permissions, role_perm_name, role_perm_val)
        await role.edit(permissions=permissions)
        return role_config

    def _set_ch_creator(self, ctx, cat, ch_id, ch_name, ch_type):
        # discord.py does not have a separate function
        # for creation of announcement channels
        async def create_announcement_channel(ch_name, cat=None):
            ancmt_ch = await ctx.guild.create_text_channel(ch_name,
                                category=cat, news=True)
            return ancmt_ch

        # RULES and UPDATES channels are initialized this way due to
        # bugs in the discord.py `guild.edit` function.
        # When converting a default server to a community server,
        # the discord.py documentation states that
        # the `guild.edit` function has TEXT channels for 
        # RULES and UPDATES channels as required fields.
        # However, the `guild.edit` function does work in the intended way.
        # Instead, discord.py has a bug where even in a default server,
        # discord.py can convert a TEXT channel into a RULES or UPDATES channel.
        # These converted channels are then passed into the `guild.edit` to
        # convert the default server to a community server.
        async def create_rules_channel(ch_name):
            rules_ch = await ctx.guild.create_text_channel(ch_name)
            await ctx.guild.edit(rules_channel=rules_ch)
            return rules_ch

        async def create_updates_channel(ch_name):
            updates_ch = await ctx.guild.create_text_channel(ch_name)
            await ctx.guild.edit(public_updates_channel=updates_ch)
            return updates_ch

        match ch_type:
            case Channel.TEXT:
                return ctx.guild.create_text_channel
            case Channel.VOICE:
                return ctx.guild.create_voice_channel
            case Channel.FORUM:
                return ctx.guild.create_forum
            case Channel.ANNOUNCEMENT:
                return create_announcement_channel
            case Channel.STAGE:
                return ctx.guild.create_stage_channel

            # RULES and UPDATES channels are both required before
            # converting a default server to a community server,
            # which means that if a server is a community server,
            # RULES and UPDATES channels must be initialized before
            # all other channels.
            case Channel.RULES:
                return create_rules_channel
            case Channel.UPDATES:
                return create_updates_channel
            case _:
                print(f"'{ch_type}' does not match any channel type!")

    def _set_ch_perms_for_role(self, overwrite, ch_perms_for_role, ch_type):
        def prepare_ch_perm_overwriter(ch_type):
            match ch_type:
                case Channel.TEXT:
                    return (text_ch_perm_names, set_text_ch_perm_overwrite)
                case Channel.VOICE:
                    return (voice_ch_perm_names, set_voice_ch_perm_overwrite)
                case Channel.FORUM:
                    return (forum_ch_perm_names, set_forum_ch_perm_overwrite)
                case Channel.ANNOUNCEMENT:
                    return (announcement_ch_perm_names,
                            set_announcement_ch_perm_overwrite)
                case Channel.STAGE:
                    return (stage_ch_perm_names, set_stage_ch_perm_overwrite)
                case Channel.RULES:
                    return (rules_ch_perm_names, set_rules_ch_perm_overwrite)
                case Channel.UPDATES:
                    return (updates_ch_perm_names,
                            set_updates_ch_perm_overwrite)
                case _:
                    print(f"'{ch_type}' does not match any channel type!")
    
        ch_perm_names, ch_perm_overwriter = prepare_ch_perm_overwriter(ch_type)
        for ch_perm_name in ch_perm_names:
            ch_perm_val = None
            if ch_perm_name in ch_perms_for_role:
                ch_perm_val = ch_perms_for_role[ch_perm_name]
            ch_perm_overwriter(overwrite, ch_perm_name, ch_perm_val)

    async def _move_ch(self, ctx, ch, ch_idcs):
        cat_idx, text_based_ch_idx = ch_idcs
        cat_config = self.config['categories'][cat_idx]
        cat = ctx.guild.get_channel(cat_config['id'])
        await ch.move(beginning=True, category=cat, offset=text_based_ch_idx)
    
        # The following is an unsuccessful attempt at
        # circumventing a bug in discord.py.
        # The code showcases that both the beginning and after flag used in
        # the `channel.move` function are bugged.
        #
        # if text_based_ch_idx > 0: 
        #     after_ch_config = \
        #        cat_config['text_based_channels'][text_based_ch_idx-1]
        #     after_ch = ctx.guild.get_channel(after_ch_config['id'])
        #     await ch.move(after=after_ch, category=cat, offset=-1)
        # else:
        #     await ch.move(beginning=True,
        #                   category=cat, offset=text_based_ch_idx)

    async def _write_ch(self, ctx, ch_config, role_ids, cat_id):
        '''
        Create a channel with properties and permissions specified by
        a channel dictionary (which is either in the `text_based_channel`
        or `voice_based_channel` list) and the `role_configs` dictionary.
        '''
        cat = None
        if cat_id:
            cat = discord.utils.get(ctx.guild.categories, id=cat_id)
    
        ch_id = ch_config['id']
        ch_name = ch_config['name']
        ch_type = get_ch_type_from_str(ch_config['channel_type'])
            
        ch_creator = self._set_ch_creator(ctx, cat, ch_id, ch_name, ch_type)
        ch = None
        if ch_id == None:
            if cat:
                ch = await ch_creator(ch_name, category=cat)
            else:
                ch = await ch_creator(ch_name)
            ch_id = ch.id
            ch_config['id'] = ch_id
        else:
            ch = discord.utils.get(ctx.guild.channels, id=ch_id)
    
        # The ch.edit(position=<new_position>) function does not work as
        # discord.py intends. But switch to using position from the
        # `channel.move` function if this discord.py function is fixed in
        # the future.
        # 
        # if ch_type == Channel.RULES and rules_ch_pos != -1:
        #     await ch.edit(position=rules_ch_pos)
        # if ch_type == Channel.UPDATES and updates_ch_pos != -1:
        #     await ch.edit(position=updates_ch_pos)
    
        if ch_type == Channel.RULES and self.rules_ch_idcs:
            await self._move_ch(ctx, ch, self.rules_ch_idcs)
        if ch_type == Channel.UPDATES and self.updates_ch_idcs:
            await self._move_ch(ctx, ch, self.updates_ch_idcs)

        print(ch_type, ch.name, ch.position)
    
        for role_id in role_ids:
            role = discord.utils.get(ctx.guild.roles, id=role_id) 
            overwrite = discord.PermissionOverwrite()
            ch_perms = ch_config['permissions']
            if role.name in ch_perms:
                self._set_ch_perms_for_role(overwrite, ch_perms[role.name],
                                           ch_type)
                await ch.set_permissions(role, overwrite=overwrite)
    
        return ch, ch_config

    def _set_cat_perms_for_role(self, overwrite, role, cat_perms_for_role):
        for cat_perm_name in cat_perm_names:
            cat_perm_val = None
            if cat_perm_name in cat_perms_for_role:
                cat_perm_val = cat_perms_for_role[cat_perm_name]
            set_cat_perm_overwrite(overwrite, cat_perm_name, cat_perm_val)

    async def _write_cat(self, ctx, cat_config, role_ids):
        cat_id = cat_config['id']
        name = cat_config['name']
        cat = None
        if name != None: # name can be null if not in a category
            if cat_id == None:
                cat = await ctx.guild.create_category(name)
                cat_id = cat.id
                cat_config['id'] = cat_id
            else:
                cat = discord.utils.get(ctx.guild.category, id=cat_id)
        for role_id in role_ids:
            role = discord.utils.get(ctx.guild.roles, id=role_id) 
            overwrite = discord.PermissionOverwrite()
            cat_perms = cat_config['permissions']
            # cat_perms can be null if not in a category
            if cat_perms and role.name in cat_perms: 
                self._set_cat_perms_for_role(overwrite,
                                             role, cat_perms[role.name])
                await cat.set_permissions(role, overwrite=overwrite)
        return cat_config

    async def _create_required_community_chs(self, ctx, config):
        '''
        Helper function for `write_server`.
        Iterates through the list of text-based channels under
        each category to find and create both a RULES and UPDATES channel.
        Returns a tuple of two tuples, where the first and second tuples for
        RULES and UPDATES channels respectively are of the form
        (channel, position).
    
        This is done to position RULES and UPDATES channels once
        all categories and channels have been initialized.
        '''
        pos_update = 0
        rules_ch = None
        updates_ch = None
        for i, cat_config in enumerate(config['categories']):
            self.rules_ch_pos += pos_update if not rules_ch != None else 0
            self.updates_ch_pos += pos_update if not updates_ch != None else 0
            pos_update = len(cat_config['text_based_channels'])
            for j, ch_config in enumerate(cat_config['text_based_channels']):
                ch_type = get_ch_type_from_str(ch_config['channel_type'])
                if rules_ch != None and updates_ch != None:
                    break
                elif ch_type == Channel.RULES:
                    rules_ch, config = \
                        await self._write_ch(ctx, ch_config,
                                                  self.role_ids, None)
                    # + 1 since list indices start with 0
                    self.rules_ch_pos += j + 1 
                    self.rules_ch_idcs = (i, j)
                elif ch_type == Channel.UPDATES:
                    updates_ch, config = \
                        await self._write_ch(ctx, ch_config,
                                                  self.role_ids, None)
                    self.updates_ch_pos += j + 1
                    self.updates_ch_idcs = (i, j)
        return rules_ch, updates_ch

    @commands.command()
    async def write_server(self, ctx, config):
        '''
        Updates the server with the given config.
        '''
        self.config = config
        for i, role_config in enumerate(config['roles']):
            config['roles'][i] = await self._write_role(ctx, role_config)
        self.role_ids = [role_config['id'] for role_config in config['roles']]
    
        if config['community'] == True:
            rules_ch, updates_ch = \
                await self._create_required_community_chs(ctx, config)
            await ctx.guild.edit(community=True,
                                 rules_channel=rules_ch,
                                 public_updates_channel=updates_ch)
        else:
            await ctx.guild.edit(community=False)
    
        for i, cat_config in enumerate(config['categories']):
            config['categories'][i] = \
                await self._write_cat(ctx, cat_config, self.role_ids)
            cat_id = config['categories'][i]['id']
            for j, ch_config in enumerate(cat_config['text_based_channels']):
                ch, config['categories'][i]['text_based_channels'][j] = \
                    await self._write_ch(ctx, ch_config, self.role_ids,
                                               cat_id)
            for j, ch_config in enumerate(cat_config['voice_based_channels']):
                ch, config['categories'][i]['voice_based_channels'][j] = \
                    await self._write_ch(ctx, ch_config, self.role_ids,
                                               cat_id)
        return config

    # ---------------
    # JSON processing
    # ---------------

    @commands.command()
    async def process_json_file(self, ctx):
        if ctx.message.attachments:
            attached_file = ctx.message.attachments[0]
            if attached_file.filename.endswith('.json'):
                file_content = await attached_file.read()
                try:
                    json_data = json.loads(file_content)
                    formatted_data = json.dumps(json_data, indent=2)
                except json.JSONDecodeError as e:
                    await ctx.send(f'Error decoding JSON!')

    def _convert_json(self, json_file_path):
        config = None
        try:
            with open(json_file_path, 'r') as json_file:
                config = json.load(json_file)
        except FileNotFoundError:
            print(f"File not found: {json_file_path}")
        return config


async def setup(bot):
    await bot.add_cog(Write(bot))
