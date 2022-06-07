import asyncio
from dis import disco
import discord
from discord.ext import commands, tasks
import socket   
import json
import config


intents = discord.Intents.all()
bot = commands.Bot(command_prefix= config.prefix, description='Relatively simple BOT', intents = intents)
hostname = socket.gethostname() 

members = []
servers = []
f = open('config.json')
data = json.load(f)
print(discord.version_info)
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    from requests import get
    ip = get('https://api.ipify.org').text
    print(f'My public IP address is: {ip}')
    server_name = []
    for server in bot.guilds:
        servers.append(server.id)
        server_name.append(server.name)
    server = bot.get_guild(servers[0])
    channel = discord.utils.get(server.channels, id = 977206032872906752)
    #await channel.send(f'My public IP address is: {ip}')
    roles = []
    bot_member = server.get_member(bot.user.id)
    for role in bot_member.roles:
        if role.name != '@everyone':
            roles.append(role.name)
    print(roles)
    #await channel.send(f'My roles are: {roles}')
    print(data)
    embed = discord.Embed(title="Bot Status", description="Online", color=0x00FF00)
    embed.add_field(name="Server(s)", value= server_name, inline= True)
    embed.add_field(name="Backend Channel", value = data['backend_channel'], inline=True)
    embed.add_field(name = "Roles" , value= str(roles), inline=True)
    embed.add_field(name="IP", value=ip, inline=True)
    await channel.send(embed=embed)

@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server')
    print(member.guild.name)
    channel = discord.utils.get(member.guild.channels, id = config.template)
    member_channel = await channel.clone(name = member.name, reason = 'None')
    await member_channel.set_permissions(member, read_messages = True, send_messages = True)
    await member_channel.send(f'Welcome <@{member.id}> to {member.guild.name}')

   
@bot.slash_command(pass_context=True)
async def roles(ctx, 
                     role1 : discord.Option(discord.Role, "Role1", required = True),
                     role2 : discord.Option(discord.Role, "Role2", required = False),
                     role3 : discord.Option(discord.Role, "Role3", required = False),
                     role4 : discord.Option(discord.Role, "Role4", required = False)
                ):
    roles = [role1, role2, role3, role4]
    AuthRoles = [   
                699429967359901766,
                718980142248099850,
                872855873213591612,
                937144816351993886
            ]
    members = []
    for role in roles:
        if role is not None:
            for member in role.members:
                members.append(member.id)
    
    author = ctx.message.author
    author_roles = []
    for role in author.roles:
        author_roles.append(role.id)
    flag = False
    for role in author_roles:
        if role in roles:
            flag = True
    if flag == True:
        msg = None
        msg_list = await bot.get_channel(ctx.channel.id).history(limit=10).flatten()
        for message in msg_list:
            if (message.author.id == 616754792965865495):
                msg = message
        embeds = msg.embeds # return list of embeds
        i = 0
        embed = embeds[0]
        flag = True
        index = 1
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
        if role is None:
            embed = discord.Embed(title="Error", description="Role not found", color=0xFF0000)
            await ctx.send(embed=embed)
            await asyncio.sleep(3)
            msg = await ctx.channel.fetch_message(ctx.message.id)
            await msg.delete()
            return
        for member in members:
            if not (str(member.id)) in users:
                member_roles.append(member.id)

        data = ">>> "
        for user in member_roles:
            data += "<@"+str(user)+">"+ ' '

        message =  data + '\n' +str(len(role.members)-len(member_roles))+'/'+str(len(role.members))
        await ctx.send(message)
        await asyncio.sleep(3)
        msg = await ctx.channel.fetch_message(ctx.message.id)
        await msg.delete()

    
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
        index = 1
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
        if type(role) == str:
            guild = ctx.guild
            role = discord.utils.get(guild.roles,name=role)
        if role is None:
            embed = discord.Embed(title="Error", description="Role not found", color=0xFF0000)
            await ctx.send(embed=embed)
            await asyncio.sleep(config.pending_delete)
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
        await asyncio.sleep(config.pending_delete)
        msg = await ctx.channel.fetch_message(ctx.message.id)
        await msg.delete()

@bot.slash_command( pass_context=True, description = 'Use this for configuring the bot')
async def setup(ctx):
    embed = discord.Embed(title = "Setup Started", description = "", color= 0x09a5ed)
    user_id = ctx.author.id
    await ctx.respond( "<@"+str(user_id)+">" + "started Bot setup", )
    await asyncio.sleep(5)
    await ctx.send("```What is the $backendchannel?```")
    msg = await bot.wait_for("message", check= None)
    backend_channel = msg.content
    await ctx.send("<@"+str(user_id)+">" + "set backend channel to " + msg.content)
    await ctx.send("```What is the new user role? ($newuser_role)```")
    msg = await bot.wait_for("message", check= None)
    newuser_role = msg.content
    await ctx.send("<@"+str(user_id)+">" + "set new member role to " + msg.content)
    await ctx.send("```What is the mod role?```")
    msg = await bot.wait_for("message", check= None)
    mod_role = msg.content
    await ctx.send( "<@"+str(user_id)+">" + "set mod role to " + msg.content )
    await ctx.send("```What is the welcome message?```")
    msg = await bot.wait_for("message", check= None)
    welcome_message = msg.content
    await ctx.send("<@"+str(user_id)+">" + "set welcome message to " +  msg.content)
    await ctx.send("```What are step1 Roles?```")
    msg = await bot.wait_for("message", check= None)
    step1_roles = msg.content
    await ctx.send("<@"+str(user_id)+">" + "set step1 roles to " + msg.content)
    await ctx.send("```What are step2 Roles?```")
    msg = await bot.wait_for("message", check= None)
    step2_roles = msg.content
    await ctx.send("<@"+str(user_id)+">" + "set step2 roles to " +  msg.content)
    dic = {
        "backend_channel":backend_channel,
        "newuser_role":newuser_role,
        "mod_role":mod_role,
        "welcome_message":welcome_message,
        "step1_roles":step1_roles,
        "step2_roles":step2_roles
    }
    with open("config.json", 'r+') as f:
            f.truncate(0)
    with open('config.json', 'w') as fp:
        json.dump(dic, fp)
    
    
    embed = discord.Embed(title = "New Config", description = "", color= 0x09a5ed)
    embed.add_field(name = "Backend Channel", value = dic[backend_channel], inline= True)
    embed.add_field(name = "New User Role", value = dic[newuser_role], inline= True)
    embed.add_field(name = "Mod Role", value = dic[mod_role], inline= True)
    embed.add_field(name = "Welcome message", value = dic[welcome_message], inline= True)
    embed.add_field(name = "Step1 Roles", value = dic[step1_roles], inline= True)
    embed.add_field(name = "Step2 Roles", value = dic[step2_roles], inline= True)

    await ctx.send(embed = embed)


bot.run(config.token)