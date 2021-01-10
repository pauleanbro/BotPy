from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import discord

client = discord.Client()

prefixArtist = ['ph$poze', 'ph$poze2', 'ph$kanye', 'ph$bcraff', 'ph$muca', 'ph$travisman', 'ph$tuecareca', 'ph$dokacareca', 'ph$trumpcareca']

thirtyMessagens = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(tuple(prefixArtist)):
        randomArtist = False
        await make(message, randomArtist)
    else:
      thirtyMessagens.append(message)
      await SendRandom()

#Function SendRandom
async def SendRandom():
  if len(thirtyMessagens) == 30:
    randomArtist = True
    await make(thirtyMessagens[random.randrange(30)], randomArtist)
    thirtyMessagens.clear()


#Function Make
async def make(text, randomArtist):
  artist = ""

  if not randomArtist:
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
  else:
    txt = text.content
    artist = random.choice(prefixArtist).split('$')
    img = Image.open('templates/{}.jpg'.format(artist[1]))
 
  if len(txt) > 490:
    txt = txt[:490]
  
  print(txt)
  w = 200 if len(txt) <= 150 else 20

  fnt = ImageFont.truetype('fonts/OpenSansEmoji.ttf', 32, encoding = 'utf-8')
  d = ImageDraw.Draw(img)

  d.text((15, w), textwrap.fill(txt, width=40), font=fnt, fill=(255,255,255), embedded_color=True)

  img.save("saves/{}.jpg".format(artist[1]), 'JPEG')

  await text.channel.send(file=discord.File("saves/{}.jpg".format(artist[1])))


client.run('text')
