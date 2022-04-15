import segundario as seg #Constantes importantes.
from replit import db #Para Score.
from time import time as tNow
import pypokedex as poke
import random as rand1
rand1.seed(tNow())



def score(u,soma=0):
  id=str(u.id)
  if not id in db:
    db[id]=0
  if soma: db[id]+=soma
  return db[id]

def fixarRand(seed,limite):
  rand1.seed(seed)
  gera=rand1.randint(0,limite)
  rand1.seed(tNow())
  return gera
      


#1
async def simples(mensagem,enviar,enviarE): #Comandos que se verificam apenas.
  if 'comando'in mensagem and('bot'in mensagem or mensagem=='+comandos'): await enviarE(seg.LstCmds)
  if'live'in mensagem and'hora'in mensagem: await enviar(seg.hora)
  if '+youtube'==mensagem or'+live'==mensagem or'[btlnk]'in mensagem:
    await enviarE(seg.links[0])
  if mensagem.startswith('+'):
    if '+twitter'==mensagem: await enviarE(seg.links[1])
    if '+doação'==mensagem: await enviarE(seg.links[2])
    if '+links'==mensagem: await enviarE(seg.links[3])
    if "+sobre"==mensagem: await enviar(seg.sobre)
    if mensagem.startswith('+pergunta'): await enviar('O Algoritmo™ diz:\n"{}"'.format(rand1.choice(seg.rsp)))

#2
async def limpar(autor,msg,enviar):
  canal=msg.channel
  if canal.permissions_for(autor).manage_messages:
    await canal.purge(limit=31)
    await canal.send('30 mensangens apagadas por {}.'.format(autor.display_name),delete_after=23)
  else:await enviar('Você não tem as permissões certas.')

#3
async def avatar(menciona,mensagem,autor,enviar):
  if len(mensagem)==7:
    await enviar(autor.display_avatar.url)
  else:
    try: await enviar(menciona[0].display_avatar.url)
    except: await enviar('Marque um usuário ou envie "+avatar".')

#4
async def nice(mensagem,msg):
  with open("nice.txt","r") as txt:
    contador=int(txt.readlines()[0])
  #Adicionar número de vezes.
  contador+=mensagem.count("nice")
  #Mensagem
  await msg.channel.send("Contador de nice: "+str(contador), delete_after=10)
  #Fechar, abrir e fechar arquivo.
  with open("nice.txt","w") as txt:
    txt.write(str(contador))

#5
async def nome(autor,enviar):
  sil=rand1.randint(2,5)
  if sil==5 and rand1.randint(0,1)==1:sil-=1
  frag=[]
  for i in range(0,sil):
    frag.append(rand1.choice(seg.consoante))
    if frag[-1] and frag[-1][-1]=='u':
      frag[-1]= frag[-1]+rand1.choice(seg.vogal[:-3])
    else:
      frag[-1]= frag[-1]+rand1.choice(seg.vogal)
    frag[-1]= frag[-1]+rand1.choice(seg.fim)
  nom=''.join(frag) #unir
  if rand1.randint(0,1): nom=nom.replace('ãos','ões')
  if nom.startswith('ss'): nom=nom[1:]
  if nom[-1]=='n'and rand1.randint(1,4)>1: nom=nom[:-1]+'m'
  if nom.startswith('ç'): nom=rand1.choice(['c','s'])+nom[1:]
  nom= nom.replace('nb','mb').replace('np','mp')
  nom= nom.replace('nn','n').replace('nm','m')
  nom= nom.replace('çi','si').replace('çe','se')
  nom= nom.replace('ll','l').replace('sss','ss')
  nom=nom.capitalize()
  try:await autor.edit(nick=nom,reason="+nome")
  except:await enviar(nom)
  else:await enviar("Feito, "+nom+".")

#6
async def abraço(menciona,enviar,autor):
  try: n=menciona[0].nick
  except:n=False
  await enviar(seg.gifAbr(rand1.choice(seg.gifsAbr),n,autor.display_name, rand1.choice(seg.frasesAbr)))

#7
async def pontos(msg,autor,menc,enviar):
  if msg=='+score'or msg=='+pontos':
    await enviar('Você tem '+str(score(autor))+' Score!')
  else:
    if len(menc)==1 and not menc[0].bot:
      score(menc[0])
      await enviar('Score de '+menc[0].mention+': '+str(score(menc[0])))
    else: await enviar("Mencione um humano ou ninguém para usar este comando.")

#8
async def loritta(msg,client):
  eSP=client.get_emoji(776145108689092639)
  await msg.add_reaction(eSP)

#9
async def pokemon(enviar):
  n = rand1.randint(1,898)
  p = poke.get(dex=n)
  await enviar(seg.pokemon.format(n,p.name.title(),', '.join(p.types)))

#10
async def ship(candidatos,carta):
  if len(candidatos)==2:
    paixão=[]
    nomes=[]
    for apaixonado in candidatos:
      signo=apaixonado.id
      signo=''.join(format(signo,"b")[-12::])
      signo=int(signo,2)
      paixão.append(signo)
      nomes.append(apaixonado.display_name)
    amor = round(min(paixão)/max(paixão)*1000)/10
    nomeFofo=''
    if amor >= 60:
      tam0,tam1= round(len(nomes[0])/2), round(len(nomes[1])/2)
      nomeFofo=' "'+ ''.join(nomes[0][0:tam0]) + ''.join(nomes[1][-tam1::]) +'"?!'
    elif amor<15:nomeFofo=' Oh não...'
    await carta('O nível de amor é '+str(amor)+'%.'+nomeFofo)
  else:await carta('Marque 2 pessoas para usar este comando.')

#11
async def tapa(menciona,enviar,autor):
  try: n=menciona[0].nick
  except:n=False
  await enviar(seg.gifTap(rand1.choice(seg.gifsTap),n,autor.display_name,rand1.choice(seg.frasesTap)))

#12
async def rank(menc,enviar,aut,msg):
  async with msg.channel.typing():
    scores=[]
    for u in db.keys():scores.append([db[u],u])
    scores.sort(reverse=True,key=lambda par:par[0])
    await enviar(seg.ranking(scores))
  


async def processar(msg,mensagem,autor,menciona,enviar,enviarE,client):

  score(autor,1) #Score
  
  #Verificações
  await simples(mensagem,enviar,enviarE) #1
  if mensagem=='+limpar':await limpar(autor,msg,enviar) #2
  if mensagem.startswith('+avatar'):await avatar(menciona,mensagem,autor,enviar) #3
  if'nice'in mensagem: await nice(mensagem,msg) #4
  if mensagem.startswith('+nome'):await nome(autor,enviar) #5
  if mensagem.startswith('+abraço'):await abraço(menciona,enviarE,autor) #6
  if mensagem.startswith('+score')or mensagem.startswith('+pontos'): #7
    await pontos(mensagem,autor,menciona,enviar)
  if'loritta'in mensagem or'lorita'in mensagem:
    await loritta(msg,client) #8
  if mensagem=='+pokemon'or mensagem=='+pokémon':
    await pokemon(enviar) #9
  if mensagem.startswith('+ship'):await ship(menciona,enviar) #10
  if mensagem.startswith('+tapa'):await tapa(menciona,enviarE,autor) #11
  if mensagem.startswith('+rank'):await rank(menciona,enviarE,autor,msg) #12

  if mensagem=='¨bro': #Comando debug
    pass