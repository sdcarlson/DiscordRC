import asyncio
import discord
import json
import os
from discord.ext import commands
from dotenv import load_dotenv
from functions_test import Ruco

async def main():
    load_dotenv()
    bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
    while True:
        await bot.add_cog(Ruco(bot))
        bot.run(os.environ['TOKEN'])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
