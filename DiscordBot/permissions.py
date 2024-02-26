# Aside: At the time of writing, there is no set_voice_channel_status
# permission available for categories and voice channels in the discord.py API.
# The pull request for the permission is being worked on here:
# https://github.com/discord/discord-api-docs/pull/6400
# P.S.: create_events is not supported for voice channels and categories either.

# Channel Ordering:
# Note that forum, announcement, and stage channels are options only for community channels.
# Text-based channels such as text, forum, and announcement channels can swap orders.
# Voice-based channels such as voice and stage channels can swap orders.
# However, text-based and voice-based channels cannot swap orders;
# moreover, voice-based channels must be ordered below text-based channels
# in each category and when not in a category.

from enum import Enum

class Channel(Enum):
    TEXT = 1
    VOICE = 2
    FORUM = 3
    ANCMT = 4
    STAGE = 5

def set_ch_type(s):
    match s:
        case 'TEXT':
            return Channel.TEXT
        case 'VOICE':
            return Channel.VOICE
        case 'FORUM':
            return Channel.FORUM
        case 'ANCMT':
            return Channel.ANCMT
        case 'STAGE':
            return Channel.STAGE
        case _:
            print(f"'{s}' does not match any channel type!")

role_perm_names = [
    'add_reactions',
    'administrator',
    'attach_files',
    'ban_members',
    'change_nickname',
    'create_events',
    'connect',
    'create_expressions',
    'create_instant_invite',
    'create_private_threads',
    'create_public_threads',
    'deafen_members',
    'embed_links',
    'external_emojis',
    'external_stickers',
    'kick_members',
    'manage_channels',
    'manage_emojis',
    'manage_emojis_and_stickers',
    'manage_events',
    'manage_expressions',
    'manage_guild',
    'manage_messages',
    'manage_nicknames',
    'manage_permissions',
    'manage_roles',
    'manage_threads',
    'manage_webhooks',
    'mention_everyone',
    'moderate_members',
    'move_members',
    'mute_members',
    'priority_speaker',
    'read_message_history',
    'read_messages',
    'request_to_speak',
    'send_messages',
    'send_messages_in_threads',
    'send_tts_messages',
    'send_voice_messages',
    'speak',
    'stream',
    'use_application_commands',
    'use_embedded_activities',
    'use_external_emojis',
    'use_external_sounds',
    'use_external_stickers',
    'use_soundboard',
    'use_voice_activation',
    'value',
    'view_audit_log',
    'view_channel',
    'view_guild_insights',
]

