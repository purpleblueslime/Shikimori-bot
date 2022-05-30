import interactions
from bot import bot
from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
import requests
import math
from io import BytesIO
from graphql.anilist import fetchUserFavourites
from .login import database

@bot.command(
  name='favourite',
  description='favourite..',
  options=[
    interactions.Option(
      name='anime',
      description='favourite anime duh!',
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
      name='manga',
      description='favourite manga duh!',
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
      name='characters',
      description='favourite characters duh!',
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
      name='staff',
      description='favourite staff duh!',
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
async def favourite(ctx: interactions.CommandContext, sub_command: str=None, user: interactions.User=None):

  await ctx.defer()
  if user == None: user = ctx.author

  itstype = sub_command
  if itstype == None:
    await ctx.send('**Internal shikimori error**')   
    return

  data = database.find_one({'_id': int(user.id)})
  if data == None: 
    await ctx.send(f'**{user.name}** is not logged in!')
    return

  this = fetchUserFavourites(data['userId'])
  if len(this[itstype].n) == 0: 
    await ctx.send(f'**{user.name}** don\'t have any favourite {itstype}')
    return

  yAxis = (math.ceil(len(this[itstype].n)/4))*300
  if yAxis < 300: yAxis = 300
  image = Image.new('RGBA', (900,yAxis), (0,0,0,0))
  font = ImageFont.truetype('src/fonts/whitneybold.otf', 25)

  nth = 0
  for yAxis in range(0, yAxis, 300):
    for xAxis in range(0, 4*225, 225):
      coverImage = Image.open(requests.get(this[itstype].n[nth].coverImage.extraLarge, stream=True).raw)
      coverImage = ImageOps.fit(coverImage, (225,300)).convert('RGB')

      r, g, b = coverImage.getpixel((112,290))
      if r <= 180 and g <= 180 and b <= 180: textColor = 'white'  
      else: textColor = 'black' 

      draw = ImageDraw.Draw(coverImage)
      title = textwrap.shorten((this[itstype].n[nth].title.english or  this[itstype].n[nth].title.romaji), width=18, placeholder='..')
      draw.text((225/2,290), title, fill=textColor, font=font, anchor='ms')

      image.paste(coverImage, (xAxis, yAxis))
      nth += 1
      if nth == len(this[itstype].n): break 

  buffer = BytesIO()
  image.save(buffer, format='PNG', quality=90)
  buffer.seek(0)
  await ctx.send(files = [interactions.File('favourites.png', buffer)])