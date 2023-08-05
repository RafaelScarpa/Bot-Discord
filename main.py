print('-----')
import os
import nextcord as nxc
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = nxc.Intents.all()
intents.messages = True
from comandos import processar,barra

client=nxc.Client(intents=intents,default_guild_ids=[472197062554026004])

#Só pra avisar que tudo deu certo.
@client.event
async def on_ready():
  print('Versão do nextcord: '+nxc.__version__)
  print('Login como {0.user}!'.format(client))
  print('-----')

@client.event
async def on_message(message):
  #Impedir loops infinitos e ignorar mensagens.
  if message.author.bot or"[ign]"in message.content: return

  #Variáveis relevantes.
  mensagem,autor,menciona= message.content.lower().strip(),message.author,message.mentions
  async def enviar(Entrada): await message.reply(content=Entrada)
  async def enviarE(embed,content=""): await message.channel.send(embed=embed,reference=message,content=content)

  await processar(message,mensagem,autor,menciona,enviar,enviarE,client)

#Boas vindas
@client.event
async def on_member_join(membro):
  if membro.bot: return
  boasVindas=nxc.Embed(title=f"Boas vindas, {membro.display_name}!!")
  boasVindas.set_image(membro.display_avatar.url)
  await client.get_partial_messageable(654000815526117386).send(content=membro.mention,embed=boasVindas)

barra(client)

client.run(TOKEN)
