import segundario as seg #Constantes.
from replit import db #Para Score.
from datetime import datetime as dt, timedelta as td
import pypokedex as poke
import random as rand1
rand1.seed(dt.now())
delay={}
 
def score(u,soma=0,com=False):
  id=str(u.id)
  if not id in db:
    db[id]=0
  if soma:
    if com or id not in delay or delay[id]<dt.now():
      db[id]+=soma
      if not com:
        delay[id]=dt.now()+td(seconds=20)
  return db[id]

async def níveis(u,enviar):
  p = db[str(u.id)]
  if p == 200:
    u.add_roles(seg.cargo[0][0])
    await enviar("Você é um membro prata!")
  if p == 2200:
    print("aaaaaaaaaaaaaaa "+u.id)
    u.remove_roles(seg.cargo[0][0])
    u.add_roles(seg.cargo[0][1])
    await enviar("Você é um Membro Ouro!")
  
  
def fixarRand(s,limite,rep=1):
  gera=[]
  for seed in s:
    rand1.seed(seed)
    for i in range(0,rep): 
      gera.append(rand1.randint(0, limite))
  rand1.seed(dt.now())
  if len(gera)==1: gera=[0]
  return gera
      


#1
async def simples(mensagem,enviar,enviarE,msg): #Comandos que se verificam apenas.
  if mensagem=="prefixos são constritivos!": await enviar("Jamais instale `nextcord-ext-commands`!")
  if ('comando'in mensagem and'bot'in mensagem) or mensagem=='+comandos': await enviarE(seg.LstCmds[0])
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
async def avatar(m,mensagem,autor,enviar):
  if not(m) or len(mensagem)==7:
    await enviar(autor.display_avatar.url)
  else:await enviar(m[0].display_avatar.url)

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
async def nome(autor=None,enviar=None,sub=False):
  sil=rand1.randint(2,5)
  if sil==5 and rand1.randint(0,1)==1:sil-=1
  frag=[]
  for i in range(0,sil):
    frag.append(rand1.choice(seg.consoante))
    if frag[-1] and frag[-1][-1]=='u':
      frag[-1]= frag[-1]+rand1.choice(seg.vogal[:-4])
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
  if not sub:
    try:await autor.edit(nick=nom,reason="+nome")
    except:await enviar(nom)
    else:await enviar("Feito, "+nom+".")
  else:
    return nom

#6
async def gif(i,menciona,enviar,autor):
  try: n=menciona[0].nick
  except:n=False
  await enviar(seg.gif(rand1.choice(seg.gifs[i]), n, autor.display_name, rand1.choice(seg.frases[i])))

#7
async def pontos(msg,autor,menc,enviar):
  if not(menc) or msg=='+score'or msg=='+pontos':
    await enviar('Você tem '+str(score(autor))+' Score!')
  else:
    if len(menc)==1 and not menc[0].bot:
      score(menc[0])
      await enviar('Score de '+menc[0].mention+': '+str(score(menc[0])))
    else: await enviar("Mencione um humano ou ninguém para usar este comando.")

#8
async def loritta(msg,client):
  eSP= client.get_emoji(776145108689092639)
  await msg.add_reaction(eSP)

#9
async def pokemon(enviar,n=""):
  if n=="" or n not in range(1,898):
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
async def rank(enviar,aut,msg,t=1):
  async with msg.channel.typing():
    scores=[]
    for u in db.keys():
      v=db[u]
      if v>=8:scores.append([v,u])
    scores.sort(reverse=True,key=lambda par:par[0])
    await enviar(seg.ranking(scores))

#12
async def evento(s,n="Live!"):
  t=dt.now()
  t+=td(minutes=1)
  c=s.get_channel(779403680096452639)
  await s.create_scheduled_event(name= n, start_time= t, entity_type= seg.nxc.ScheduledEventEntityType.voice, channel=c)

#13
async def dado(enviar, d=6):
  if d<1:d=6
  t="🎲" if not d==2 else "🪙"
  await enviar("Seu número é "+str(rand1.randint(1,d))+". ("+t+str(d)+")")

