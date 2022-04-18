import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(intents=intents, command_prefix='$') 
TOKEN = "" # Put here your token

@bot.command()
async def move(ctx, channel : discord.VoiceChannel, *members : discord.Member):
    for member in members:
        await member.move_to(channel)    
    print("move started")


@bot.command()
async def moveByRole(ctx, channel : discord.VoiceChannel, givenRole : discord.Role):
    for member in givenRole.members:
        try:
            await member.move_to(channel)
            print(f"User \"{member.name}\" with role \"{givenRole.name}\" moved.")
        except:
            print(f"User \"{member.name}\" with role \"{givenRole.name}\" not moved.")    
   
@bot.event
async def on_ready():
    print("Ready")

bot.run(TOKEN)





