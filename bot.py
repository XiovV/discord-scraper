#! /usr/bin/python3
import discord
from discord.ext import tasks, commands
import asyncio
import requests
import time 
import json
import os

# Settings
parseHubKey = "your key" 
parseHubLink_run = 'url'
parseHubLink_fetch = 'url'
botToken = 'token'
thumbnailURL = "https://i.imgur.com/2c6X56V.png"
channelID = channel-id 

# Author Icons
default = "https://i.imgur.com/cmXAse2.jpeg"
irisMemic = "https://i.imgur.com/P3tNbI6.jpg"
senadRahimic = "https://i.imgur.com/RC1Cthj.jpeg"
edinaCmanjcanin = "https://i.imgur.com/gZ3DWaU.png"
elmirBabovic = "https://i.imgur.com/KvsbWXn.png"
denisMusic = "https://i.imgur.com/WQH2OJh.png"
indiraHamulic = "https://i.imgur.com/oZ1N2vv.png"

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background.start()
        self.runs = 0

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="fit.ba/student"))
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)

    @tasks.loop(seconds=120)
    async def background(self):
        self.runs += 1
        print(f"Ran {self.runs} times.")
        params = {"api_key": parseHubKey}
        requests.post(parseHubLink_run, params=params)
        await asyncio.sleep(30)
        r = requests.get(parseHubLink_fetch, params=params)
        data = json.loads(r.text)  
        msg = await self.get_channel(channelID).history(limit=1).flatten()
        msg = msg[0]
        embeds = msg.embeds
        for embed in embeds:
            old_embed = embed.to_dict()
        channel = self.get_channel(channelID)

        # Checks if it's the same post. If no, proceed.
        if old_embed["title"] != data["title"]:
            if "content" not in data.keys():
                noPostDescription = "Obavijest nema teksta. Kliknite na naslov da otvorite u browser-u."
                embed=discord.Embed(title=data["title"], url=data["article_url"], description=noPostDescription, color=0xf6f6f6)
            elif len(data["content"])>2000:
                if "short_description" in data.keys():
                    description = f"{data['short_description']} \n\nPoruka preduga. Otvorite u browseru."
                else:
                    description = "\n\nPoruka preduga. Otvorite u browseru."
                embed=discord.Embed(title=data["title"], url=data["article_url"], description=description, color=0xf6f6f6)
            else:
                embed=discord.Embed(title=data["title"], url=data["article_url"], description=data["content"], color=0xf6f6f6)

            # Please don't look at this code.
            if "Iris" in data["author"]:
                icon = irisMemic
            elif "Senad" in data["author"]:
                icon = senadRahimic
            elif "Edina" in data["author"]:
                icon = edinaCmanjcanin
            elif "Elmir" in data["author"]:
                icon = elmirBabovic
            elif "Denis" in data["author"]:
                icon = denisMusic
            elif "Indira" in data["author"]:
                icon = indiraHamulic
            else:
                 icon = default
                
            date = data["date"]
            embed.set_author(name=data["author"], icon_url=icon)
            embed.set_footer(text=f"Posted on {date[:-1]} |  github.com/omznc/discord-scraper")
            embed.set_thumbnail(url=thumbnailURL)
            
            await channel.send("<@&796116996000579644>", embed=embed)
        
    @background.before_loop
    async def before_loop(self):
        print("Waiting until the bot starts...")
        await self.wait_until_ready()

client = MyClient()
client.run(botToken)