#14
async def aposta(enviar,u,e):
  if score(u)<10:
    await enviar("Você não tem saldo de suficiente para jogar.")
    return
  b=rand1.choice(["🪨","📄","✂️"])
  resultado="Você escolheu {0}. Eu escolhi {1}.\n".format(e,b)
  if e==b:
    resultado+="É um empate! Você perde 2 Score."
    score(u,-2,True)
  if (((e=="🪨")and(b=="📄")) or
  ((e=="📄")and(b=="✂️")) or
  ((e=="✂️")and(b=="🪨"))):
    resultado+="Eu ganhei! Você perde 10 Score."
    score(u,-10,True)
  if (((b=="🪨")and(e=="📄")) or
  ((b=="📄")and(e=="✂️")) or
  ((b=="✂️")and(e=="🪨"))):
    resultado+="Eu perdi! Você ganha 10 Score!"
    score(u,10,True)
  await enviar(resultado)

#15
async def pagar(enviar,u,m,v):
  if m.bot:
    return await enviar("Isso não é aceito.")
  bal1=[score(u),score(m)]
  if v>0 or score(u)<v:
    bal2=[score(u,0-v,True), score(m,v,True)]
    await enviar(seg.pagar.format( bal1[0],bal2[0],bal1[1],bal2[1]))
  else: await enviar("Não? 🤨")

#16
async def convite(canal,i,enviar):
  c= await canal.create_activity_invite(seg.atividade[i])
  await enviar(c)

#17
async def stat(enviar,m=None):
  if m==None:
    n= await nome(sub=True)
    val=[rand1.randint(0,14),rand1.randint(0,14),rand1.randint(0,14),rand1.randint(0,14),rand1.randint(0,14)]
  else:
    n=m.display_name
    val= fixarRand([m.id],14,5)
  await enviar(seg.stat(n,str(val[0]+7),str(val[1]+7),str(val[2]+7),str(val[3]+7),str(val[4]+7)))

#18
async def palavras(enviar,q=0):
  if q>seg.lenPalavras or q<1:
    q=rand1.randint(0,seg.lenPalavras-1)
  else: q-=1
  await enviar(seg.palavras[q])



async def processar(msg,mensagem,autor,menciona,enviar,enviarE,client):

  score(autor,1) #Score
  await níveis(autor,enviar)
  
  #Verificações
  await simples(mensagem,enviar,enviarE,msg) #1
  if mensagem=='+limpar':await limpar(autor,msg,enviar) #2
  if mensagem.startswith('+avatar'):await avatar(menciona,mensagem,autor,enviar) #3
  if'nice'in mensagem: await nice(mensagem,msg) #4
  if mensagem.startswith('+nome'):await nome(autor,enviar) #5
  if mensagem.startswith('+abraço'):await gif(0,menciona,enviarE,autor) #6a
  if mensagem.startswith('+tapa'):await gif(1,menciona,enviarE,autor) #6b
  if mensagem.startswith('+score')or mensagem.startswith('+pontos'): #7
    await pontos(mensagem,autor,menciona,enviar)
  if'loritta'in mensagem or'lorita'in mensagem:
    await loritta(msg,client) #8
  if mensagem=='+pokemon'or mensagem=='+pokémon':
    await pokemon(enviar) #9
  if mensagem.startswith('+ship'):await ship(menciona,enviar) #10
  if mensagem.startswith('+rank'):await rank(enviarE,autor,msg) #11
  if mensagem=="+evento"and seg.eu(msg.author):
    await evento(msg.guild) #12
  if mensagem=="+dado": await dado(enviar) #13
  if mensagem=="+estatistica"or mensagem=="+estatística":
    await stat(enviarE,None)
  if mensagem=="+palavra": await palavras(enviar)

    
  if mensagem=='01000001': #Comando debug
    await enviar(":(")



