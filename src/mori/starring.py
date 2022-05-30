import interactions
from bot import bot
from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageOps
import textwrap
import requests
from io import BytesIO
from graphql.anilist import searchStaff, fetchStaff

@bot.command(
  name='starring',
  description='starring..',
  options=[
    interactions.Option(
      name='artist',
      description='starring artist!',
      type=interactions.OptionType.SUB_COMMAND,
      options=[
        interactions.Option(
          name='query',
          description='search query!',
          type=interactions.OptionType.STRING,
          required=True,
          autocomplete=True,
        ),
      ],
    ),
  ],
)
async def who(ctx: interactions.CommandContext, sub_command: str, query: str=None):

  await ctx.defer()
  if query.isdigit(): this = fetchStaff(query)
  else: this = searchStaff(query)[0]

  if this == None:
    await ctx.send('**Internal shikimori error**') 
    return 

  if this.primaryOccupations[0] == 'Voice Actor': 
    itstype = 'voiceartist'
  else: 
    itstype = 'artist'

  actorImage = Image.open(requests.get(this.image.large, stream=True).raw)
  image = ImageOps.fit(actorImage, (800,480)).convert('RGB')
  image = image.filter(ImageFilter.GaussianBlur(25))

  actorImage = ImageOps.fit(actorImage, (190,280))
  image.paste(actorImage, (30,160))

  r, g, b = image.getpixel((400,40))
  if r <= 180 and g <= 180 and b <= 180: textColor = 'white'  
  else: textColor = 'black' 

  draw = ImageDraw.Draw(image)
  font = ImageFont.truetype('src/fonts/whitneybold.otf', 40)
  title = textwrap.shorten(this.name.full, width=42, placeholder='..')
  draw.text((400,40), f'Starring {this.primaryOccupations[0]}', fill=textColor, font=font, anchor='mt')
  draw.text((400,80), title, fill=textColor, font=font, anchor='mt')

  nth = 0
  for yAxis in (160, 310):
    for xAxis in (240, 350, 460, 570, 680):
      if nth >= len(this[itstype].e): break
      actImage = Image.open(requests.get(this[itstype].e[nth].n.image.extraLarge, stream=True).raw)
      actImage = ImageOps.fit(actImage, (90,130)).convert('RGB')

      r, g, b = actImage.getpixel((90/2,120))
      if r <= 180 and g <= 180 and b <= 180: textColor = 'white'  
      else: textColor = 'black' 

      draw = ImageDraw.Draw(actImage)
      
      title = textwrap.shorten((this[itstype].e[nth].n.title.english or  this[itstype].e[nth].n.title.romaji), width=12, placeholder='..')
      font = ImageFont.truetype('src/fonts/whitneybold.otf', 14)
      draw.text((90/2,115), title, fill=textColor, font=font, anchor='ms')

      role = textwrap.shorten(this[itstype].e[nth].role.capitalize(), width=12, placeholder='..')
      font = ImageFont.truetype('src/fonts/whitneybold.otf', 12)
      draw.text((90/2,125), role, fill=textColor, font=font, anchor='ms')

      image.paste(actImage, (xAxis, yAxis))
      nth += 1

  buffer = BytesIO()
  image.save(buffer, format='PNG', quality=90)
  buffer.seek(0)

  await ctx.send(files = [interactions.File(f'starring.png', buffer)])  

@bot.autocomplete('starring', 'query')
async def autoComplete(ctx: interactions.CommandContext, query: str = 'Yum'):
  enties = searchStaff(query)
  choices = []
  for e in enties:
    choices.append(interactions.Choice(name=f'{e.name.full} / {e.primaryOccupations[0]}', value=str(e.id)))

  await ctx.populate(choices)