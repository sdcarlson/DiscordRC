import discord
import os
from DiscordBot.GuildCreatorBot import GuildCreatorBot
from DiscordBot.functions import GuildConfigurationCommands
import threading

# TODO: do we need Install Certificates
# Note: For this code to run on Mac, need to use the Install Certificates command on your Python
# installation (something about how python 3.6 or later handles SSL certificates on Mac?)
# Also, the Discord bot token should be stored in separate env file as DISCORD_TOKEN="...".

class DiscordInterface:
    """
    An interface for the Discord API for the backend to use.
    Runs bots in separate threads to avoid the blocking behavior of discord.py bots.

    Methods
    -------
    create_guild(guild_config_dict):
       Creates a new guild, returns an invite link.
    thread_done(bot):
       Removes the bot and the thread it was running in from DiscordInterface.
    """
    # DiscordInterface runs bots in separate threads when its methods are called.
    # This is to avoid the blocking behaviour of discord.py bots.

    def __init__(self):
        self.active_bots = []
        # The active_threads, bot_outputs, and bot_output_events map the object
        # ids of bots to their threads, outputs, and thread events respectively.
        self.active_threads = {}
        self.bot_outputs = {}
        self.bot_output_events = {}


    async def create_guild(self, guild_config_dict):
        """
        Creates a new Discord guild based on the supplied guild_config_dict.
        Returns an invite link to the Discord guild as a string.

        :param guild_config_dict: A dictionary representation of the JSON file
        :return: A Discord guild invitation link.
        """
        print("Creating a new guild!")
        # Set up the GuildCreatorBot
        bot_intents = discord.Intents.default()
        # Note: bots in 100 or more servers need verification for member intent.
        bot_intents.members = True
        Bot = GuildCreatorBot(self, bot_intents, guild_config_dict)
        # Adds the guild configuration commands to the bot
        await Bot.add_cog(GuildConfigurationCommands(Bot))

        # Run the GuildCreatorBot in a separate thread. If we want to run
        # multiple Bots at once, we need to do this because Bot.run is blocking.
        self.active_bots.append(Bot)
        bot_thread = threading.Thread(target=Bot.run, args=[os.environ['DISCORD_TOKEN']])
        bot_thread.daemon = False  # bot_thread will stop program from closing
        self.active_threads[id(Bot)] = bot_thread
        self.bot_output_events[id(Bot)] = threading.Event()
        bot_thread.start()

        # Once the bot signals that it has output the invite link, return it.
        self.bot_output_events[id(Bot)].wait()
        self.bot_output_events.pop(id(Bot))
        return self.bot_outputs.pop(id(Bot))

    def thread_done(self, bot):
        """
        Called by the bot when it's done. Removes the bot and the
        thread it was running in from DiscordInterface.

        :param: bot: The bot to remove.
        """
        self.active_bots.remove(bot)
        self.active_threads.pop(id(bot))

