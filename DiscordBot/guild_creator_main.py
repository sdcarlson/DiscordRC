import asyncio
import json

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DiscordBot.DiscordInterface import DiscordInterface

async def main():
    discord_interface = DiscordInterface()
    while (True):
        if input("create new guild(s)? (input y for yes): ") == 'y':
            num_guilds = int(input("input number of new guilds to create simultaneously: "))
            for i in range(num_guilds):
                json_file_path = input("which JSON file path to use for guild number " + str(i) + "? ")
                # ./DiscordRC/DiscordBot/UnitTests/NoCommunityTest.json
                if json_file_path == "":
                    invite_string = await discord_interface.create_guild(None)
                else:
                    guild_config_dict = convert_json(json_file_path)
                    invite_string = await discord_interface.create_guild(guild_config_dict)
                print("Invite link: " + invite_string)

def convert_json(json_file_path):
    config = None
    try:
        with open(json_file_path, 'r') as json_file:
            config = json.load(json_file)
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
    return config

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
