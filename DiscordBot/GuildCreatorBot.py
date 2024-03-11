import discord
from discord.ext.commands import Bot
import asyncio

NEW_GUILD_NAME = "new_guild"
BOT_NAME = "RCBot"
ADMIN_PERMISSIONS = {
      "name": "Administrator",
      "id": None,
      "permissions": [
        "administrator"
      ]
    }

class GuildCreatorBot(Bot):
    """
    A Discord Bot which creates and configures a Discord guild when run.
    After returning an invite link to DiscordInterface, it waits until
    a member joins the guild. Then it makes that member owner, leaves
    the guild, and shuts itself down.

    Methods
    -------
    on_ready():
        Called when the bot connects to Discord. It contains the routine
        the bot follows to create the guild.
    create_new_guild():
        Creates a new guild, and sets the created_guild_id.
    configure_guild():
        Calls GuildConfigurationCog method to configure the guild based on the guild_config_dict.
    create_new_invite():
        Creates an invite to the created guild, and provides it to DiscordInterface.
    give_discord_interface_output(output):
        Provides output to DiscordInterface.
    give_non_bot_user_owner(member):
        Gives the member ownership of the created guild.
    leave_guild():
        Leaves the created guild.
    get_created_guild():
        Returns the created guild.
    on_member_join(member):
        Method called automatically when a member joins any guild the bot is in, but only
        does anything if it's the created guild.
    make_self_admin():
        Creates an admin role and makes the bot an admin.
    on_guild_update(before, after):
        Method called automatically when any guild the bot is in updates, but only does
        anything if it's the created guild, and it was turned into a community server.
    leave_all_guilds():
        Makes the bot leave all guilds it belongs to and delete guilds it owns.
    shut_down():
        Disconnects the bot and notifies DiscordInterface that it is done.
    """
    def __init__(self, discord_interface, intents, guild_config_dict):
        super().__init__(command_prefix="//", intents=intents)
        self.discord_interface = discord_interface # Reference to the DiscordInterface which started the Bot
        self.guild_config_dict = guild_config_dict # Object containing config information for the guild.
        self.guild_configuration_cog = None # Cog containing the commands and methods for guild configuration.
        self.created_guild_id = None # Discord guild ID of the guild created by this bot

    async def on_ready(self):
        """
        Called when the bot connects to Discord. The bot tries to create a new guild.
        If guild_config_dict is not None, the bot configures the guild according to
        that dict. Finally, the bot outputs an invite link to DiscordInterface.
        """
        print("Successfully logged in as " + str(self.user))

        self.guild_configuration_cog = self.get_cog("GuildConfigurationCommands")
        # This bot automatically creates a new guild when ran.
        if not await self.create_new_guild():
            await self.shut_down()
        if self.guild_config_dict is None:
            await self.create_new_invite()  # If no config given, just send the invite.
        elif not self.guild_config_dict['community']:  # If not a community server, no need for user to manually verify.
            await self.configure_guild()
            await self.create_new_invite()
        else:  # It is a community server, manual verification needed!
            await self.create_new_invite()

        # Connection will only be closed once user joins and ownership is handed over


    async def create_new_guild(self):
        """
        Creates a new guild, and sets the created_guild_id. Handles the error of the bot
        being unable to create guilds due to being in 10 or more guilds, and ensures that
        the created guild will be accessible by get_created_guild().

        :return: True if guild creation, False otherwise.
        """
        try:
            if self.guild_config_dict is None:
                guild = await self.create_guild(name=NEW_GUILD_NAME)
            else:
                guild = await self.create_guild(name=self.guild_config_dict['name'])
            self.created_guild_id = guild.id
        except discord.HTTPException:
            # HTTPException will occur if guild creation fails, usually the bot is in 10 guilds.
            # This is the maximum number it can be in while still being allowed to create guilds.
            print("Guild creation failed. Check that the bot is not in 10 guilds.")
            return False
        print("Waiting for guild creation to be confirmed...")
        # Confirm that the guild has been created and is visible.
        # The created guild might not immediately show up in the bot's guilds, so it is important
        # to do this to avoid errors when calling get_created_guild.
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
        """
        Calls GuildConfigurationCog method to configure the guild based on the guild_config_dict.
        """
        # Since the commands of guild_configuration_cog require a ctx but for this function's
        # purposes only need ctx.guild, we do this:
        ctx = type('guild_ctx',(object,),{"guild": await self.get_created_guild()})()
        print("Configuring guild...")
        await self.guild_configuration_cog.update_server(ctx, self.guild_config_dict)

    async def create_new_invite(self):
        """
        Creates an invite to the created guild, and provides it to DiscordInterface by
        give_discord_interface_output.
        """
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
        """
        Provides output to DiscordInterface by storing it in bot_outputs,
        then notifies DiscordInterface of this result by setting the output
        event corresponding to this bot.

        :param output: The value stored in DiscordInterface's bot_outputs.
        """
        self.discord_interface.bot_outputs[id(self)] = output
        self.discord_interface.bot_output_events[id(self)].set()

    async def give_non_bot_user_owner(self, member):
        """
        Gives the member ownership of the created guild.

        :param member: The member to make owner.
        """
        created_guild = await self.get_created_guild()
        print(member)
        print("making this member owner...")
        new_guild = await created_guild.edit(owner=member)

    async def leave_guild(self):
        """
        Leaves the created guild.
        """
        guild = await self.get_created_guild()
        await guild.leave()

    async def get_created_guild(self):
        """
        Returns the created guild.

        :return: The Guild object of the created guild.
        :raise LookupError: There is no created_guild_id or the guild with that id is missing.
        """
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
        """
        Overrides an event functions which triggers when a new member joins a guild, but the function
        does nothing unless the guild is the created_guild. For non-community guilds or if there
        is no config, it then hands over ownership to the member and leave the guild. For community
        guilds, it still hands over ownership and then waits for the server to be set to community
        before configuring and leaving in on_guild_update.

        :param member: The member who just joined a guild the bot is a member of.
        """
        # A Member object is only associated with one guild, so member.guild.id can only correspond to
        # the guild the member just joined.
        if member.guild.id == self.created_guild_id:
            if self.guild_config_dict is None or not self.guild_config_dict['community']:
                print("Member joined, making them owner!")
                await self.give_non_bot_user_owner(member)
                await self.leave_guild()
                print("Left the guild!")
                await self.shut_down()
            else:
                print("Waiting for guild to be made community before configuring...")
                await self.make_self_admin()
                await self.give_non_bot_user_owner(member)
                # TODO: send message in Discord explaining what to do

                # Server will be configured in on_guild_update after guild has been set to community.

    async def make_self_admin(self):
        """
        Creates and admin role and makes self an admin.
        """
        # Since the commands of guild_configuration_cog require a ctx but for this function's
        # purposes only need ctx.guild, we do this:
        print("before...")
        created_guild = await self.get_created_guild()
        ctx = type('guild_ctx', (object,), {"guild": created_guild})()
        await self.guild_configuration_cog.update_role(ctx, ADMIN_PERMISSIONS)
        admin_role = discord.utils.get(created_guild.roles, name=ADMIN_PERMISSIONS["name"])
        await created_guild.me.add_roles(admin_role)
        print("Made self admin.")

    async def on_guild_update(self, before, after):
        """
        Overrides an event functions which triggers when the guild is updates, but the function
        does nothing unless the guild is the created_guild and the change was making it
        a community server. Method called automatically when any guild the bot is in updates,
        but only does anything if it's the created guild, and it was turned into a community server.
        Then it configures the server and leaves the guild before shutting down.

        :param before: Guild object before.
        :param after: Guild object after.
        """
        if after.id == self.created_guild_id and "COMMUNITY" in after.features:
            await self.configure_guild()
            await self.leave_guild()
            print("Left the guild!")
            await self.shut_down()

    async def leave_all_guilds(self):
        """
        Makes the bot leave all guilds it belongs to and delete guilds it owns.
        WARNING!!!! If the bot can't leave a guild due to being owner, it will delete the guild!
        This method can also take minutes to run due to Discord API limits.
        """
        print("current number of guilds:" + str(len(self.guilds)))
        print("Warning: this may take a while if many guilds are being deleted because of rate limits.")
        for guild in self.guilds:
            try:
                await guild.leave()
            except discord.HTTPException:
                await guild.delete()
        print("left all guilds")

    async def shut_down(self):
        """
        Disconnects the bot and notifies DiscordInterface that it is done.
        """
        await self.close()
        print("closed connection")
        self.discord_interface.thread_done(self)
