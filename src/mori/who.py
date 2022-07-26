import interactions
from bot import bot
from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageOps
import textwrap
import requests
from io import BytesIO
from graphql.anilist import fetchUsersEntry, search, fetch
from .login import database

@bot.command(
  name='who',
  description='who..',
  options=[
    interactions.Option(
      name='watch',
      description='who watch this anime!',
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
    interactions.Option(
      name='read',
      description='who read this manga!',
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
  if query.isdigit(): this = fetch(query)
  else: this = search(query)[0]

  if this.type == 'ANIME':
    itstype = 'watch'
  elif this.type == 'MANGA':
    itstype = 'read'
  else:
    await ctx.send('**Internal shikimori error**') 
    return 
  
  bannerImage = Image.open(requests.get(this.bannerImage or this.coverImage.extraLarge, stream=True).raw)
  bannerImage = ImageOps.fit(bannerImage, (800,480)).convert('RGB')
  bannerImage = bannerImage.filter(ImageFilter.GaussianBlur(25))

  coverImage = Image.open(requests.get(this.coverImage.extraLarge, stream=True).raw)
  coverImage = ImageOps.fit(coverImage, (190,280)).convert('RGB')
  bannerImage.paste(coverImage, (40,160))

  r, g, b = bannerImage.getpixel((400,40))
  if r <= 180 and g <= 180 and b <= 180: textColor = 'white'  
  else: textColor = 'black' 

  draw = ImageDraw.Draw(bannerImage)
  font = ImageFont.truetype('src/fonts/whitneybold.otf', 40)
  title = textwrap.shorten((this.title.english or  this.title.romaji), width=42, placeholder='..')
  draw.text((400,40), f'Who {itstype}', fill=textColor, font=font, anchor='mt')
  draw.text((400,80), title, fill=textColor, font=font, anchor='mt')

  inColor = this.coverImage.color
  if inColor == None: 
    r, g, b = coverImage.getpixel((0,0))
    inColor = '#{:02x}{:02x}{:02x}'.format(r,g,b)
  else:
    r, g, b = ImageColor.getcolor(inColor, 'RGB')
  if r <= 180 and g <= 180 and b <= 180: textColor = 'white'  
  else: textColor = 'black' 
  inImage = Image.new('RGBA', (530,280), f'{inColor}80')
      
  userIds = []
  userNames = {}
  await ctx.get_guild()
  for user in database.find({}):
    try:
      member = await ctx.guild.get_member(user['_id'])
      print(member)
      if member: 
        userIds.append(user['userId'])
        userNames[user['userId']] = str(member.name)
    except: pass

  if len(userIds) == 0: 
    await ctx.send(f'No one {itstype} **{this.title.english or  this.title.romaji}**')
    return
  
  entries = fetchUsersEntry(userIds, this.id)
  if len(entries) == 0: 
    await ctx.send(f'No one {itstype} **{this.title.english or  this.title.romaji}**')
    return

  topCord = 0
  font = ImageFont.truetype('src/fonts/whitneybold.otf', 30)
  fontIcon = ImageFont.truetype('src/fonts/materialiconsregular.ttf', 30)
  for entry in entries:
    textWrap = Image.new('RGBA', (530,38), f'{inColor}F2')
    draw = ImageDraw.Draw(textWrap)

    uname = textwrap.shorten(userNames[entry.user.id], width=15, placeholder='..')
    draw.text((15, 19), uname, fill=textColor, font=font, anchor='lm')
    
    if (entry.status) == 'CURRENT': 
      if (entry.progress >= 1000): entryProgress = f'~{round(entry.progress/1000)}K'
      else: entryProgress = f'~{entry.progress}'
    else: 
      entryProgress = ''

    draw.text((265, 19), f'{entry.status.capitalize()}{entryProgress}', fill=textColor, font=font, anchor='lm')
    draw.text((490, 19), str(entry.score), fill=textColor, font=font, anchor='rm')
    draw.text((490, 19), '\ue838', fill=textColor, font=fontIcon, anchor='lm')

    inImage.paste(textWrap, (0,topCord), textWrap)
    topCord += 40
    if topCord >= 40*7: break

  bannerImage.paste(inImage, (230,160), inImage)

  buffer = BytesIO()
  bannerImage.save(buffer, format='PNG', quality=90)
  buffer.seek(0)
  buffers = [buffer]

  if len(entries) > 7:
    entries = entries[7:]

    bannerImage = Image.open(requests.get(this.bannerImage or this.coverImage.extraLarge, stream=True).raw)
    bannerImage = ImageOps.fit(bannerImage, (570, (40*len(entries)) + 40)).convert('RGB')
    bannerImage = bannerImage.filter(ImageFilter.GaussianBlur(25))

    topCord = 20
    for entry in entries:
      textWrap = Image.new('RGBA', (530,38), f'{inColor}F2')
      draw = ImageDraw.Draw(textWrap)

      uname = textwrap.shorten(userNames[entry.user.id], width=14, placeholder='..')
      draw.text((15, 19), uname, fill=textColor, font=font, anchor='lm')

      if (entry.status) == 'CURRENT': 
        if (entry.progress >= 1000): entryProgress = f'~{round(entry.progress/1000)}K'
        else: entryProgress = f'~{entry.progress}'
      else: 
        entryProgress = ''

      draw.text((265, 19), f'{entry.status.capitalize()}{entryProgress}', fill=textColor, font=font, anchor='lm')
      draw.text((490, 19), str(entry.score), fill=textColor, font=font, anchor='rm')
      draw.text((490, 19), '\ue838', fill=textColor, font=fontIcon, anchor='lm')

      bannerImage.paste(textWrap, (20,topCord), textWrap)
      topCord += 40

    buffer = BytesIO()
    bannerImage.save(buffer, format='PNG', quality=90)
    buffer.seek(0)
    buffers.append(buffer)

  if this.isAdult:
    files = []
    for buffer in buffers:
      files.append(interactions.File(f'SPOILER_who{itstype}.png', buffer))
    await ctx.send('<:RimuruWET:862571444617871360> **nsfw**', files=files) 
  else: 
    files = []
    for buffer in buffers:
      files.append(interactions.File(f'who{itstype}.png', buffer))
    await ctx.send(files=files)  

@bot.autocomplete('who', 'query')
async def autoComplete(ctx: interactions.CommandContext, query: str = 'shikimori is not just a cutie'):
  enties = search(query)
  choices = []
  for e in enties:
    FORMAT = (e.format or '').replace('_', ' ')
    TITLE = textwrap.shorten((e.title.english or e.title.romaji), width=69, placeholder='..')
    choices.append(interactions.Choice(name=f'{TITLE} / {FORMAT}', value=str(e.id)))

  await ctx.populate(choices)