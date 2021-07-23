import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from discord.ext.commands import has_permissions, MissingPermissions
import time
import os
import random
import datetime
import steamfront
from datetime import timedelta
from datetime import timezone
from discord.ext.commands import CommandNotFound
import datetime
import pymongo,dns
from pymongo import MongoClient
from discord_components import DiscordComponents, Button, ButtonStyle
from key_generator.key_generator import generate



intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')
dbClient = MongoClient("mongodb+srv://D1P:D1P9812@hokuspokusdb.gehgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = dbClient["ElonWare"]
EWLogins= db["EW-Logins"]
EWEmbeds = db["EW-Embeds"]

@client.event
async def on_ready():
	DiscordComponents(client)
	print('K/D Ware bot ready!')
	
@client.command()
async def gen(ctx):
  try:user = await client.fetch_user(ctx.message.content.split(" ")[1])
  except:await ctx.send(embed = discord.Embed(description='Make sure to follow the correct format: !!gen [discord id] and/or check the id is correct'))
  
  genEmbed = discord.Embed(title=f'{user}' + f'({user.id})\n\n', timestamp = datetime.datetime.now()).set_thumbnail(url=user.avatar_url).set_footer(text='K/D Ware', icon_url = ctx.guild.icon_url).add_field(name='--------------\nSubscription length:', value='None\n--------------\n\n')
  
  genEmbed_message = await ctx.send(
    embed = genEmbed, content = ctx.message.author.id,components = [
      [Button(label='30 Days'), Button(label='Lifetime')],
      [Button(label='Gen Key', style = ButtonStyle.green), Button(label='Cancel', style = ButtonStyle.red)]
      ]
    )
    
  try:
    post = {'message_id':str(genEmbed_message.id),'costumer_id':str(user.id),'reseller_id':str(ctx.message.author.id),'sub_length':'None','key':'None'}
    EWEmbeds.insert_one(post)
  except Exception as e:
    print(e)
    await genEmbed_message.delete()
    await ctx.send(embed = discord.Embed(description='Something went wrong while accessing the database'))
    
  await ctx.message.delete()
  
@client.event
async def on_button_click(res):
  #Mongodb also stores if its an int or string so makes sure message id is int if its stored like int in db 
  if EWEmbeds.count_documents({"message_id": str(res.message.id)}) > 0:
    for dbFind in EWEmbeds.find({"message_id": str(res.message.id)}):
      message_id = dbFind["message_id"]
      costumer_id = dbFind["costumer_id"]
      reseller_id = dbFind["reseller_id"]
      sub_length = dbFind["sub_length"]
      key = dbFind["key"]
  else:
    await res.respond(embed = discord.Embed(description='Something went wrong while fetching from database'))
    return
  
  user = await client.fetch_user(costumer_id)

  
  async def update():
    await res.message.edit(embed=discord.Embed(title=f'{user}' + f'({user.id})\n\n', timestamp = datetime.datetime.now()).set_thumbnail(url=user.avatar_url).set_footer(text='K/D Ware', icon_url = res.guild.icon_url).add_field(name='--------------\nSubscription length:', value=f'{sub_length}\n--------------\n\n'))
  
  
  if res.component.label == '30 Days' and str(res.message.content) == str(reseller_id):
    sub_length = '30 Days'
    EWEmbeds.update_one(
      {"message_id":f"{res.message.id}"},
      {"$set":{"sub_length":f"30 Days"}}
    )
    await res.respond(embed = discord.Embed(description='Subscription length changed to 30 days🕒'))
    await update()
  if res.component.label == 'Lifetime' and str(res.message.content) == str(reseller_id):
    sub_length = 'Lifetime'
    EWEmbeds.update_one(
      {"message_id":f"{res.message.id}"},
      {"$set":{"sub_length":f"Lifetime"}}
    )
    await res.respond(embed=discord.Embed(description='Subscription length changed to lifetime🪦'))
    await update()
  if res.component.label == 'Gen Key' and str(res.message.content) == str(reseller_id):
    log_channel = res.guild.get_channel(866366312506720276)
  
    generated_key = generate(capital='mix') 
    
  
    post = {'expirationDate':str(datetime.timedelta(days=30) + datetime.datetime.now()),'first_login':'True','Seller':str(res.user.id),'Buyer':str(costumer_id), 'hwid':'None', 'ip':'None', 'key':str(generated_key.get_key())}
    
    await log_channel.send(embed = discord.Embed(title=f"{res.user}({res.user.id})\n\n", description = f'Subscription length: {sub_length}\nReseller ID: {reseller_id}\nCostumer ID:{costumer_id}\n\n', timestamp=datetime.datetime.now()).set_thumbnail(url=res.user.avatar_url).set_footer(text='K/D Ware', icon_url=res.guild.icon_url))
    
    await res.respond(embed=discord.Embed(description='Sending key to you now🔑'))
    
    await res.user.send(f'Key: ``{generated_key.get_key()}``\nCostumer: ``{user}``')
    
    await res.message.delete()
    
    EWLogins.insert_one(post)
  if res.component.label == 'Cancel' and str(res.message.content) == str(reseller_id):
    await res.message.delete()
    await res.respond(embed = discord.Embed(description='Key generation cancelled❌'))
  
client.run("ODY2MzI5NzI0OTQ2MDg3OTc3.YPQ-bg.YGD2MNrNiAa0lZEkW4X0kaULYqA")