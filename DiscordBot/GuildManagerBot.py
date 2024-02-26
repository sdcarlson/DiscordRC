import discord

BOT_NAME = "RCBot"

class GuildManagerBot(discord.Client):
    guild = None

    async def on_ready(self):
        print("Successfully logged in as " + str(self.user))

        # TODO: can use code from DiscordBot for the GuildManagerBot

        # TODO: is the unclosed connector error OK?
        await self.close()