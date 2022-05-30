import interactions
from bot import bot
from graphql.anilist import fetchUserStats
from .login import database
import time

@bot.command(
  name='consumed',
  description='consumed..',
  options=[
    interactions.Option(
      name='weebness',
      description='how many weebness have you consumed!',
      type=interactions.OptionType.SUB_COMMAND,
      options=[
        interactions.Option(
          name='user',
          description='user duh!',
          type=interactions.OptionType.USER,
          required=False,
        ),
      ],
    ),
    interactions.Option(
      name='any',
      description=f'any percent of weebness consumed!',
      type=interactions.OptionType.SUB_COMMAND,
      options=[
        interactions.Option(
          name='user',
          description='user duh!',
          type=interactions.OptionType.USER,
          required=False,
        ),
      ],
    ),
  ],
)
async def consumed(ctx: interactions.CommandContext, sub_command: str=None, user: interactions.User=None):

  await ctx.defer()
  if user == None: user = ctx.author

  data = database.find_one({'_id': int(user.id)})
  if data == None: 
    await ctx.send(f'**{user.name}** is not logged in!')
    return
 
  this = fetchUserStats(data['userId'])
  minutesWatched = this.stats.anime.minutesWatched
  if minutesWatched <= 0:
    await ctx.send('**Internal shikimori error**') 
    return

  if sub_command == 'weebness':
    if 0 < minutesWatched < 60:
      await ctx.send(f'**{user.name}** has consumed **{minutesWatched} minutes** of weebness')
    elif 60 < minutesWatched < 1440:
      await ctx.send(f'**{user.name}** has consumed **{round(minutesWatched/60, 2)} hours** of weebness')
    elif minutesWatched >= 1440:
      await ctx.send(f'**{user.name}** has consumed **{round(minutesWatched/1440, 2)} days** of weebness') 
    return

  try:
    secsPassed = time.time() - this.createdAt
    await ctx.send(f'**{user.name}** has a weebness consumed any percent of **{round(minutesWatched / round(secsPassed/1440), 2)}%**') 
  except:
    await ctx.send('**Internal shikimori error**')   