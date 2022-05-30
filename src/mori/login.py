import interactions
from bot import bot
from graphql.anilist import fetchUser

import os
from pymongo import MongoClient
Mongo = MongoClient(os.getenv('mongoUrl'))
database = Mongo.Rimuru.Users


@bot.modal('LoginPopup')
async def sendResponse(ctx, response: str):
  await ctx.defer()
  user = fetchUser(response)
  if user == None:
    await ctx.send(f'Login failed! **{response} not found**')
    return
  if user.id == None:
    await ctx.send(f'Login failed! **{response} not found**')
    return
  query = { '_id': int(ctx.author.id) }
  update = { '$set': {'userId': user['id']} }
  database.update(query, update, True)
  await ctx.send(f'*Login success {response}!*')

@bot.command(
  name='login',
  description='login duh!',
)
async def login(ctx: interactions.CommandContext):
  loginPopup = interactions.Modal(
    title='Login',
    custom_id='LoginPopup',
    components=[ 
      interactions.TextInput (
        style=interactions.TextStyleType.SHORT,
        label='ENTER YOUR ANILIST.CO USERNAME:',
        custom_id='TextInputResponse',
      )
    ],
  )

  await ctx.popup(loginPopup)