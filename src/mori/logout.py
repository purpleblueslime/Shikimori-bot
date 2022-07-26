import interactions
from bot import bot

from .login import database

@bot.command(
  name='logout',
  description='logout duh!',
)
async def login(ctx: interactions.CommandContext):
  database.remove({ '_id': int(ctx.author.id) })
  await ctx.send('Logged out <:SlimePensive:850655707639709696>', ephemeral=False)