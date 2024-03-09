import pdb
import pprint
import os
# from dotenv import load_dotenv
import json
import discord
from discord.ext import commands
from permissions import Channel, set_ch_type
from permissions import role_perm_names, set_role_perm, \
                        cat_perm_names, set_cat_perm_overwrite, \
                        text_ch_perm_names, set_text_ch_perm_overwrite, \
                        voice_ch_perm_names, set_voice_ch_perm_overwrite, \
                        forum_ch_perm_names, set_forum_ch_perm_overwrite, \
                        announcement_ch_perm_names, set_announcement_ch_perm_overwrite, \
                        stage_ch_perm_names, set_stage_ch_perm_overwrite, \
                        rules_ch_perm_names, set_rules_ch_perm_overwrite, \
                        updates_ch_perm_names, set_updates_ch_perm_overwrite

class GuildConfigurationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.command(name='sync')
async def sync(ctx):
    if ctx.author.id == 485313109360115714:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')

@bot.command(name='update_role')
async def update_role(ctx, role_config):
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

@bot.command(name='update_channel')
async def update_channel(ctx, ch_config, role_ids, cat_id):
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
    ch_type = set_ch_type(ch_config['type'])

    def set_ch_creator(ch_type):
        # discord.py does not have a separate function
        # for creation of announcement channels
        async def create_announcement_channel(ch_name, category=None):
            ancmt_ch = await ctx.guild.create_text_channel(ch_name,
                                category=category, news=True)
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

    ch_creator = set_ch_creator(ch_type)
    ch = None
    if ch_id == None:
        if cat:
            ch = await ch_creator(ch_name, category=cat)
        else:
            await ctx.send('You must be the owner to use this command!')

    @commands.command(name='update_role')
    async def update_role(self, ctx, role_config):
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
            if role_perm_name in role_config['permissions']:
                role_perm_val = role_config['permissions'][role_perm_name]
            set_role_perm(permissions, role_perm_name, role_perm_val)
        await role.edit(permissions=permissions)
        return role_config

    @commands.command(name='update_channel')
    async def update_channel(self, ctx, ch_config, role_ids, cat_id):
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
        ch_type = set_ch_type(ch_config['type'])

        def set_ch_creator(ch_type):
            # discord.py does not have a separate function
            # for creation of announcement channels
            def create_ancmt_channel(ch_name, category=None):
               return ctx.guild.create_text_channel(ch_name, category=category,
                                                    news=True)

    print("channel details:")
    print(ch.name, ch.position)

    def set_ch_perms_for_role(overwrite, ch_perms_for_role):
        def prepare_ch_perm_overwriter(ch_type):
            match ch_type:
                case Channel.TEXT:
                    return ctx.guild.create_text_channel
                case Channel.VOICE:
                    return ctx.guild.create_voice_channel
                case Channel.FORUM:
                    return (forum_ch_perm_names, set_forum_ch_perm_overwrite)
                case Channel.ANNOUNCEMENT:
                    return (announcement_ch_perm_names, set_announcement_ch_perm_overwrite)
                case Channel.STAGE:
                    return (stage_ch_perm_names, set_stage_ch_perm_overwrite)
                case Channel.RULES:
                    return (rules_ch_perm_names, set_rules_ch_perm_overwrite)
                case Channel.UPDATES:
                    return (updates_ch_perm_names, set_updates_ch_perm_overwrite)
                case _:
                    print(f"'{ch_type}' does not match any channel type!")

        ch_perm_names, ch_perm_overwriter = prepare_ch_perm_overwriter(ch_type)
        for ch_perm_name in ch_perm_names:
            ch_perm_val = None
            if ch_perm_name in ch_perms_for_role:
                ch_perm_val = ch_perms_for_role[ch_perm_name]
            ch_perm_overwriter(overwrite, ch_perm_name, ch_perm_val)

    for role_id in role_ids:
        role = discord.utils.get(ctx.guild.roles, id=role_id) 
        overwrite = discord.PermissionOverwrite()
        ch_perms = ch_config['permissions']
        if role.name in ch_perms:
            set_ch_perms_for_role(overwrite, ch_perms[role.name])
            await ch.set_permissions(role, overwrite=overwrite)

    return ch, ch_config

