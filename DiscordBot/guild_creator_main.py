import asyncio
from DiscordInterface import DiscordInterface
import functions

async def main():
    discord_interface = DiscordInterface()
    await discord_interface.create_guild()

    # TODO: this waits until discord interface is done
    for thread in discord_interface.active_threads:
        thread.join()


if __name__ == "__main__":
    pass
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
