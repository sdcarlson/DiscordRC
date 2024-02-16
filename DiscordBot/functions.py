import pdb
import json
import discord
from discord.ext import commands
from permissions import role_perm_names, set_role_perm, \
                        ch_perm_names, set_ch_perm_overwrite

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
async def update_text_channel(ctx, ch_config, role_configs):
    '''
    Create a text channel with properties and permissions specified by
    the `text_channel` and `role_configs` dictionaries.
    '''
    ch_id = ch_config['id']
    name = ch_config['name']
    ch = None
    if ch_id == None:
        ch = await ctx.guild.create_text_channel(name)
        ch_id = ch.id
        ch_config['id'] = ch_id
    else:
        ch = discord.utils.get(ctx.guild.channels, id=ch_id)

    def set_ch_perms_for_role(overwrite, role, ch_perms_for_role):
        for ch_perm_name in ch_perm_names:
            ch_perm_val = None
            if ch_perm_name in ch_perms_for_role:
                ch_perm_val = ch_perms_for_role[ch_perm_name]
            set_ch_perm_overwrite(overwrite, ch_perm_name, ch_perm_val)

    role_ids = [role_config['id'] for role_config in role_configs]
    for role_id in role_ids:
        role = discord.utils.get(ctx.guild.roles, id=role_id) 
        overwrite = discord.PermissionOverwrite()
        ch_perms = ch_config['permissions']
        if role.name in ch_perms:
            set_ch_perms_for_role(overwrite, role, ch_perms[role.name])
        await ch.set_permissions(role, overwrite=overwrite)
    return ch_config

@bot.command(name='update_category')
async def update_category(ctx, category_perms, roles):
    pass

@bot.command(name='create_voice_channel')
async def create_voice_channel(ctx, vc_perms, roles):
    id = voice_channel['id']
    name = voice_channel['name']
    if id == None:
        vc = await ctx.guild.create_voice_channel(name)
        id = vc.id
    else:
        vc = discord.utils.get(ctx.guild.channels, id=id)

    role_names = [role['name'] for role in roles]
    for role_name in role_names:
        overwrite = discord.PermissionOverwrite()
        for vc_perm_name in vc_perm_names:
            vc_perm_val = None
            if vc_perm_name in vc_perms:
                vc_perm_val = vc_perms[vc_perm_name]
            set_vc_perm_overwrite(overwrite, vc_perm_name, vc_perm_val)
        await vc.set_permissions(role, overwrite=overwrite)

@bot.command(name='update_server')
async def update_server(ctx, config):
    for i, role_config in enumerate(config['roles']):
        config['roles'][i] = await update_role(ctx, role_config)
    for i, category_config in enumerate(config['categories']):
        # config['categories'][i] = await update_category(ctx, category_config)
        for j, text_ch_config in enumerate(category_config['text_channels']):
            config['categories'][i]['text_channels'][j] = \
                await update_text_channel(ctx, text_ch_config, config['roles'])
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

@bot.command(name='delete_created_roles')
async def delete_created_roles(ctx, role_configs):
    '''
    Only deletes roles with id in the roles JSON config.
    '''
    for role_config in role_configs:
        if role_config['id']:
            role = discord.utils.get(ctx.guild.roles, id=role_config['id'])
            if role:
                await role.delete()

@bot.command(name='delete_created_categories')
async def delete_created_categories(ctx, category_configs):
    '''
    Only deletes channels with id in the categories JSON config.
    Note that deleting a category does not delete the channels inside it.
    This is consistent with the native behavior in the Discord app.
    '''
    pass

@bot.command(name='delete_created_text_channels')
async def delete_created_text_channels(ctx, category_configs):
    '''
    Only deletes channels with id in the text channels JSON config.
    '''
    async def delete_created_text_channels_in_category(ch_configs):
        for ch_config in ch_configs:
            if ch_config['id']:
                ch = discord.utils.get(ctx.guild.text_channels, id=ch_config['id'])
                if ch:
                    await ch.delete()

    for category_config in category_configs:
        await delete_created_text_channels_in_category(
            category_config['text_channels'])

@bot.command(name='clear')
async def clear(ctx):
    '''
    Clears all Discord objects with an id in the JSON config.
    '''
    config_file_path = './UnitTests/CreateRolesAndChannelsV2.json'
    config = convert_json(config_file_path)
    await delete_created_roles(ctx, config['roles'])
    await delete_created_text_channels(ctx, config['categories'])

@bot.command(name='test')
async def test(ctx):
    config_file_path = './UnitTests/CreateRolesAndChannels.json'
    config = convert_json(config_file_path)
    config = await update_server(ctx, config)
    new_config_file_path = './UnitTests/CreateChannelsAndRolesV2.json'
    fp = open(new_config_file_path, 'w')
    json_config = json.dump(config, fp, indent=4)

TOKEN = 'MTE5MzMyMjEwNDgxNzQ1MTEwOQ.GXtYMy.2PkMY5D_MKw3PXuqij4gQUS2gLRQlFZUpLzezo'
bot.run(TOKEN)
