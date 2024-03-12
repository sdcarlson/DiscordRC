import discord
from discord.ext.commands import Bot
import asyncio

NEW_GUILD_NAME = "new_guild"
BOT_NAME = "RCBot"

class GuildCreatorBot(Bot):
    def __init__(self, discord_interface, intents, guild_config_dict):
        # TODO: note that guild_config_dict may be None for no config in comments
        super().__init__(command_prefix="//", intents=intents)
        self.discord_interface = discord_interface # Reference to the DiscordInterface which started the Bot
        self.guild_config_dict = guild_config_dict # Object containing config information for the guild.
        self.guild_read_cog = None
        self.guild_write_cog = None
        self.guild_test_cog = None
        self.guild_configuration_cog = None # Cog containing the commands and methods for guild configuration.
        self.created_guild_id = None # Discord guild ID of the guild created by this bot

    async def on_ready(self):
        print("Successfully logged in as " + str(self.user))

        self.guild_read_cog = self.get_cog("Read")
        self.guild_write_cog = self.get_cog("Write")
        self.guild_test_cog = self.get_cog("Test")
        # This bot automatically creates a new guild when ran.
        if not await self.create_new_guild():
            await self.shut_down()
        if self.guild_config_dict is not None:
            await self.configure_guild()
        await self.create_new_invite()

        # Connection will only be closed once user joins and ownership is handed over


    async def create_new_guild(self):
        try:
            guild = await self.create_guild(name=NEW_GUILD_NAME)
            self.created_guild_id = guild.id
        except discord.HTTPException:
            # HTTPException will occur if guild creation fails, usually the bot is in 10 guilds.
            # This is the maximum number it can be in while still being allowed to create guilds.
            print("Guild creation failed. Check that the bot is not in 10 guilds.")
            return False
        print("Waiting for guild creation to be confirmed...")
        # Confirm that the guild has been created and is visible
        loop_count = 0
        while loop_count < 100:
            try:
                created_guild = await self.get_created_guild()
                break
            except LookupError:
                print("Failed to find guild...")
                await asyncio.sleep(0.2)
                loop_count += 1
        else:
            print("Guild creation failed.")
            return False
        print("Guild successfully created.")
        print("Total guilds joined: " + str(len(self.guilds)))
        if len(self.guilds) >= 9:
            print("Warning: GuildCreatorBot will not work if it has joined more than 10 guilds.")
        return True

    async def configure_guild(self):
        # Since the commands of guild_configuration_cog require a ctx but for this function's
        # purposes only need ctx.guild, we do this:
        ctx = type('guild_ctx',(object,),{"guild": await self.get_created_guild()})()
        print("Configuring guild...")
        await self.guild_test_cog.clear(ctx)
        await self.guild_write_cog.write_server(ctx, self.guild_config_dict)

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
        self.give_discord_interface_output(str(invite))

    def give_discord_interface_output(self, output):
        self.discord_interface.bot_outputs[id(self)] = output
        self.discord_interface.bot_output_events[id(self)].set()

    async def give_non_bot_user_owner(self, member):
        created_guild = await self.get_created_guild()
        print(member)
        print("making this member owner...")
        new_guild = await created_guild.edit(owner=member)

    async def leave_guild(self):
        guild = await self.get_created_guild()
        await guild.leave()

    async def get_created_guild(self):
        if self.created_guild_id is None:
            raise LookupError("created guild does not exist yet!")
        guild = None
        for guild in self.guilds:
            if guild.id == self.created_guild_id:
                break
        if guild is None:
            raise LookupError("No guild with id of created guild found!")
        return guild

    async def on_member_join(self, member):
        # Overrides an event functions which triggers when a new member joins a guild.
        # Member object is only associated with one guild, so this will not trigger if a member joins some
        # other guild the bot is part of
        if member.guild.id == self.created_guild_id:
            print("Member joined, making them owner!")
            await self.give_non_bot_user_owner(member)
            await self.leave_guild()
            print("Left the guild!")
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
        # TODO: unclosed connector error
        await self.close()
        print("closed connection")
        self.discord_interface.thread_done(self)