@bot.command(name='update_category')
async def update_category(ctx, cat_config, role_ids):
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

    def set_cat_perms_for_role(overwrite, role, cat_perms_for_role):
        for cat_perm_name in cat_perm_names:
            cat_perm_val = None
            if cat_perm_name in cat_perms_for_role:
                cat_perm_val = cat_perms_for_role[cat_perm_name]
            set_cat_perm_overwrite(overwrite, cat_perm_name, cat_perm_val)

    for role_id in role_ids:
        role = discord.utils.get(ctx.guild.roles, id=role_id) 
        overwrite = discord.PermissionOverwrite()
        cat_perms = cat_config['permissions']
        # cat_perms can be null if not in a category
        if cat_perms and role.name in cat_perms: 
            set_cat_perms_for_role(overwrite, role, cat_perms[role.name])
            await cat.set_permissions(role, overwrite=overwrite)
    return cat_config

@bot.command(name='update_server')
async def update_server(ctx, config):

    for i, role_config in enumerate(config['roles']):
        config['roles'][i] = await update_role(ctx, role_config)
    role_ids = [role_config['id'] for role_config in config['roles']]

    async def create_required_community_channels(config):
        '''
        Iterate through the list of text-based channels under
        each category to find and create both a RULES and UPDATES channel.
        Return a tuple of two tuples, where the first and second tuples for
        RULES and UPDATES channels respectively are of the form
        (channel, category index, channel index).

        This is done to position RULES and UPDATES channels once
        all categories and channels have been initialized.
        '''
        community_chs_data = [None, None]
        for i, cat_config in enumerate(config['categories']):
            for j, ch_config in enumerate(cat_config['text_based_channels']):
                ch_type = set_ch_type(ch_config['type'])
                if ch_type == Channel.RULES:
                    print('here1')
                    ch, config = await update_channel(ctx, ch_config, role_ids, None)
                    community_chs_data[0] = (ch, i, j)
                elif ch_type == Channel.UPDATES:
                    print('here2')
                    ch, config = await update_channel(ctx, ch_config, role_ids, None)
                    community_chs_data[1] = (ch, i, j)
        return tuple(community_chs_data)

    print('here')
    if config['community'] == True:
        rules_ch_data, updates_ch_data = await create_required_community_channels(config)
        print(rules_ch_data, updates_ch_data)
        await ctx.guild.edit(community=True,
                             rules_channel=rules_ch_data[0],
                             public_updates_channel=updates_ch_data[0])
    else:
        await ctx.guild.edit(community=False)

    for i, cat_config in enumerate(config['categories']):
        config['categories'][i] = await update_category(ctx, cat_config, role_ids)
        cat_id = config['categories'][i]['id']
        for j, ch_config in enumerate(cat_config['text_based_channels']):
            ch, config['categories'][i]['text_based_channels'][j] = \
                await update_channel(ctx, ch_config, role_ids, cat_id)
        for j, ch_config in enumerate(cat_config['voice_based_channels']):
            ch, config['categories'][i]['voice_based_channels'][j] = \
                await update_channel(ctx, ch_config, role_ids, cat_id)
    
    return config

@bot.command(name='process_json_file')
async def process_json_file(ctx):
    # Check if there are attachments in the message
    if ctx.message.attachments:
        # Get the first attached file
        attached_file = ctx.message.attachments[0]

        # Check if the attached file is a JSON file
        if attached_file.filename.endswith('.json'):
            # Download the file
            file_content = await attached_file.read()

            # Decode JSON content
            try:
                json_data = json.loads(file_content)

                # Process the JSON data
                # Example: Send a formatted version back to the user
                formatted_data = json.dumps(json_data, indent=2)
                await ctx.send(f'Processed JSON:\n```\n{formatted_data}\n```')

            except json.JSONDecodeError as e:
                await ctx.send(f'Error decoding JSON: {str(e)}')

        else:
            await ctx.send('Please attach a JSON file.')

    else:
        await ctx.send('No file attached.')