def set_role_perm(perm, role_perm_name, role_perm_val):
    match role_perm_name:
        case 'add_reactions':
            perm.update(add_reactions=role_perm_val)
        case 'administrator':
            perm.update(administrator=role_perm_val)
        case 'attach_files':
            perm.update(attach_files=role_perm_val)
        case 'ban_members':
            perm.update(ban_members=role_perm_val)
        case 'change_nickname':
            perm.update(change_nickname=role_perm_val)
        case 'connect':
            perm.update(connect=role_perm_val)
        case 'create_events':
            perm.update(create_events=role_perm_val)
        case 'create_expressions':
            perm.update(create_expressions=role_perm_val)
        case 'create_instant_invite':
            perm.update(create_instant_invite=role_perm_val)
        case 'create_private_threads':
            perm.update(create_private_threads=role_perm_val)
        case 'create_public_threads':
            perm.update(create_public_threads=role_perm_val)
        case 'deafen_members':
            perm.update(deafen_members=role_perm_val)
        case 'embed_links':
            perm.update(embed_links=role_perm_val)
        case 'external_emojis':
            perm.update(external_emojis=role_perm_val)
        case 'external_stickers':
            perm.update(external_stickers=role_perm_val)
        case 'kick_members':
            perm.update(kick_members=role_perm_val)
        case 'manage_channels':
            perm.update(manage_channels=role_perm_val)
        case 'manage_emojis':
            perm.update(manage_emojis=role_perm_val)
        case 'manage_emojis_and_stickers':
            perm.update(manage_emojis_and_stickers=role_perm_val)
        case 'manage_events':
            perm.update(manage_events=role_perm_val)
        case 'manage_expressions':
            perm.update(manage_expressions=role_perm_val)
        case 'manage_guild':
            perm.update(manage_guild=role_perm_val)
        case 'manage_messages':
            perm.update(manage_messages=role_perm_val)
        case 'manage_nicknames':
            perm.update(manage_nicknames=role_perm_val)
        case 'manage_permissions':
            perm.update(manage_permissions=role_perm_val)
        case 'manage_roles':
            perm.update(manage_roles=role_perm_val)
        case 'manage_threads':
            perm.update(manage_threads=role_perm_val)
        case 'manage_webhooks':
            perm.update(manage_webhooks=role_perm_val)
        case 'mention_everyone':
            perm.update(mention_everyone=role_perm_val)
        case 'moderate_members':
            perm.update(moderate_members=role_perm_val)
        case 'move_members':
            perm.update(move_members=role_perm_val)
        case 'mute_members':
            perm.update(mute_members=role_perm_val)
        case 'priority_speaker':
            perm.update(priority_speaker=role_perm_val)
        case 'read_message_history':
            perm.update(read_message_history=role_perm_val)
        case 'read_messages':
            perm.update(read_messages=role_perm_val)
        case 'request_to_speak':
            perm.update(request_to_speak=role_perm_val)
        case 'send_messages':
            perm.update(send_messages=role_perm_val)
        case 'send_messages_in_threads':
            perm.update(send_messages_in_threads=role_perm_val)
        case 'send_tts_messages':
            perm.update(send_tts_messages=role_perm_val)
        case 'send_voice_messages':
            perm.update(send_voice_messages=role_perm_val)
        case 'speak':
            perm.update(speak=role_perm_val)
        case 'stream':
            perm.update(stream=role_perm_val)
        case 'use_application_commands':
            perm.update(use_application_commands=role_perm_val)
        case 'use_embedded_activities':
            perm.update(use_embedded_activities=role_perm_val)
        case 'use_external_emojis':
            perm.update(use_external_emojis=role_perm_val)
        case 'use_external_sounds':
            perm.update(use_external_sounds=role_perm_val)
        case 'use_external_stickers':
            perm.update(use_external_stickers=role_perm_val)
        case 'use_soundboard':
            perm.update(use_soundboard=role_perm_val)
        case 'use_voice_activation':
            perm.update(use_voice_activation=role_perm_val)
        case 'value':
            perm.update(value=role_perm_val)
        case 'view_audit_log':
            perm.update(view_audit_log=role_perm_val)
        case 'view_channel':
            perm.update(view_channel=role_perm_val)
        case 'view_guild_insights':
            perm.update(view_guild_insights=role_perm_val)
        case _:
            print(f"'{role_perm_name}' does not match any role permission!")

text_ch_perm_names = [
    'add_reactions',
    'attach_files',
    'create_instant_invite',
    'create_private_threads',
    'create_public_threads',
    'embed_links',
    'manage_channels',
    'manage_messages',
    'manage_permissions',
    'manage_threads',
    'manage_webhooks',
    'mention_everyone',
    'read_message_history',
    'send_messages',
    'send_messages_in_threads',
    'send_tts_messages',
    'send_voice_messages',
    'use_application_commands',
    'use_embedded_activities',
    'use_external_emojis',
    'use_external_stickers',
    'view_channel'
]

def set_text_ch_perm_overwrite(overwrite, ch_perm_name, ch_perm_val):
    match ch_perm_name:
        case 'add_reactions':
            overwrite.add_reactions = ch_perm_val
        case 'attach_files':
            overwrite.attach_files = ch_perm_val
        case 'create_instant_invite':
            overwrite.create_instant_invite = ch_perm_val
        case 'create_private_threads':
            overwrite.create_private_threads = ch_perm_val
        case 'create_public_threads':
            overwrite.create_public_threads = ch_perm_val
        case 'embed_links':
            overwrite.embed_links = ch_perm_val
        case 'manage_channels':
            overwrite.manage_channels = ch_perm_val
        case 'manage_messages':
            overwrite.manage_messages = ch_perm_val
        case 'manage_permissions':
            overwrite.manage_permissions = ch_perm_val
        case 'manage_threads':
            overwrite.manage_threads = ch_perm_val
        case 'manage_webhooks':
            overwrite.manage_webhooks = ch_perm_val
        case 'mention_everyone':
            overwrite.mention_everyone = ch_perm_val
        case 'read_message_history':
            overwrite.read_message_history = ch_perm_val
        case 'send_messages':
            overwrite.send_messages = ch_perm_val
        case 'send_messages_in_threads':
            overwrite.send_messages_in_threads = ch_perm_val
        case 'send_tts_messages':
            overwrite.send_tts_messages = ch_perm_val
        case 'send_voice_messages':
            overwrite.send_voice_messages = ch_perm_val
        case 'use_application_commands':
            overwrite.use_application_commands = ch_perm_val
        case 'use_embedded_activities':
            overwrite.use_embedded_activities = ch_perm_val
        case 'use_external_emojis':
            overwrite.use_external_emojis = ch_perm_val
        case 'use_external_stickers':
            overwrite.use_external_stickers = ch_perm_val
        case 'view_channel':
            overwrite.view_channel = ch_perm_val
        case _:
            print(f"'{ch_perm_name}' does not match any text channel permission!")

