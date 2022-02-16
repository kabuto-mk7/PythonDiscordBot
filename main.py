import discord
from discord.ext import commands
import os
import json

bot = commands.Bot(command_prefix='?')

bot.lavalink_nodes = [
    {"host": "lava.link", "port": 80, "password": "anything"},
]


@bot.event
async def on_ready():
    print('Bot is ready.')


with open("users.json", "ab+") as ab:
    ab.close()
    f = open('users.json', 'r+')
    f.readline()
    if os.stat("users.json").st_size == 0:
        f.write("{}")
        f.close()
    else:
        pass

with open('users.json', 'r') as f:
    users = json.load(f)


@bot.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)
        await add_experience(users, message.author)
        await level_up(users, message.author, message)
        with open('users.json', 'w') as f:
            json.dump(users, f)
            await bot.process_commands(message)


async def add_experience(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 0
    users[f'{user.id}']['experience'] += 6
    print(f"{users[f'{user.id}']['level']}")


async def level_up(users, user, message):
    experience = users[f'{user.id}']["experience"]
    lvl_start = users[f'{user.id}']["level"]
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f':tada: {user.mention} has reached level {lvl_end}. Congrats! :tada:')
        users[f'{user.id}']["level"] = lvl_end


@bot.command()
async def rank(ctx, member: discord.Member = None):
    userlvl = users[f'{ctx.author.id}']['level']
    await ctx.send(f'{ctx.author.mention} You are at level {userlvl}!')


bot.load_extension('dismusic')
bot.run("OTQzNDU1NDU3Mzg3ODg4NjUw.YgzTXQ.c_iNvR4TMFzE0kMRyPEyjIKmHDE")