def convert_json(json_file_path):
    config = None
    try:
        with open(json_file_path, 'r') as json_file:
            config = json.load(json_file)
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
    return config

# ----------------
# cmds for testing
# ----------------

@bot.command(name='clear')
async def clear(ctx):
    bot_role = ctx.guild.get_member(bot.user.id).top_role
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
        except discord.errors.HTTPException as e:
            if e.code == 50074:
                print(f"Skipped deletion of essential community channel: {channel.name}")
            else:
                ch = await ch_creator(ch_name)
            ch_id = ch.id
            ch_config['id'] = ch_id
        else:
            ch = discord.utils.get(ctx.guild.channels, id=ch_id)

        def set_ch_perms_for_role(overwrite, role, ch_perms_for_role):
            def prepare_ch_perm_overwriter(ch_type):
                match ch_type:
                    case Channel.TEXT:
                        return (text_ch_perm_names, set_text_ch_perm_overwrite)
                    case Channel.VOICE:
                        return (voice_ch_perm_names, set_voice_ch_perm_overwrite)
                    case Channel.FORUM:
                        return (forum_ch_perm_names, set_forum_ch_perm_overwrite)
                    case Channel.ANCMT:
                        return (ancmt_ch_perm_names, set_ancmt_ch_perm_overwrite)
                    case Channel.STAGE:
                        return (stage_ch_perm_names, set_stage_ch_perm_overwrite)
                    case _:
                        print(f"'{s}' does not match any channel type!")

            ch_perm_names, ch_perm_overwriter = prepare_ch_perm_overwriter(ch_type)
            for ch_perm_name in ch_perm_names:
                ch_perm_val = None
                if ch_perm_name in ch_perms_for_role:
                    ch_perm_val = ch_perms_for_role[ch_perm_name]
                ch_perm_overwriter(overwrite, ch_perm_name, ch_perm_val)

        for role_id in role_ids:
            role = discord.utils.get(ctx.guild.roles, id=role_id)
            overwrite = discord.PermissionOverwrite()
            ch_perms = ch_config['permissions']
            if role.name in ch_perms:
                set_ch_perms_for_role(overwrite, role, ch_perms[role.name])
                await ch.set_permissions(role, overwrite=overwrite)
        return ch_config

    @commands.command(name='update_category')
    async def update_category(self, ctx, cat_config, role_ids):
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

        def set_cat_perms_for_role(overwrite, role, cat_perms_for_role):
            for cat_perm_name in cat_perm_names:
                cat_perm_val = None
                if cat_perm_name in cat_perms_for_role:
                    cat_perm_val = cat_perms_for_role[cat_perm_name]
                set_cat_perm_overwrite(overwrite, cat_perm_name, cat_perm_val)

        for role_id in role_ids:
            role = discord.utils.get(ctx.guild.roles, id=role_id)
            overwrite = discord.PermissionOverwrite()
            cat_perms = cat_config['permissions']
            # cat_perms can be null if not in a category
            if cat_perms and role.name in cat_perms:
                set_cat_perms_for_role(overwrite, role, cat_perms[role.name])
                await cat.set_permissions(role, overwrite=overwrite)
        return cat_config

    @commands.command(name='update_server')
    async def update_server(self, ctx, config):
        await ctx.guild.edit(name = config['name'])
        # await ctx.guild.edit(community=config['community'])
        for i, role_config in enumerate(config['roles']):
            config['roles'][i] = await self.update_role(ctx, role_config)
        role_ids = [role_config['id'] for role_config in config['roles']]
        for i, cat_config in enumerate(config['categories']):
            config['categories'][i] = await self.update_category(ctx, cat_config, role_ids)
            cat_id = config['categories'][i]['id']
            for j, ch_config in enumerate(cat_config['text_based_channels']):
                config['categories'][i]['text_based_channels'][j] = \
                    await self.update_channel(ctx, ch_config, role_ids, cat_id)
            for j, ch_config in enumerate(cat_config['voice_based_channels']):
                config['categories'][i]['voice_based_channels'][j] = \
                    await self.update_channel(ctx, ch_config, role_ids, cat_id)
        return config

    @commands.command(name='process_json_file')
    async def process_json_file(self, ctx):
        # Check if there are attachments in the message
        if ctx.message.attachments:
            # Get the first attached file
            attached_file = ctx.message.attachments[0]

            # Check if the attached file is a JSON file
            if attached_file.filename.endswith('.json'):
                # Download the file
                file_content = await attached_file.read()

                # Decode JSON content
                try:
                    json_data = json.loads(file_content)

                    # Process the JSON data
                    # Example: Send a formatted version back to the user
                    formatted_data = json.dumps(json_data, indent=2)
                    await ctx.send(f'Processed JSON:\n```\n{formatted_data}\n```')

                except json.JSONDecodeError as e:
                    await ctx.send(f'Error decoding JSON: {str(e)}')

            else:
                await ctx.send('Please attach a JSON file.')

        else:
            await ctx.send('No file attached.')

    def convert_json(self, json_file_path):
        config = None
        try:
            with open(json_file_path, 'r') as json_file:
                config = json.load(json_file)
        except FileNotFoundError:
            print(f"File not found: {json_file_path}")
        return config

    # ----------------
    # cmds for testing
    # ----------------

    @commands.command(name='clear')
    async def clear(self, ctx):
        bot_role = ctx.guild.get_member(self.bot.user.id).top_role
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
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

    @commands.command(name='delete_created_roles')
    async def delete_tracked_roles(self, ctx, role_configs):
        '''
        Only deletes roles with id in the roles JSON config.
        '''
        for role_config in role_configs:
            if role_config['id']:
                role = discord.utils.get(ctx.guild.roles, id=role_config['id'])
                if role:
                    await role.delete()

    @commands.command(name='delete_created_categories')
    async def delete_tracked_categories(self, ctx, cat_configs):
        '''
        Only deletes channels with id in the categories JSON config.
        Note that deleting a category does not delete the channels inside it.
        This is consistent with the native behavior in the Discord app.
        '''
        pass

    @commands.command(name='delete_tracked_text_channels')
    async def delete_tracked_text_channels(self, ctx, cat_configs):
        '''
        Only deletes channels with id in the text channels JSON config.
        '''
        async def delete_tracked_text_channels_in_cat(ch_configs):
            for ch_config in ch_configs:
                if ch_config['id']:
                    ch = discord.utils.get(ctx.guild.text_channels, id=ch_config['id'])
                    if ch:
                        await ch.delete()

        for cat_config in cat_configs:
            await self.delete_created_text_channels_in_cat(
                cat_config['text_channels'])

    @commands.command(name='delete_tracked_entities')
    async def delete_tracked_entities(self, ctx):
        '''
        Deletes all Discord objects with an id in the JSON config.
        '''
        config_file_path = './UnitTests/CreateRolesAndChannelsV2.json'
        config = self.convert_json(config_file_path)
        await self.delete_tracked_roles(ctx, config['roles'])
        await self.delete_tracked_text_channels(ctx, config['categories'])

    config_file_path = './UnitTests/SeparateTextAndVoiceBasedChannels.json'

    @commands.command(name='test')
    async def test(self, ctx, config_file_path=config_file_path):
        config = self.convert_json(config_file_path)
        config = await self.update_server(ctx, config)
        new_config_file_path = config_file_path[:-5] + 'V2.json'
        fp = open(new_config_file_path, 'w')
        json_config = json.dump(config, fp, indent=4)

config_file_path = './UnitTests/DefaultServer.json'