voice_ch_perm_names = [
    'add_reactions',
    'attach_files',
    'connect',
    # 'create_events',
    'create_instant_invite',
    'deafen_members',
    'embed_links',
    'manage_channels',
    'manage_events',
    'manage_messages',
    'manage_permissions',
    'mention_everyone',
    'move_members',
    'mute_members',
    'priority_speaker',
    'read_message_history',
    'send_messages',
    'send_tts_messages',
    'send_voice_messages',
    'speak',
    'stream',
    'use_application_commands',
    'use_embedded_activities',
    'use_external_emojis',
    'use_external_sounds',
    'use_external_stickers',
    'use_soundboard',
    'use_voice_activation',
    'view_channel',
]

def set_voice_ch_perm_overwrite(overwrite, ch_perm_name, ch_perm_val):
    match ch_perm_name:
        case 'add_reactions':
            overwrite.add_reactions = ch_perm_val
        case 'attach_files':
            overwrite.attach_files = ch_perm_val
        case 'connect':
            overwrite.connect = ch_perm_val
        # case 'create_events':
        #     overwrite.create_events = ch_perm_val
        case 'create_instant_invite':
            overwrite.create_instant_invite = ch_perm_val
        case 'deafen_members':
            overwrite.deafen_members = ch_perm_val
        case 'embed_links':
            overwrite.embed_links = ch_perm_val
        case 'manage_channels':
            overwrite.manage_channels = ch_perm_val
        case 'manage_events':
            overwrite.manage_events = ch_perm_val
        case 'manage_messages':
            overwrite.manage_messages = ch_perm_val
        case 'manage_permissions':
            overwrite.manage_permissions = ch_perm_val
        case 'mention_everyone':
            overwrite.mention_everyone = ch_perm_val
        case 'move_members':
            overwrite.move_members = ch_perm_val
        case 'mute_members':
            overwrite.mute_members = ch_perm_val
        case 'priority_speaker':
            overwrite.priority_speaker = ch_perm_val
        case 'read_message_history':
            overwrite.read_message_history = ch_perm_val
        case 'send_messages':
            overwrite.send_messages = ch_perm_val
        case 'send_tts_messages':
            overwrite.send_tts_messages = ch_perm_val
        case 'send_voice_messages':
            overwrite.send_voice_messages = ch_perm_val
        case 'speak':
            overwrite.speak = ch_perm_val
        case 'stream':
            overwrite.stream = ch_perm_val
        case 'use_application_commands':
            overwrite.use_application_commands = ch_perm_val
        case 'use_embedded_activities':
            overwrite.use_embedded_activities = ch_perm_val
        case 'use_external_emojis':
            overwrite.use_external_emojis = ch_perm_val
        case 'use_external_sounds':
            overwrite.use_external_sounds = ch_perm_val
        case 'use_external_stickers':
            overwrite.use_external_stickers = ch_perm_val
        case 'use_soundboard':
            overwrite.use_soundboard = ch_perm_val
        case 'use_voice_activation':
            overwrite.use_voice_activation = ch_perm_val
        case 'view_channel':
            overwrite.view_channel = ch_perm_val
        case _:
            print(f"'{ch_perm_name}' does not match any voice channel permission!")

forum_ch_perm_names = [
]

