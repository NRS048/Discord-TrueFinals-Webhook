import requests
import json
import time
import discord
from discord import Webhook
import asyncio
import aiohttp

headers = {
    "x-api-user-id":"Truefinals user ID",
    "x-api-key":"TrueFinals API Key"
}

url = "URL of your webhook"

id1 = "" #ids of your truefinals brackets (will be found inside the actual poage url, EX. https://truefinals.com/tournament/12345678abcdefgh
id2 = ""
id3 = ""

def api(bracketId):
    rs1 = requests.get("https://truefinals.com/api/v1/tournaments/" + bracketId + "/games", headers=headers)
    print(rs1)
    s1 = json.loads(rs1.text)
    rs1.close()
    return s1

def playerName(playerId, bracketId):
    rs2 = requests.get("https://truefinals.com/api/v1/tournaments/" + bracketId + "/players/" + playerId, headers=headers)
    s2 = json.loads(rs2.text)
    rs2.close()
    return s2["name"]

def bracketName(bracketId):
    rs3 = requests.get("https://truefinals.com/api/v1/tournaments/" + bracketId, headers=headers)
    s3 = json.loads(rs3.text)
    rs3.close()
    return s3["title"]

def called(fight, bracketId, P1id, P2id):
    async def function1(url):
        async with aiohttp.ClientSession() as session:
            j = api(bracketId)
            webhook = Webhook.from_url(url, session=session)
            embed = discord.Embed(title="New Match Called", color=0xF4B400)
            embed.add_field(name=bracketName(bracketId), value= j[fight]["name"])
            embed.add_field(name="Competitors:", value=playerName(P1id, bracketId) + " VS " + playerName(P2id, bracketId))
            await webhook.send(embed=embed, username="TrueFinals")

    if __name__ == "__main__":
        loop = asyncio.new_event_loop()
        loop.run_until_complete(function1(url))
        loop.close()

def active(fight, bracketId, P1id, P2id):
    async def function1(url):
        async with aiohttp.ClientSession() as session:
            h = api(bracketId)
            webhook = Webhook.from_url(url, session=session)
            embed = discord.Embed(title="New Active Match", color=0xff0000)
            embed.add_field(name=bracketName(bracketId), value= h[fight]["name"])
            embed.add_field(name="Competitors:", value=playerName(P1id, bracketId) + " VS " + playerName(P2id, bracketId))
            await webhook.send(embed=embed, username="TrueFinals")

    if __name__ == "__main__":
        loop = asyncio.new_event_loop()
        loop.run_until_complete(function1(url))
        loop.close()

def done(fight, bracketId, P1id, P2id):
    async def function1(url):
        async with aiohttp.ClientSession() as session:
            z = api(bracketId)
            w = ""
            i = 0
            while i < 2:
                if z[fight]["slots"][i]["slotState"] == "winner":
                    w = playerName(z[fight]["slots"][i]["playerID"] ,bracketId)
                i+=1
            webhook = Webhook.from_url(url, session=session)
            embed = discord.Embed(title="New completed Match", color=0x1ba300)
            embed.add_field(name=bracketName(bracketId), value= z[fight]["name"])
            embed.add_field(name="Competitors:", value=playerName(P1id, bracketId) + " VS " + playerName(P2id, bracketId))
            embed.add_field(name= w + " Wins by ", value= z[fight]["resultAnnotation"])
            await webhook.send(embed=embed, username="TrueFinals")

    if __name__ == "__main__":
        loop = asyncio.new_event_loop()
        loop.run_until_complete(function1(url))
        loop.close()

states1 = []
oldStates1 = []

states2 = []
oldStates2 = []

states3 = []
oldStates3 = []


i = 0
a = api(id1)
while i<len(a):
    states1.append(a[i]["state"])
    i += 1



i = 0
b = api(id2)
while i<len(b):
    states2.append(b[i]["state"])
    i += 1

time.sleep(3)

i = 0
c = api(id3)
while i<len(c):
    states3.append(c[i]["state"])
    i += 1

time.sleep(3)

#print(states1)
#print(states2)
#print(states3)

while True: #forever loop, need to manually stop i guess
    print("loop")
    #---------------------------------bracket1
    d = api(id1)
    oldStates1.clear()
    i = 0
    while i < len(d):
        oldStates1.append("d")
        oldStates1[i] = d[i]["state"]
        if not oldStates1[i] == states1[i]:
            match oldStates1[i]:
                case "called":
                    #print("called")
                    called(i, id1, d[i]["slots"][0]["playerID"], d[i]["slots"][1]["playerID"])
                case "active":
                    active(i, id1, d[i]["slots"][0]["playerID"], d[i]["slots"][1]["playerID"])
                case "done":
                    done(i, id1, d[i]["slots"][0]["playerID"], d[i]["slots"][1]["playerID"])
                case _:
                    #print(oldStates1[i])
                    pass
            states1[i] = oldStates1[i]
        i += 1
    #---------------------------------

    time.sleep(3)

    e = api(id2)
    oldStates2.clear()
    i = 0
    while i < len(e):
        oldStates2.append("e")
        oldStates2[i] = e[i]["state"]
        if not oldStates2[i] == states2[i]:
            match oldStates2[i]:
                case "called":
                    #print("called")
                    called(i, id2, e[i]["slots"][0]["playerID"], e[i]["slots"][1]["playerID"])
                case "active":
                    active(i, id2, e[i]["slots"][0]["playerID"], e[i]["slots"][1]["playerID"])
                case "done":
                    done(i, id2, e[i]["slots"][0]["playerID"], e[i]["slots"][1]["playerID"])
                case _:
                    #print(oldStates2[i])
                    pass
            states2[i] = oldStates2[i]
        i += 1
    #print(oldStates2)
#---------------------------------

    time.sleep(3)

    f = api(id3)
    oldStates3.clear()
    i = 0
    while i < len(f):
        oldStates3.append("f")
        oldStates3[i] = f[i]["state"]
        if not oldStates3[i] == states3[i]:
            match oldStates3[i]:
                case "called":
                    #print("called")
                    called(i, id3, f[i]["slots"][0]["playerID"], f[i]["slots"][1]["playerID"])
                case "active":
                    active(i, id3, f[i]["slots"][0]["playerID"], f[i]["slots"][1]["playerID"])
                case "done":
                    done(i, id3, f[i]["slots"][0]["playerID"], f[i]["slots"][1]["playerID"])
                case _:
                    #print(oldStates3[i])
                    pass
            states3[i] = oldStates3[i]
        i += 1
    #print(oldStates3)

    time.sleep(3)
