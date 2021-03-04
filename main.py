import discord
import os
import keep_alive
client = discord.Client()
keep_alive.keep_alive()


#Só pra avisar que tudo deu certo.
@client.event
async def on_ready():
  print('-----')
  print('Login como {0.user}!'.format(client))
  print('Versão do discord.py: ' + discord.__version__)
  print('-----')


#Parte legal.
@client.event
async def on_message(message):

  #Só umas variáveis pra deixar bonito.
  mensagem = message.content.lower()
  autor = message.author
  canal = message.channel

  async def enviar(Entrada):
    await message.channel.send(Entrada)

  async def enviar2(Entrada):
    await message.channel.send(embed=Entrada)

  #Lista de comandos.
  LstCmnds = discord.Embed(color=0x00ffe1,title='Comandos:',description=(
  '**"Comandos do Bot?"** (Esta lista.)' +
  '\n**"Hora da Live?"** (Programação padrão do canal.)' +
  '\n**"+YouTube"** (Link para o canal do YouTube.)' +
  '\n**"+Sobre"** (Info do bot.)' +
  '\n**"+Live"** (Link para a live, se estiver acontecendo.)' +
  '\n**"+Doação"** (Link para me dar dinheiro.)' +
  '\n**"+Avatar"** (Avatar de alguém.)' +
  '\n**"+Clear"** (Apaga 30 mensagens. Apenas mods.)' +
  '\n**"+Silenciar"** (Silencia um usuário. Apenas mods.)'))

  #Impedir loops infinitos e ignorar mensagens.
  if autor == client.user or "[ign]" in mensagem:
    return

  #Comando da lista de comandos.
  if ('comando' in mensagem and 'bot' in mensagem) or mensagem == '+comandos':
    await enviar2(LstCmnds)

  #Comando 1
  if "+youtube"==mensagem or "+live"==mensagem or "[btlnk]"in mensagem:
    EMBED1 = discord.Embed(title="Rafael Scarpa no YouTube",url="https://youtube.co/RafaelScarpa/live",color=0x00ffe1)
    await enviar2(EMBED1)
  if "+twitter"==mensagem:
    EMBED1 = discord.Embed(title="Rafael Scarpa no Twitter",url="https://twitter.com/ScarpaYT",color=0x00ffe1)
    await enviar2(EMBED1)
  if "+doação"==mensagem:
    EMBED1 = discord.Embed(title="Doações?! :eyes:", url="https://streamelements.com/rafaelscarpa/tip",color=0x00ffe1)
    await enviar2(EMBED1)
  if "+links" == mensagem:
    EMBED1 = discord.Embed(title="Website secreto?! :flushed:",url="https://Bot-Discord.rafaelscarpa.repl.co",color=0x00ffe1)
    await enviar2(EMBED1)

  #Comando 2
  if 'live' in mensagem and 'hora' in mensagem:
    await enviar('Normalmente, 15:00(BRT/GMT-3) na sexta.')

  #Comando 3
  if "+clear"==mensagem:
    if autor.permissions_in(canal).manage_messages:
      await canal.purge(limit=31)
      await canal.send('30 mensangens apagadas por {0}.'.format(autor.display_name),delete_after=23)
    else:
      await enviar('Você não tem as permissões certas.')

  #Comando 4
  if mensagem.startswith('+avatar'):
    if mensagem.lenght==7:
      await enviar(autor.avatar_url)
    else:
      try:
        await enviar(message.mentions[0].avatar_url)
      except:
        await enviar('Marque um usuário ou envie só "+avatar".')

  #Comando 5
  if "sobre"==mensagem:
    await enviar('Fui criado para servir o Scopistão e substituir Scarpa. Para sugerir um comando, vá ao canal de sugestões.')

  #Comando 6
  if mensagem.startswith('+silenciar'):
    if autor.permissions_in(canal).manage_messages:
      if len(message.mentions) == 1:
        try:
          await message.mentions[0].add_roles(autor.guild.get_role(800783416752472095))
          await message.mentions[0].send('Você foi silenciado no Scopistão. Contate um moderador se acha que isso é um erro.)')
          await enviar('Sucesso.')
        except:
          await enviar('Eu acho que deu certo.')
      elif len(message.mentions)==0:
        await enviar('Este comando aceita apenas um usuário mencionado de cada vez e só pode ser usado por um moderador. Para desfazer, tire o cargo "Silenciado" do usuário.')
      else: await enviar('Usuários demais! O limite é 1.')
    else:
      await enviar('Você não tem as permissões certas.')

  #Comando 7
  if 'nice' in mensagem:
    nice2 = open("nice.txt", "r")
    nice = int(nice2.readlines()[0])
    nice += 1
    await enviar(str(nice))
    nice1 = open("nice.txt", "w")
    nice1.write(str(nice))
    nice1.close()
    nice2.close()


client.run(os.getenv('TOKEN'))