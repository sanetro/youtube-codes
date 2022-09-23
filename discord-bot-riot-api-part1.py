# Discrod.py with RIOT API
# it searches for a player and puts in a message on the discord server
import json
from turtle import title
from unittest import result
from urllib import response
import requests
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='$') 
TOKEN_Discord = "" # Put here your discord token
TOKEN_Riot = "" # Put here your riot token

def clearNameSpaces(nameWithSpaces):
    result = ""
    for n in nameWithSpaces:
        result = result + " " + str(n)
    return result

def engine(region, name):
    if region == "eune":
        API_Riot = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + TOKEN_Riot
    if region == "euw":
        API_Riot = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + TOKEN_Riot
    response = requests.get(API_Riot)
    jsonDataSummoner = response.json()
    sName = jsonDataSummoner['name']
    sLevel = "Lvl. " + str(jsonDataSummoner['summonerLevel'])
    sIcon = "http://ddragon.leagueoflegends.com/cdn/12.13.1/img/profileicon/" + str(jsonDataSummoner['profileIconId']) + ".png"
    return (sName, sLevel, sIcon)

@bot.command()
async def eune(ctx, *nameWithSpaces):
    name = clearNameSpaces(nameWithSpaces)
    summoner = engine("eune", name)
    embed = discord.Embed(title=summoner[0], description=summoner[1], color=0xFFD500)
    embed.set_thumbnail(url=summoner[2])
    await ctx.send(embed=embed)

@bot.command()
async def euw(ctx, *nameWithSpaces):
    name = clearNameSpaces(nameWithSpaces)
    summoner = engine("euw", name)
    embed = discord.Embed(title=summoner[0], description=summoner[1], color=0xFFD500)
    embed.set_thumbnail(url=summoner[2])
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print("Ready")

bot.run(TOKEN_Discord)
