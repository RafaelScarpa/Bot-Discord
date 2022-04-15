import os
import nextcord as nxc
from comandos import processar
from segundario import activity

#Manter o bot vivo.
import keep_alive
keep_alive.keep_alive()

#Iniciar bot com atividade.
client=nxc.Client(activity=activity)

#Só pra avisar que tudo deu certo.
@client.event
async def on_ready():
  print('-----')
  print('Versão do nextcord: '+nxc.__version__)
  print('Login como {0.user}!'.format(client))
  print('-----')


@client.event
async def on_message(message):
  #Impedir loops infinitos e ignorar mensagens.
  if message.author.bot or"[ign]"in message.content: return
    
  #Variáveis relevantes.
  mensagem,autor,menciona= message.content.lower(),message.author,message.mentions
  async def enviar(Entrada): await message.channel.send(content=Entrada,reference=message)
  async def enviarE(Entrada): await message.channel.send(embed=Entrada,reference=message)

  await processar(message,mensagem,autor,menciona,enviar,enviarE,client)


client.run(os.getenv('TOKEN'))