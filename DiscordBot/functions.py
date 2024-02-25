import pdb
import pprint
import os
from dotenv import load_dotenv
import json
import discord
from discord.ext import commands
from permissions import role_perm_names, set_role_perm, \
                        cat_perm_names, set_cat_perm_overwrite, \
                        text_ch_perm_names, set_text_ch_perm_overwrite, \
                        voice_ch_perm_names, set_voice_ch_perm_overwrite

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

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
        if role_perm_name in role_config['permissions']:
            role_perm_val = role_config['permissions'][role_perm_name]
        set_role_perm(permissions, role_perm_name, role_perm_val)
    await role.edit(permissions=permissions)
    return role_config

@bot.command(name='update_text_channel')
async def update_text_channel(ctx, ch_config, role_ids, cat_id):
    '''
    Create a text channel with properties and permissions specified by
    the `text_channel` and `role_configs` dictionaries.
    '''
    cat = None
    if cat_id:
        cat = discord.utils.get(ctx.guild.categories, id=cat_id)

    ch_id = ch_config['id']
    name = ch_config['name']
    ch = None
    if ch_id == None:
        if cat:
            ch = await ctx.guild.create_text_channel(name, category=cat)
        else:
            ch = await ctx.guild.create_text_channel(name)
        ch_id = ch.id
        ch_config['id'] = ch_id
    else:
        ch = discord.utils.get(ctx.guild.channels, id=ch_id)

    def set_ch_perms_for_role(overwrite, role, ch_perms_for_role):
        for ch_perm_name in text_ch_perm_names:
            ch_perm_val = None
            if ch_perm_name in ch_perms_for_role:
                ch_perm_val = ch_perms_for_role[ch_perm_name]
            set_text_ch_perm_overwrite(overwrite, ch_perm_name, ch_perm_val)

    for role_id in role_ids:
        role = discord.utils.get(ctx.guild.roles, id=role_id) 
        overwrite = discord.PermissionOverwrite()
        ch_perms = ch_config['permissions']
        if role.name in ch_perms:
            set_ch_perms_for_role(overwrite, role, ch_perms[role.name])
            await ch.set_permissions(role, overwrite=overwrite)
    return ch_config

@bot.command(name='update_voice_channel')
async def update_voice_channel(ctx, ch_config, role_ids, cat_id):
    '''
    Create a voice channel with properties and permissions specified by
    the `voice_channel` and `role_configs` dictionaries.
    '''
    cat = None
    if cat_id:
        cat = discord.utils.get(ctx.guild.categories, id=cat_id)

    ch_id = ch_config['id']
    name = ch_config['name']
    ch = None
    if ch_id == None:
        if cat:
            ch = await ctx.guild.create_voice_channel(name, category=cat)
        else:
            ch = await ctx.guild.create_voice_channel(name)
        ch_id = ch.id
        ch_config['id'] = ch_id
    else:
        ch = discord.utils.get(ctx.guild.channels, id=ch_id)

    def set_ch_perms_for_role(overwrite, role, ch_perms_for_role):
        for ch_perm_name in voice_ch_perm_names:
            ch_perm_val = None
            if ch_perm_name in ch_perms_for_role:
                ch_perm_val = ch_perms_for_role[ch_perm_name]
            set_voice_ch_perm_overwrite(overwrite, ch_perm_name, ch_perm_val)

    for role_id in role_ids:
        role = discord.utils.get(ctx.guild.roles, id=role_id) 
        overwrite = discord.PermissionOverwrite()
        ch_perms = ch_config['permissions']
        if role.name in ch_perms:
            set_ch_perms_for_role(overwrite, role, ch_perms[role.name])
            await ch.set_permissions(role, overwrite=overwrite)
    return ch_config

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
    for i, cat_config in enumerate(config['categories']):
        pprint.pprint(cat_config)
        config['categories'][i] = await update_category(ctx, cat_config, role_ids)
        cat_id = config['categories'][i]['id']
        for j, text_ch_config in enumerate(cat_config['text_channels']):
            config['categories'][i]['text_channels'][j] = \
                await update_text_channel(ctx, text_ch_config, role_ids, cat_id)
        pprint.pprint('voice channels')
        pprint.pprint(cat_config['voice_channels'])
        for j, voice_ch_config in enumerate(cat_config['voice_channels']):
            config['categories'][i]['voice_channels'][j] = \
                await update_voice_channel(ctx, voice_ch_config, role_ids, cat_id)
    return config

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

@bot.command(name='delete_created_roles')
async def delete_tracked_roles(ctx, role_configs):
    '''
    Only deletes roles with id in the roles JSON config.
    '''
    for role_config in role_configs:
        if role_config['id']:
            role = discord.utils.get(ctx.guild.roles, id=role_config['id'])
            if role:
                await role.delete()

@bot.command(name='delete_created_categories')
async def delete_tracked_categories(ctx, cat_configs):
    '''
    Only deletes channels with id in the categories JSON config.
    Note that deleting a category does not delete the channels inside it.
    This is consistent with the native behavior in the Discord app.
    '''
    pass

@bot.command(name='delete_tracked_text_channels')
async def delete_tracked_text_channels(ctx, cat_configs):
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
        await delete_created_text_channels_in_cat(
            cat_config['text_channels'])

@bot.command(name='delete_tracked_entities')
async def delete_tracked_entities(ctx):
    '''
    Deletes all Discord objects with an id in the JSON config.
    '''
    config_file_path = './UnitTests/CreateRolesAndChannelsV2.json'
    config = convert_json(config_file_path)
    await delete_tracked_roles(ctx, config['roles'])
    await delete_tracked_text_channels(ctx, config['categories'])

config_file_path = './UnitTests/VoiceChannel.json'

@bot.command(name='test')
async def test(ctx, config_file_path=config_file_path):
    config = convert_json(config_file_path)
    config = await update_server(ctx, config)
    new_config_file_path = config_file_path[:-5] + 'V2.json'
    # new_config_file_path = './UnitTests/CreateRolesCategoriesAndChannelsV2.json'
    fp = open(new_config_file_path, 'w')
    json_config = json.dump(config, fp, indent=4)

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
