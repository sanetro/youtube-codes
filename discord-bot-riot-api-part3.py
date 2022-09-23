# Discrod.py with RIOT API
# it searches for a player and puts in a message on the discord server
import json
from pydoc import describe
from turtle import title
from unittest import result
from urllib import response
import requests
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='$') 
TOKEN_Discord = "" # Put here your token
TOKEN_Riot = ""  # Put here your token





def clearNameSpaces(nameWithSpaces):
    result = ""
    for n in nameWithSpaces:
        result = result + " " + str(n)
    return result





def getProfile(region, name):
    if region == "eune":
        API_Riot = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + TOKEN_Riot
    if region == "euw":
        API_Riot = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + TOKEN_Riot
    response = requests.get(API_Riot)
    jsonDataSummoner = response.json()
    sEncryptedId = jsonDataSummoner['id']
    sName = jsonDataSummoner['name']
    sLevel = "Lvl. " + str(jsonDataSummoner['summonerLevel'])
    sIcon = "http://ddragon.leagueoflegends.com/cdn/12.13.1/img/profileicon/" + str(jsonDataSummoner['profileIconId']) + ".png"
    return (sName, sLevel, sIcon, sEncryptedId)




def fetchRanks(region, sEncryptedId):
    if region == "eune":
        API_Riot = "https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + sEncryptedId + "?api_key=" + TOKEN_Riot
    if region == "euw":
        API_Riot = "https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + sEncryptedId + "?api_key=" + TOKEN_Riot
    response = requests.get(API_Riot)
    jsonDataSummoner = response.json()
    calls = {0:"queueType", 1:"tier", 2:"rank", 3:"leaguePoints", 4:"wins", 5:"losses"}
    ranks = []
    try:
        for i in range(3):
            for j in range(6):
                ranks.append(jsonDataSummoner[i][calls[j]])
    except:
        pass
    return ranks




def fetchMasteries(region, sEncryptedId):
    limit = "5" # don't change to integer
    champions = []
    arrids, arrlevels, arrpoints, arrname, arrimgs = [], [], [], [], []
    championsURL = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
    iconURL = "http://ddragon.leagueoflegends.com/cdn/12.18.1/img/champion/"

    if region == "eune":
        API_Riot = f"https://eun1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{sEncryptedId}/top?count={limit}&api_key={TOKEN_Riot}"
    if region == "euw":
        API_Riot = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{sEncryptedId}/top?count={limit}&api_key={TOKEN_Riot}"

    # get player's champions - id, level, points of champions    
    response = requests.get(API_Riot)
    playersChampions = response.json()
    for champion in playersChampions:
        arrids.append(champion['championId'])
        arrlevels.append(champion['championLevel'])
        arrpoints.append(champion['championPoints'])
    
    # find champion by id and convert to name    
    champions_db = requests.get(championsURL).json()    
    
    # listing all champions
    [champions.append(champion) for champion in champions_db['data']]        

    # get ordered list champion names and include avatars
    for championId in arrids:
        for name in champions:
            wantedChampion = champions_db['data'][name]['key']             
            if int(wantedChampion) == int(championId): # one is str, one is int               
                arrname.append(name)
                arrimgs.append(iconURL + name + ".png")

    return [arrname, arrpoints, arrlevels, arrimgs]





