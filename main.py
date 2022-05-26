import asyncio
import discord
from discord.ext import commands, tasks
import socket   
import json


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', description='Relatively simple BOT', intents = intents)
hostname = socket.gethostname() 

members = []
servers = []


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    from requests import get
    ip = get('https://api.ipify.org').text
    print(f'My public IP address is: {ip}')
    for server in bot.guilds:
        servers.append(server.id)
    
    
@bot.command(pass_context = True)
async def roles(ctx, role):
    guild = ctx.message.guild
    role = discord.utils.get(guild.roles,name=role)
    print(role)
    print(role.members)
    for member in role.members:
        print(member.name)
    
def format_list(users):
    index = 0
    for user in users:
        users[index] = users[index].replace(' ', '')
        users[index] = users[index].replace('<', '')
        users[index] = users[index].replace('>', '')
        users[index] = users[index].replace('@', '')
        index = index+1
    return(users)
@bot.command(pass_context=True)
async def pending(ctx, role):
    msg = message = str(ctx.message.content).replace(':pending ', '')
    role_name = msg
    roles = [   
                699429967359901766,
                718980142248099850,
                872855873213591612,
                937144816351993886
            ]
    author = ctx.message.author
    author_roles = []
    for role in author.roles:
        author_roles.append(role.id)
    
    flag = False
    for role in author_roles:
        if role in roles:
            flag = True

    
    if flag == True:
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        embeds = msg.embeds # return list of embeds
        i = 0
        embed = embeds[0]
        flag = True
        index = 2
        embed_members = []
        while(flag): 
            try:
                users = embed.to_dict()['fields'][index]['value'].replace('>>>','')
                index = index+1
                users = users.split('\n')
                for user in users:
                    embed_members.append(user) 
            except:
                flag = False
        
        users = format_list(users= embed_members)
        member_roles = []
        guild = ctx.guild
        role = discord.utils.get(guild.roles,name=role_name)
        if role is None:
            embed = discord.Embed(title="Error", description="Role not found", color=0xFF0000)
            await ctx.send(embed=embed)
            await asyncio.sleep(3)
            msg = await ctx.channel.fetch_message(ctx.message.id)
            await msg.delete()
            return
        for member in role.members:
            if not (str(member.id)) in users:
                member_roles.append(member.id)

        data = ">>> "
        for user in member_roles:
            data += "<@"+str(user)+">"+ ' '

        message =  data + '\n' +str(len(role.members)-len(member_roles))+'/'+str(len(role.members))
        await ctx.send(message)
        print(message)
        await asyncio.sleep(3)
        msg = await ctx.channel.fetch_message(ctx.message.id)
        await msg.delete()

@bot.command(pass_context = True)
async def getEmbed(ctx):
    msg = str(ctx.message.content).replace(':getEmbed ', '')
    role = msg
    guild = ctx.guild
    role = discord.utils.get(guild.roles,name=role)
    print(role.members)
    msg = await ctx.channel.fetch_message(ctx.message.id)
    await msg.delete()

@bot.command(pass_context = True)
async def pending_multi(ctx, role):
    msg =  str(ctx.message.content).replace(':pending_multi ', '')
    roles = msg.split(',')
    for role in roles:
        await multi(ctx, role)


async def multi(ctx, role_):
    role_name = role_
    roles = [   
                699429967359901766,
                718980142248099850,
                872855873213591612,
                937144816351993886
            ]
    author = ctx.message.author
    author_roles = []
    for role in author.roles:
        author_roles.append(role.id)
    
    flag = False
    for role in author_roles:
        if role in roles:
            flag = True

    
    if flag == True:
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        embeds = msg.embeds # return list of embeds
        i = 0
        embed = embeds[0]
        flag = True
        index = 2
        embed_members = []
        while(flag): 
            try:
                users = embed.to_dict()['fields'][index]['value'].replace('>>>','')
                index = index+1
                users = users.split('\n')
                for user in users:
                    embed_members.append(user) 
            except:
                flag = False
        
        users = format_list(users= embed_members)
        member_roles = []
        guild = ctx.guild
        role = discord.utils.get(guild.roles,name=role_name)
        if role is None:
            embed = discord.Embed(title="Error", description="Role not found", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        for member in role.members:
            if not (str(member.id)) in users:
                member_roles.append(member.id)

        data = ">>> "
        for user in member_roles:
            data += "<@"+str(user)+">"+ ' '

        message =  data + '\n' +str(len(role.members)-len(member_roles))+'/'+str(len(role.members))
        await ctx.send(message)
       
bot.run('OTc4NzUyMTYwNzk3OTcwNDYy.Gk9i1r._AcqHmVr1_taFsPVGZZKPzC-glpZnSek0KOZa0')