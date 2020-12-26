from PIL import Image, ImageDraw, ImageFont
import textwrap
import discord

client = discord.Client()

prefixArtist = ['ph$poze', 'ph$poze2', 'ph$kanye', 'ph$bcraff', 'ph$muca', 'ph$travisman', 'ph$tuecareca', 'ph$dokacareca', 'ph$trumpcareca']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(tuple(prefixArtist)):
        await make(message)
 
async def make(text):
  req = text.content.split()

  try:
    prefixArtist.index(req[0])
  except ValueError:
    msg = '{0.author.mention}, esse artista não existe.'.format(text)
    await text.channel.send(msg)
    return
  else:
    artist = req[0].split('$')
    img = Image.open('templates/{}.jpg'.format(artist[1]))

  txt = ' '.join(map(str, req[1:])) 
 
  if len(txt) > 490:
    txt = txt[:490]
  
  w = 200 if len(txt) <= 150 else 20

  fnt = ImageFont.truetype('fonts/unicode.impact.ttf', 32)
  d = ImageDraw.Draw(img)

  d.text((15, w), textwrap.fill(txt, width=40), font=fnt, fill=(255,255,255))

  img.save("{}.png".format(artist[1]), 'PNG')

  await text.channel.send(file=discord.File("{}.png".format(artist[1])))

  await text.delete()

client.run('TOKEN')