@bot.command()
async def eune(ctx, *nameWithSpaces):
    # ------------------------
    #  Collecting data
    # ------------------------
    region = "eune"
    name = clearNameSpaces(nameWithSpaces)
    summoner = getProfile(region, name)
    summonerRanking = fetchRanks(region, summoner[3])
    championsMastery = fetchMasteries(region, summoner[3])

    # ------------------------
    #  Info to bot 
    # ------------------------
    embed = discord.Embed(title=summoner[0], description=summoner[1], color=0xFFD500)
    embed.set_thumbnail(url=summoner[2])

    # flex
    try:
        tmp = f"{summonerRanking[1]} {summonerRanking[2]} • LP:{summonerRanking[3]} • Wins: {summonerRanking[4]} • Losses: {summonerRanking[5]}"
        embed.add_field(name=summonerRanking[0], value=tmp, inline=False)
    except:
        embed.add_field(name="Not found", value="Player hasn't any ranked status.", inline=False)
    
    # solo duo
    try:
        tmp = f"{summonerRanking[7]} {summonerRanking[8]} • LP:{summonerRanking[9]} • Wins: {summonerRanking[10]} • Losses: {summonerRanking[11]}"
        embed.add_field(name=summonerRanking[6], value=tmp, inline=False)
    except:
        embed.add_field(name="Not found", value="Player hasn't any ranked status.", inline=False)
    
    # tft
    try:
        tmp = f"{summonerRanking[13]} {summonerRanking[14]} • LP:{summonerRanking[15]} • Wins: {summonerRanking[16]} • Losses: {summonerRanking[17]}"
        embed.add_field(name=summonerRanking[12], value=tmp, inline=False)
    except:
        embed.add_field(name="Not found", value="Player hasn't any ranked status.", inline=False)

    await ctx.send(embed=embed)

    # ------------------------
    #  Print champions sorted by highest mastery
    # ------------------------
    for i in range(len(championsMastery)+1):
        tmp = f"• Points: {str(championsMastery[1][i])[:-3]} K\n• Level Mastery: {championsMastery[2][i]}" 
        embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xFF0000)
        embed.set_thumbnail(url=championsMastery[3][i])
        await ctx.send(embed=embed)
    

    

@bot.command()
async def euw(ctx, *nameWithSpaces):
    # ------------------------
    #  Collecting data
    # ------------------------
    region = "euw"
    name = clearNameSpaces(nameWithSpaces)
    summoner = getProfile(region, name)
    summonerRanking = fetchRanks(region, summoner[3])
    championsMastery = fetchMasteries(region, summoner[3])

    # ------------------------
    #  Info to bot 
    # ------------------------
    embed = discord.Embed(title=summoner[0], description=summoner[1], color=0xFFD500)
    embed.set_thumbnail(url=summoner[2])

    # flex
    try:
        tmp = f"{summonerRanking[1]} {summonerRanking[2]} • LP:{summonerRanking[3]} • Wins: {summonerRanking[4]} • Losses: {summonerRanking[5]}"
        embed.add_field(name=summonerRanking[0], value=tmp, inline=False)
    except:
        embed.add_field(name="Not found", value="Player hasn't any ranked status.", inline=False)
    
    # solo duo
    try:
        tmp = f"{summonerRanking[7]} {summonerRanking[8]} • LP:{summonerRanking[9]} • Wins: {summonerRanking[10]} • Losses: {summonerRanking[11]}"
        embed.add_field(name=summonerRanking[6], value=tmp, inline=False)
    except:
        embed.add_field(name="Not found", value="Player hasn't any ranked status.", inline=False)
    
    # tft
    try:
        tmp = f"{summonerRanking[13]} {summonerRanking[14]} • LP:{summonerRanking[15]} • Wins: {summonerRanking[16]} • Losses: {summonerRanking[17]}"
        embed.add_field(name=summonerRanking[12], value=tmp, inline=False)
    except:
        embed.add_field(name="Not found", value="Player hasn't any ranked status.", inline=False)

    await ctx.send(embed=embed)

    # ------------------------
    #  Print champions sorted by highest mastery
    # ------------------------
    for i in range(len(championsMastery)+1):
        tmp = f"• Points: {str(championsMastery[1][i])[:-3]} K\n• Level Mastery: {championsMastery[2][i]}" 
        embed = discord.Embed(title=championsMastery[0][i], description=tmp, color=0xFF0000)
        embed.set_thumbnail(url=championsMastery[3][i])
        await ctx.send(embed=embed)





@bot.event
async def on_ready():
    print("Ready")




bot.run(TOKEN_Discord)
