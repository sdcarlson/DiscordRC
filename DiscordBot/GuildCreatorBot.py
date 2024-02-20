import os
import threading

import discord
from discord.ext.commands import Bot
import asyncio

# Discord bot token is stored in separate .env file

NEW_GUILD_NAME = "new_guild"
BOT_NAME = "RCBot"

# TODO: should bot use sharding?
class GuildCreatorBot(Bot):
    # TODO: refactor this so it works with multiple guilds created at once instead of assuming just one

    def __init__(self, discord_interface, intents):
        super().__init__(command_prefix="//", intents=intents)
        self.discord_interface = discord_interface

    async def on_ready(self):
        print("Successfully logged in as " + str(self.user))
        print(threading.get_ident())

        await self.leave_all_guilds()

        # This bot automatically creates a new guild when ran.
        # TODO: should it initialize it in any basic way, or just use the other bot for that?
        if not await self.create_new_guild():
            await self.shut_down()
        await self.create_new_invite()

        # Connection will only be closed once user joins and ownership is handed over


    async def create_new_guild(self):
        # TODO: Bot accounts in more than 10 guilds can't create guilds
        try:
            await self.create_guild(name=NEW_GUILD_NAME)
        except discord.HTTPException:
            # HTTPException will occur if guild creation fails, usually the bot is in more than 10 guilds
            return False
        print("waiting for guild creation to be confirmed...")
        # Confirm that the guild has been created and is visible
        loop_count = 0
        while loop_count < 100:
            try:
                created_guild = await self.get_created_guild()
                break
            except LookupError:
                print("FAIL")
                await asyncio.sleep(0.2)
                loop_count += 1
        else:
            return False
        print("we have a guild")
        print("number of guilds: " + str(len(self.guilds)))
        return True


    async def create_new_invite(self):
        # TODO: what if someone deletes the general channel?
        created_guild = await self.get_created_guild()
        channel = None
        for channel in created_guild.channels:
            if channel.name == "general":
                break
        if channel is not None:
            channel_to_invite_to = channel
        else:
            raise LookupError("general channel not found")

        invite = await channel_to_invite_to.create_invite()
        print("Invite link: " + str(invite))

    async def give_non_bot_user_owner(self):
        created_guild = await self.get_created_guild()
        member = None
        async for member in created_guild.fetch_members():
            if not member.name.startswith(BOT_NAME):
                break
        if member is None:
            raise LookupError("no non-bot member found")

        print(member)
        print(member.guild_permissions)

        print("making this member owner...")
        new_guild = await created_guild.edit(owner=member)
        print(member.guild_permissions)

    async def leave_guild(self):
        guild = None
        for guild in self.guilds:
            if guild.name == NEW_GUILD_NAME:
                break
        if guild is None:
            raise LookupError("guild not found")

        await guild.leave()

    async def get_created_guild(self):
        guild = None
        for guild in self.guilds:
            if guild.name == NEW_GUILD_NAME:
                break
        if guild is None:
            raise LookupError("created guild not found")
        return guild

    # Overriding event functions
    # TODO: avoid calling this twice
    async def on_member_join(self, _member):
        print("member joined, making them owner!")
        await self.give_non_bot_user_owner()
        await self.leave_guild()
        print("left the guild!")
        await self.shut_down()

    # WARNING!!!! If the bot can't leave a guild due to being owner, it will delete the guild!
    async def leave_all_guilds(self):
        print("current number of guilds:" + str(len(self.guilds)))
        print("Warning: this may take a while if many guilds are being deleted because of rate limits.")
        for guild in self.guilds:
            try:
                await guild.leave()
            except discord.HTTPException:
                await guild.delete()
        print("left all guilds")

    async def shut_down(self):
        # TODO: is the unclosed connector error OK?
        await self.close()
        print("closed connection")
