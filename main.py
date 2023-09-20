print('-----')
import os
import nextcord as nxc
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = nxc.Intents.all()
intents.messages = True
from comandos import processar,barra
from logs import inicializarLog, registrar

client=nxc.Client(intents=intents,default_guild_ids=[472197062554026004])

#Só pra avisar que tudo deu certo.
@client.event
async def on_ready():
  print('Versão do nextcord: '+nxc.__version__)
  print('Login como {0.user}!'.format(client))
  await inicializarLog(client)
  print('-----')

@client.event
async def on_message(msg):
  #Impedir loops infinitos e ignorar mensagens.
  if msg.author.bot or"[ign]"in msg.content: return

  #Variáveis relevantes.
  mensagem,autor,menciona= msg.content.lower().strip(),msg.author,msg.mentions
  async def enviar(Entrada): await msg.reply(content=Entrada)
  async def enviarE(embed,content=""): await msg.channel.send(embed=embed,reference=msg,content=content)

  await processar(msg,mensagem,autor,menciona,enviar,enviarE,client)

#Boas vindas
@client.event
async def on_member_join(membro):
  if membro.bot: return
  boasVindas=nxc.Embed(title=f"Boas vindas, {membro.display_name}!!")
  boasVindas.set_image(membro.display_avatar.url)
  await client.get_partial_messageable(654000815526117386).send(content=membro.mention,embed=boasVindas)

#log
@client.event
async def on_message_delete(msg):
  if msg.author.bot:
    return
  else:
    await registrar(msg,0)
@client.event
async def on_message_edit(msg0,msg1=None):
  if msg0.author.bot:
    return
  else:
    await registrar(msg0,1)

barra(client)

client.run(TOKEN)
