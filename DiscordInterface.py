import discord
from discord.ext.commands import command, Cog, Bot
import os
from GuildCreatorBot import GuildCreatorBot, OutsideCommunicationCog
from GuildManagerBot import GuildManagerBot
from discord.ext.commands import Bot
import threading
import asyncio

class DiscordInterface:
    def __init__(self):
        # Set up the GuildCreatorBot
        bot_intents = discord.Intents.default()
        # TODO: bots in 100 or more servers need verification for member intent
        bot_intents.members = True
        self.Bot = GuildCreatorBot(command_prefix="//", intents=bot_intents)

        # Run the GuildCreatorBot in a separate thread.
        # Separate thread is used because bot.run is blocking.
        # Based on: https://stackoverflow.com/questions/66335984/can-i-control-a-discord-py-bot-using-external-means
        bot_thread = threading.Thread(target=self.Bot.run, args=[os.environ['DISCORD_TOKEN']])
        bot_thread.daemon = True # bot_thread will not stop program from closing
        bot_thread.start()

        print("This is apparently the main thread")
        print(threading.get_ident())

        # The loop the bot is using
        self.bot_loop = asyncio.get_event_loop()

        # This must be initialized by setup
        self.outside_communication_cog = None

    async def setup(self):
        cogs = [OutsideCommunicationCog(self.Bot)]
        self.outside_communication_cog = cogs[0]
        for cog in cogs:
            await self.Bot.add_cog(cog)


    async def create_guild(self):
        if input("create a new guild? (input y for yes): ") == 'y':
                print("creating a new guild!")
                print(threading.get_ident())
                future = asyncio.run_coroutine_threadsafe(self.outside_communication_cog.say(None),
                                                          self.bot_loop)
                # future = asyncio.run_coroutine_threadsafe(self.Bot.create_new_guild(),
                #                                           self.bot_loop)

                # TODO: actually handle failures
                while not future.done():
                    await asyncio.sleep(10)

                # future = asyncio.run_coroutine_threadsafe(self.Bot.create_new_invite(),
                #                                           asyncio.get_event_loop())
                # while not future.done():
                #     await asyncio.sleep(1)
                # print(future.result())


                # future = asyncio.run_coroutine_threadsafe(self.outside_communication_cog.say(None), asyncio.get_event_loop())
                # i = 0
                # while i < 10:
                #     print("waiting for result...")
                #     print(future.running())
                #     await asyncio.sleep(1)
                #     i = i+1
                # Wait for the result with an optional timeout argument

                # new_guild_id = await self.Bot.create_new_guild()
                # except discord.HTTPException:
                #     # HTTPException will occur if guild creation fails, for example if the bot is in more than 10 guilds
                #     raise Err
                # future = asyncio.run_coroutine_threadsafe(self.Bot.create_new_invite(), self.asyncio_loop)
                # future.result(timeout = 10)

                # await self.Bot.create_new_invite()
        # else:
        #     await self.Bot.close()
        #     return None
        #
        # # TODO: return guild object rather than guild id
        # return new_guild_id
        return 0


    def apply_changes_to_guild(self, some_way_of_designating_guilds, json_file_or_something):
        bot_intents = discord.Intents.default()
        # TODO: bots in 100 or more servers need verification for member intent
        Bot = GuildManagerBot(intents = bot_intents)

        Bot.start(os.environ['DISCORD_TOKEN'])