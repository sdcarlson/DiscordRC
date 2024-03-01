import asyncio
from DiscordInterface import DiscordInterface

async def main():
    discord_interface = DiscordInterface()
    if input("create new guild(s)? (input y for yes): ") == 'y':
        num_guilds = int(input("input number of new guilds to create simultaneously: "))
        for i in range(num_guilds):
            await discord_interface.create_guild()

        # TODO: this waits until discord interface is done
        for thread in discord_interface.active_threads:
            thread.join()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