def set_forum_ch_perm_overwrite(overwrite, ch_perm_name, ch_perm_val):
    pass

ancmt_ch_perm_names = [
]

def set_ancmt_ch_perm_overwrite(overwrite, ch_perm_name, ch_perm_val):
    pass

stage_ch_perm_names = [
]

def set_stage_ch_perm_overwrite(overwrite, ch_perm_name, ch_perm_val):
    pass

cat_perm_names = [
    'add_reactions',
    'attach_files',
    'connect',
    # 'create_events',
    'create_instant_invite',
    'create_private_threads',
    'create_public_threads',
    'deafen_members',
    'embed_links',
    'manage_channels',
    'manage_events',
    'manage_messages',
    'manage_permissions',
    'manage_threads',
    'manage_webhooks',
    'mention_everyone',
    'move_members',
    'mute_members',
    'priority_speaker',
    'read_message_history',
    'request_to_speak',
    'send_messages',
    'send_messages_in_threads',
    'send_tts_messages',
    'send_voice_messages',
    'speak',
    'stream',
    'use_application_commands',
    'use_embedded_activities',
    'use_external_emojis',
    'use_external_sounds',
    'use_external_stickers',
    'use_soundboard',
    'use_voice_activation',
    'view_channel'
]

def set_cat_perm_overwrite(overwrite, cat_perm_name, cat_perm_val):
    match cat_perm_name:
        case 'add_reactions':
            overwrite.add_reactions = cat_perm_val
        case 'attach_files':
            overwrite.attach_files = cat_perm_val
        case 'connect':
            overwrite.connect = cat_perm_val
        # case 'create_events':
        #     overwrite.create_events = cat_perm_val
        case 'create_instant_invite':
            overwrite.create_instant_invite = cat_perm_val
        case 'create_private_threads':
            overwrite.create_private_threads = cat_perm_val
        case 'create_public_threads':
            overwrite.create_public_threads = cat_perm_val
        case 'deafen_members':
            overwrite.deafen_members = cat_perm_val
        case 'embed_links':
            overwrite.embed_links = cat_perm_val
        case 'manage_channels':
            overwrite.manage_channels = cat_perm_val
        case 'manage_events':
            overwrite.manage_events = cat_perm_val
        case 'manage_messages':
            overwrite.manage_messages = cat_perm_val
        case 'manage_permissions':
            overwrite.manage_permissions = cat_perm_val
        case 'manage_threads':
            overwrite.manage_threads = cat_perm_val
        case 'manage_webhooks':
            overwrite.manage_webhooks = cat_perm_val
        case 'mention_everyone':
            overwrite.mention_everyone = cat_perm_val
        case 'move_members':
            overwrite.move_members = cat_perm_val
        case 'mute_members':
            overwrite.mute_members = cat_perm_val
        case 'priority_speaker':
            overwrite.priority_speaker = cat_perm_val
        case 'read_message_history':
            overwrite.read_message_history = cat_perm_val
        case 'request_to_speak':
            overwrite.request_to_speak = cat_perm_val
        case 'send_messages':
            overwrite.send_messages = cat_perm_val
        case 'send_messages_in_threads':
            overwrite.send_messages_in_threads = cat_perm_val
        case 'send_tts_messages':
            overwrite.send_tts_messages = cat_perm_val
        case 'send_voice_messages':
            overwrite.send_voice_messages = cat_perm_val
        case 'speak':
            overwrite.speak = cat_perm_val
        case 'stream':
            overwrite.stream = cat_perm_val
        case 'use_application_commands':
            overwrite.use_application_commands = cat_perm_val
        case 'use_embedded_activities':
            overwrite.use_embedded_activities = cat_perm_val
        case 'use_external_emojis':
            overwrite.use_external_emojis = cat_perm_val
        case 'use_external_sounds':
            overwrite.use_external_sounds = cat_perm_val
        case 'use_external_stickers':
            overwrite.use_external_stickers = cat_perm_val
        case 'use_soundboard':
            overwrite.use_soundboard = cat_perm_val
        case 'use_voice_activation':
            overwrite.use_voice_activation = cat_perm_val
        case 'view_channel':
            overwrite.view_channel = cat_perm_val
        case _:
            print(f"'{cat_perm_name}' does not match any category permission!")
