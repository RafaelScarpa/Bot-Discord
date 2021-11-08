import discord, os, keep_alive, random

activity=discord.Streaming(name="⭐CLIQUE AQUI!", url='https://www.youtube.com/watch?v=ldmckFxztzA')
client=discord.Client(activity=activity)

keep_alive.keep_alive()
  

#Só pra avisar que tudo deu certo.
@client.event
async def on_ready():
  print('-----')
  print('Login como {0.user}!'.format(client))
  print('Versão do discord.py: '+discord.__version__)
  print('-----')


#Parte legal.
@client.event
async def on_message(message):

  #Variáveis relevantes.
  mensagem,autor,canal=message.content.lower(),message.author,message.channel
  async def enviar(Entrada):
    await message.channel.send(content=Entrada, reference=message)
  async def enviar2(Entrada):
    await message.channel.send(embed=Entrada)

  #Lista de comandos.
  LstCmds= discord.Embed(color=0x00ff90,title='Comandos:',description=(
  '**"Comandos do Bot?"** (Isto.)'+
  '\n**"Hora da Live?"** (3h, sexta)'+
  '\n**"+YouTube"** (Meu canal!)'+
  '\n**"+Sobre"** (Info do bot!)'+
  '\n**"+Live"** (Assista a live!)'+
  '\n**"+Pergunta"** (Calcule seu futuro!)'+
  '\n**"+Doação"** (Me dê dinheiro que não mereço!)'+
  '\n**"+Avatar"** (Pegue a foto de alguém!)'+
  '\n**"+clear"** (Apaga 30 mensagens. (Para mods.))'+
  '\n**"+Silenciar"** (Shhhhhh! (Para mods.))'))

  #Impedir loops infinitos e ignorar mensagens.
  if autor==client.user or"[ignore]"in mensagem: return

  #Comando da lista de comandos.
  if ('comando'in mensagem and'bot'in mensagem)or mensagem=='+comandos':
    await enviar2(LstCmds)

  #Comando 1
  if "+youtube"== mensagem or"+live"==mensagem or"[btlnk]"in mensagem:
    EMBED1=discord.Embed(title="Rafael Scarpa no YouTube",url="https://youtube.co/RafaelScarpa/live",color=0x00ff90)
    await enviar2(EMBED1)
  if "+twitter"==mensagem:
    EMBED1=discord.Embed(title="Avisos do Scarpa no Twitter",url="https://twitter.com/ScarpaYT",color=0x00ff90)
    await enviar2(EMBED1)
  if "+doação"==mensagem:
    EMBED1=discord.Embed(title="Doações?! :eyes:",url="https://streamelements.com/rafaelscarpa/tip",color=0x00ff90)
    await enviar2(EMBED1)
  if "+links"==mensagem:
    EMBED1=discord.Embed(title="Website secreto?! :flushed:",url="https://Bot-Discord.rafaelscarpa.repl.co",color=0x00ff90)
    await enviar2(EMBED1)

  #Comando 2
  if'live'in mensagem and'hora'in mensagem: await enviar('Normalmente, 15:00(BRT/GMT-3) na sexta.')

  #Comando 3
  if "+clear"==mensagem:
    if autor.permissions_in(canal).manage_messages:
      await canal.purge(limit=31)
      await canal.send('30 mensangens apagadas por {}.'.format(autor.display_name),delete_after=23)
    else:await enviar('Você não tem as permissões certas.')

  #Comando 4
  if mensagem.startswith('+avatar'):
    if len(mensagem)==7:await enviar(autor.avatar_url)
    else:
      try:await enviar(message.mentions[0].avatar_url)
      except:await enviar('Marque um usuário ou envie "+avatar".')

  #Comando 5
  if "+sobre"==mensagem:await enviar('Um dia, Scarpa imaginou um tempo após sua vida. Após ele, quem diria o horário da live?! Fui criado para servir o Scopistão e substituir Scarpa.\nPara sugerir um novo comando, vá ao canal de sugestões.')

  #Comando 6
  if mensagem.startswith('+silenciar'):
    if autor.permissions_in(canal).manage_messages:
      if len(message.mentions)==1:
        try:
          await message.mentions[0].add_roles(autor.guild.get_role(800783416752472095))
          await message.mentions[0].send('Você foi silenciado no Scopistão. Contate um moderador se acha que isso é um erro.)')
          await enviar('Sucesso.')
        except: await enviar('Eu acho que deu certo.')
      elif len(message.mentions)==0:
        await enviar('Este comando aceita apenas um usuário mencionado de cada vez e só pode ser usado por um moderador. Para desfazer, tire o cargo "Silenciado" do usuário.')
      else:await enviar('Usuários demais! O limite é 1.')
    else:await enviar('Você não tem as permissões certas.')

  #Comando 7
  if'nice'in mensagem:
    #Coisas de arquivo.
    nice=open("nice.txt","r")
    Nice=int(nice.readlines()[0])
    #Adicionar número de vezes.
    Nice+=mensagem.count("nice")
    #Mensagem
    await canal.send("Contador de nice: " + str(Nice), delete_after=10)
    #Mais coisas de arquivo.
    nice.close()
    nice=open("nice.txt","w")
    nice.write(str(Nice))
    nice.close()

  #Comando 8
  if mensagem.startswith('+pergunta'):
    rsp=["Nah.","Achando que não, ein.","Não sei...","Tem uma boa chance.",":+1: Sim.","Pergunte de novo.","As aparências enganam.","Este futuro não é definido."]
    await enviar('O Algoritmo™ diz:\n"{}"'.format(rsp[random.randint(0,7)]))

  #Comando 9
  if mensagem.startswith('+nome'):
    ltr=['a','a','a','a','b','c','d','e','e','e','e','f','g','h','i','i','i','i','j','k','l','m','n','o','o','o','o','p','q','r','s','t','u','u','u','u','v','w','x','y','z']
    nom= (str(ltr[random.randint(0,41)]+ltr[random.randint(0,41)]+ltr[random.randint(0,45)]+ltr[random.randint(0,41)]+ltr[random.randint(0,41)]+ltr[random.randint(0,41)])).title()
    try: await autor.edit(nick=nom,reason="+nome")
    except: await enviar(nom)
    else: await enviar("Feito, "+nom+".")

  #Comando 10
  if client.user.mentioned_in(message):
    await enviar("salve")

client.run(os.getenv('TOKEN'))