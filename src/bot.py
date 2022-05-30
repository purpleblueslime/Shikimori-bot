import interactions
import ImageSending
import asyncio
import os

bot = interactions.Client(token=os.getenv('token'))

@bot.event()
async def on_ready():
  print('Online')
  while True:
    await bot.change_presence(interactions.ClientPresence(activities=[interactions.PresenceActivity(name=f'/login in {len(bot.guilds)} servers', type=interactions.PresenceActivityType.LISTENING)]))
    await asyncio.sleep(200)

    
