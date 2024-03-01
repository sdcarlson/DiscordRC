import asyncio

import discord
import os
from GuildCreatorBot import GuildCreatorBot
from functions import GuildConfigurationCommands
import threading

# Note: for discord bot code to work (on Mac at least), need certifi or use Install Certificates command in python
# installation (something about how python 3.6 or later handles SSL certificates on Mac?)
# Also, discord token is stored in separate env file.

class DiscordInterface:
    # DiscordInterface runs bots in separate threads when its methods are called.
    # This is to avoid the blocking behaviour of discord.py bots.

    def __init__(self):
        self.active_bots = []
        self.active_threads = []


    async def create_guild(self, json_file_path):
        print("creating a new guild!")
        print(threading.get_ident())

        # Set up the GuildCreatorBot
        bot_intents = discord.Intents.default()
        # TODO: bots in 100 or more servers need verification for member intent
        bot_intents.members = True
        Bot = GuildCreatorBot(self, bot_intents, json_file_path)
        # Adds the bot configuration functions to the bot
        await Bot.add_cog(GuildConfigurationCommands(Bot))
        self.active_bots.append(Bot)

        # Run the GuildCreatorBot in a separate thread.
        # Separate thread is used because bot.run is blocking.
        # Based on: https://stackoverflow.com/questions/66335984/can-i-control-a-discord-py-bot-using-external-means
        bot_thread = threading.Thread(target=Bot.run, args=[os.environ['DISCORD_TOKEN']])
        # TODO: eventually make this true
        bot_thread.daemon = False  # bot_thread will stop program from closing
        self.active_threads.append(bot_thread)
        bot_thread.start()

        print("This is apparently the main thread")
        print(threading.get_ident())


    def apply_changes_to_guild(self, some_way_of_designating_guilds, json_file_or_something):
        pass
        # TODO: bots in 100 or more servers need verification for member intent
