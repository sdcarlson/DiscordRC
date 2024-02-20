import pdb
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == 485313109360115714:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name='clear')
async def clear(ctx):
    guild = ctx.guild

    for text_channel in guild.text_channels:
        await text_channel.delete()

    for voice_channel in guild.voice_channels:
        await voice_channel.delete()

    for category in guild.categories:
        await category.delete()

    await ctx.send("All text and voice channels have been deleted!")

@bot.command(name='create_text_channel')
async def create_text_channel(ctx, channel_name):
    guild = ctx.guild

    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel:
        await ctx.send(f"A channel with the name '{channel_name}' already exists!")
        return

    new_channel = await guild.create_text_channel(channel_name)
    await ctx.send(f"Text channel '{channel_name}' created successfully!")

@bot.command(name='create_voice_channel')
async def create_voice_channel(ctx, channel_name):
    guild = ctx.guild

    existing_channel = discord.utils.get(guild.voice_channels, name=channel_name)
    if existing_channel:
        await ctx.send(f"A channel with the name '{channel_name}' already exists!")
        return

    new_channel = await guild.create_voice_channel(channel_name)
    await ctx.send(f"Voice channel '{channel_name}' created successfully!")

class Parser:
    def parse(self, filename):
        lines = []
        with open(filename, 'r') as file:
            line = file.readline()
            while line:
                if line != '\n' and line[0:2] != '//':
                    lines.append(line)
                line = file.readline()
        return lines

class Interpreter:
    def __init__(self, ctx, lines):
        self.ctx = ctx
        self.lines = lines

    def get_list_strings(self, line):
        i = 0
        while line[i] != '[':
            i += 1

        strings = []
        while line[i] != ']':
            while line[i] != "'":
                i += 1
            i += 1
            string_start = i
            while line[i] != "'":
                i += 1
            i += 1
            string_end = i-1
            strings.append(line[string_start:string_end])
        return strings

    def get_var_name(self, line):
        i = 0
        while line[i] != 's':
            i += 1
        return line[0:i+1]

    async def run(self):
        for line in self.lines:
            var_name = self.get_var_name(line)
            match var_name:
                case 'text_channels':
                    channel_names = self.get_list_strings(line)
                    for channel_name in channel_names:
                        await create_text_channel(self.ctx, channel_name)
                case 'voice_channels':
                    channel_names = self.get_list_strings(line)
                    for channel_name in channel_names:
                        await create_voice_channel(self.ctx, channel_name)
                case _:
                    print(f"Invalid variable name '{var_name}'")

@bot.command(name='source')
async def source(ctx):
    await ctx.send("Sourcing")
    parser = Parser()
    await ctx.send("Parsing")
    lines = parser.parse('./.discordrc')
    interpreter = Interpreter(ctx, lines)
    await ctx.send("Interpreting")
    await interpreter.run()

TOKEN = 'MTE5MzMyMjEwNDgxNzQ1MTEwOQ.GXWA_z.zIAH8qHoNC6hSmjvnq2xJI9zRscDUMJLEOJAeI'
bot.run(TOKEN)
