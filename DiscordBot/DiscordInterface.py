import discord
import os
from DiscordBot.GuildCreatorBot import GuildCreatorBot
from DiscordBot.ruco.read import Read
from DiscordBot.ruco.write import Write
from DiscordBot.ruco.test import Test
import threading

# Note: For this code to run on Mac, need to use the Install Certificates command on your Python
# installation (something about how python 3.6 or later handles SSL certificates on Mac?)
# Also, the Discord bot token should be stored in separate env file as DISCORD_TOKEN="...".

class DiscordInterface:
    # DiscordInterface runs bots in separate threads when its methods are called.
    # This is to avoid the blocking behaviour of discord.py bots.

    def __init__(self):
        self.active_bots = []
        self.active_threads = {}
        self.bot_outputs = {}
        self.bot_output_events = {}


    async def create_guild(self, guild_config_dict):
        print("Creating a new guild!")
        # Set up the GuildCreatorBot
        bot_intents = discord.Intents.all()
        # Note: bots in 100 or more servers need verification for member intent.
        bot_intents.members = True
        Bot = GuildCreatorBot(self, bot_intents, guild_config_dict)
        # Adds the bot configuration commands to the bot
        await Bot.add_cog(Read(Bot))
        await Bot.add_cog(Write(Bot))
        await Bot.add_cog(Test(Bot))

        # Run the GuildCreatorBot in a separate thread. If we want to run
        # multiple Bots at once, we need to do this because Bot.run is blocking.
        self.active_bots.append(Bot)
        bot_thread = threading.Thread(target=Bot.run, args=[os.environ['DISCORD_TOKEN']])
        bot_thread.daemon = False  # bot_thread will stop program from closing
        self.active_threads[id(Bot)] = bot_thread
        self.bot_output_events[id(Bot)] = threading.Event()
        bot_thread.start()

        # Once the bot has output the invite link, return it.
        self.bot_output_events[id(Bot)].wait()
        self.bot_output_events.pop(id(Bot))
        return self.bot_outputs.pop(id(Bot))

    def thread_done(self, bot):
        # Once the bot_thread is done, it calls this to clean up
        bot_thread = self.active_threads[id(bot)]
        self.active_bots.remove(bot)
        self.active_threads.pop(id(bot))