def barra(client,Membro,Opção,Canal,Voz):
  sS=[472197062554026004]

  
  @client.slash_command("pergunta", "O algoritmo dirá seu futuro!",sS) #1a
  async def b01a(interage,pergunta:str):
    await interage.send('O Algoritmo™ diz:\n"{}"'.format(rand1.choice(seg.rsp)))

  @client.slash_command("comandos", "Quais as opções?", sS) #1b
  async def b01b(interage):
    await interage.send(embed=seg.LstCmds[1])

  @client.slash_command("avatar", "Pegue seu avatar!",sS) #3
  async def b03(interage,m:Membro=
    Opção(name="membro",
    required=False,default=[])
  ):
    if not m==[]: m=[m]
    await avatar(m,'', interage.user,interage.send)

  @client.slash_command("nome", "Um novo nome saindo do forno!",sS) #5
  async def b05(interage):
    await nome(interage.user,interage.send)

  @client.slash_command("abraco", "Calor humano, digital!",sS) #6a
  async def b06a(interage, m:Membro):
    async def enviarEB(embed):
      await interage.send(embed=embed ,content=m.mention)
    await gif(0,[m],enviarEB, interage.user)
  
  @client.slash_command("tapa", "Agressão?",sS) #6b
  async def b06b(interage, m:Membro):
    async def enviarEB(embed):
      await interage.send(embed=embed ,content=m.mention)
    await gif(1,[m],enviarEB, interage.user)

  @client.slash_command("score", "Veja seus pontos!",sS) #7
  async def b07(interage,m:Membro=
    Opção(name="membro",
    required=False,default=[])
  ):
    if not m==[]: m=[m]
    await pontos('',interage.user,m,interage.send)

  @client.slash_command("pokemon", "Um pokémon aleatório!",sS) #9
  async def b09(interage, id:int= Opção(required=False,default="")):
    await pokemon(interage.send,id)

  @client.slash_command("ship","😳",sS) #10
  async def b10(interage,m1:Membro,m2:Membro):
    await ship([m1,m2],interage.send)

  @client.slash_command("rank", "Os tagarelas!",sS) #11
  async def b11(interage):
    await interage.response.defer()
    async def enviarEB(embed):
      await interage.send(embed=embed)
    await rank(enviarEB,interage.user,interage,0)

  @client.slash_command("evento", "COMEÇA LOGO!",sS) #12
  async def b12(interage,n:str=
    Opção(name="nome",
    required=False,default="Live!")
  ):
    if seg.eu(interage.user):
      await interage.send("ok",ephemeral=True)
      await evento(interage.guild,n)
    else: await interage.send("não",ephemeral=True)

  @client.slash_command("dado", "Role e boa sorte!",sS) #13
  async def b13(interage,d:int= Opção(name="lados",required=False, default=6)):
    await dado(interage.send,d)

  @client.slash_command("aposta", "Jogue, vença, ganhe!", sS) #14
  async def b14(interage, e= Opção(name="escolha", choices=["🪨","📄","✂️"], required=True)):
    await interage.response.defer()
    await aposta(interage.send, interage.user, e)

  @client.slash_command("pagar", "Cryptomoedas.",sS) #15
  async def b15(interage, destino:Membro, valor:int):
    await interage.response.defer()
    await pagar(interage.send,interage.user,destino,valor)
 
  @client.slash_command("youtube", "Assista YouTube com a call!",sS) #16a
  async def b16a(interage, canal:Canal= Opção(required=True,channel_types=[Voz])):
    await convite(canal,0,interage.send)
  
  @client.slash_command("gartic","Gartic falso!",sS) #16b
  async def b16b(interage,canal:Canal= Opção(required=True,channel_types=[Voz])):
    await convite(canal,1,interage.send)

  @client.slash_command("estatistica","Veja seus atributos!",sS) #17
  async def b17(interage,membro:Membro=Opção(required=False,default=None)):
    async def enviarEB(embed):
      await interage.send(embed=embed)
    await stat(enviarEB,membro)

  @client.slash_command("palavra","Leia novos termos!",sS)
  async def b18(interage,id:int=Opção (required=False,default=0)):
    await palavras(interage.send,id)
