import os
import discord
from discord.ext import commands
# from ruco.read import Read
# from ruco.write import Write
# from ruco.test import Test
from DiscordBot.ruco.read import Read
from DiscordBot.ruco.write import Write
from DiscordBot.ruco.test import Test

def run():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='.', intents=intents)

    @bot.event
    async def on_ready():
        await bot.add_cog(Read(bot))
        await bot.add_cog(Write(bot))
        await bot.add_cog(Test(bot))

    bot.run(os.environ['DISCORD_TOKEN'])

if __name__ == '__main__':
    run()
