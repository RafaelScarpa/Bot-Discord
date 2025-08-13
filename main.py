print('-----')
import os
import nextcord as nxc
from dotenv import load_dotenv
from comandos import processar,barra,agora
from logs import inicializarLog, registrar


load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = nxc.Intents.all()
intents.messages = True
client=nxc.Client(intents=intents,default_guild_ids=[472197062554026004])


@client.event
async def on_ready():
  await inicializarLog(client)
  #Avisar que tudo deu certo.
  agora()
  print('Versão do nextcord: '+nxc.__version__)
  print(f'Login como {client.user}!')
  print('-----')


@client.event
async def on_message(msg):
  #Impedir loops infinitos e ignorar mensagens.
  if msg.author.bot or"[ign]"in msg.content: return

  await processar(msg=msg, mensagem=msg.content.lower().strip(), autor=msg.author, menciona=msg.mentions, enviar=msg.reply, client=client)

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
  if msg.author.bot: return
  await registrar(msg,0)
@client.event
async def on_message_edit(msg0,msg1=None):
  if msg0.author.bot:
    return
  else:
    await registrar(msg0,1)

#@client.event
#async def on_reaction(reação,usuário):
#  pass

barra(client)



client.run(TOKEN)
