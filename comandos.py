import os, asyncio
import nextcord as nxc
import segundario as seg #Constantes.
from datetime import datetime as dt, timedelta as td
import random
from time import time
from db import lerDB
import translators as ts
import wikipedia
import pypokedex as poke
from LeeSpork1 import ship as Ship
import spotify
from inventário import inv as Inventário
random.seed(time())
delay={}
print(dt.now().strftime("%d-%m-%Y %H:%M:%S"))



async def níveis(u:int,enviar,msg):
  p = lerDB(u.id)
  if p >= 2200 and msg.guild.get_role(seg.cargo[1]) not in u.roles:
    print("aaaaaaaaaaaaaaa "+str(u.id))
    await u.remove_roles(msg.guild.get_role(seg.cargo[0]))
    await u.add_roles(msg.guild.get_role(seg.cargo[1]))
    await enviar("Você está no nível Ouro!")
  elif p >= 200 and msg.guild.get_role(seg.cargo[0]) not in u.roles:
    await u.add_roles(msg.guild.get_role(seg.cargo[0]))
    await enviar("Você está no nível Prata!")
    
def fixarRand(s:int,limite:int,rep=1):
  gera=[]
  for seed in s:
    random.seed(seed)
    for i in range(0,rep): 
      gera.append(random.randint(0, limite))
  random.seed(time())
  if len(gera)==1: gera=[0]
  return gera



#1
async def simples(mensagem:str,enviar,enviarE,msg): #Comandos que se verificam apenas.
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
    if "+queanime"==mensagem: await enviar("<@!594211566581186646> que anime é esse?")
    if mensagem.startswith('+pergunta'): await enviar(seg.prgt[seg.eng(msg.author)].format(random.choice(seg.rsp)))

#2
async def limpar(autor,msg,enviar,limit:int=31):
  canal=msg.channel
  if canal.permissions_for(autor).manage_messages:
    await canal.purge(limit=limit)
    await canal.send(str(limit)+' mensangens apagadas por {}.'.format(autor.display_name),delete_after=23)
  else:await enviar(['Você não tem as permissões certas.','Wrong permissions.'][seg.eng(autor)])

#3
async def avatar(m,mensagem:str,autor,enviar):
  if not(m) or len(mensagem)==7:
    await enviar(autor.display_avatar.url)
  else:await enviar(m[0].display_avatar.url)

#4
async def nice(mensagem:str,msg):
  with open("nice.txt","r") as txt:
    contador=int(txt.readlines()[0])
  #Adicionar número de vezes.
  contador+=mensagem.count("nice")
  #Mensagem
  await msg.channel.send(seg.nice[seg.eng(msg.author)].format(str(contador)), delete_after=10)
  #Fechar, abrir e fechar arquivo.
  with open("nice.txt","w") as txt:
    txt.write(str(contador))

#5
async def nome(autor=None,enviar=None,sub:bool=False):
  quantidade=random.randint(2,5)
  if quantidade==5 and random.randint(0,1)==1:quantidade-=1
  fragmento=[]
  for i in range(0,quantidade):
    fragmento.append(random.choice(seg.consoante))
    if fragmento[-1] and fragmento[-1][-1]=='u':
      fragmento[-1]= fragmento[-1]+random.choice(seg.vogal[:-4])
    else:
      fragmento[-1]= fragmento[-1]+random.choice(seg.vogal)
    fragmento[-1]= fragmento[-1]+random.choice(seg.fim)
  nom=''.join(fragmento) #unir
  if random.randint(0,1): nom=nom.replace('ãos','ões')
  if nom.startswith('ss'): nom=nom[1:]
  if nom[-1]=='n'and random.randint(1,4)>1: nom=nom[:-1]+'m'
  if nom.startswith('ç'): nom=random.choice(['c','s'])+nom[1:]
  nom= nom.replace('nb','mb').replace('np','mp')
  nom= nom.replace('nn','n').replace('nm','m')
  nom= nom.replace('çe','se').replace('sss','ss')
  nom=nom.capitalize()
  if not sub:
    try:await autor.edit(nick=nom,reason="+nome")
    except:await enviar(nom)
    else:
      prefixo= "Done, " if seg.eng(autor) else "Feito, "
      await enviar(prefixo+nom+".")
  else:
    return nom

#6
async def gif(i:int,menciona,enviar,autor):
    try: nick=menciona[0].nick
    except:nick=False
    await enviar(
      seg.gif(random.choice(seg.gifs[i]), nick, autor.display_name, random.choice(seg.frases[i])[seg.eng(autor)])
    )

#7
async def pontos(msg,autor,menção,enviar):
  if not(menção) or msg in ['+score','+pontos']:
    await enviar('Você tem '+str(lerDB(autor.id))+' Score!')
  else:
    if len(menção)==1 and not menção[0].bot:
      lerDB(menção[0].id)
      await enviar('Score de '+menção[0].mention+': '+str(lerDB(menção[0].id)))
    else: await enviar("Mencione um humano ou ninguém para usar este comando.")

#8
async def loritta(msg,client):
  scarpaPara= client.get_emoji(776145108689092639)
  await msg.add_reaction(scarpaPara)

#9
async def pokemon(enviar,numero:int=""):
  if numero=="" or numero not in range(1,905):
    numero = random.randint(1,905)
  p = poke.get(dex=numero)
  await enviar(seg.pokemon.format(numero,p.name.title(),', '.join(p.types)))

#10
async def ship(menções,enviar):
  if len(menções)==2:
    try:
      await enviar(Ship(
        menções[0].display_name,int(menções[0].id),
        menções[1].display_name,int(menções[1].id))
      )
    except:
      try:
        await enviar(Ship(
          "Amor verdadeiro",int(menções[0].id),
          "Amor verdadeiro",int(menções[1].id))
        )
      except: await enviar("Erro!")
  else: await enviar('Selecione 2 pessoas para usar este comando.')

#11
async def rank(enviar,msg,autor):
  async with msg.channel.typing():
    scores=lerDB(tudo=1)
    scores= sorted(scores.items(),reverse=True,key=lambda par:par[1])
    await enviar(seg.ranking(scores,seg.eng(autor)))
    return

#12
async def evento(servidor,n:str="Live!"):
  tempo=dt.now()
  tempo+=td(hours=3,minutes=6)
  canal=servidor.get_channel(779403680096452639)
  await servidor.create_scheduled_event(name=n, start_time=tempo, entity_type= seg.nxc.ScheduledEventEntityType.voice, channel=c)

#13
async def dado(enviar,lados:int=6,mensagem=None):
  if mensagem !=None:
    for i in ["+dado","+dice","+die"]: mensagem=mensagem.replace(i,"")
    try: lados=int(mensagem.strip())
    except: pass
  if lados<1:lados=6
  texto="🎲" if not lados==2 else "🪙"
  await enviar("Seu número é "+str(random.randint(1,lados))+". ("+texto+str(lados)+")")

#14
async def aposta(enviar,usuário,escolha,mensagem=None):
  en=eng(usuário)
  id_=usuário.id
  if lerDB(id_)<10:
    await enviar(["Você não tem saldo suficiente para jogar.","You don't have enough Score to play."][en])
    return
  contra=random.choice(["🪨","📄","✂"])
  resultado=(["Você escolheu {0}. Eu escolhi","You chose {0}. I chose"][en] +" {1}.\n").format(escolha,contra)
  if escolha==contra:
    resultado+=["É um empate! Você perde 1 Score.","It's a tie! You lose 1 Score."][en]
    lerDB(id_,-1,True)
  if (escolha=="🪨" and contra=="📄") or (escolha=="📄" and contra=="✂") or (escolha=="✂" and contra=="🪨"):
    resultado+=["Eu ganhei! Você perde 10 Score.","I won! You lose 10 Score."][en]
    lerDB(id_,-10,True)
  if (contra=="🪨" and escolha=="📄") or (contra=="📄" and escolha=="✂") or (contra=="✂" and escolha=="🪨"):
    resultado+=["Eu perdi! Você ganha 10 Score.","I lost! You win 10 Score."][en]
    lerDB(id_,10,True)
  await enviar(resultado)

#15
async def pagar(enviar,autor,destino,valor:int,en):
  if destino.bot:
    return await enviar("Isso não é aceito.")
  balanço1=[lerDB(autor.id),lerDB(destino.id)]
  if valor>0 and balanço1[0]>valor:
    balanço2=[lerDB(autor.id,-valor,True),lerDB(destino.id,valor,True)]
    await enviar(seg.pagar(en).format(balanço1[0],balanço2[0],balanço1[1],balanço2[1]))
  else: await enviar("Não? 🤨")

#16
async def stat(enviar,membro=None):
  if membro==None:
    texto= await nome(sub=True)
    valores=[random.randint(0,14),random.randint(0,14),random.randint(0,14),random.randint(0,14),random.randint(0,14)]
  else:
    texto=membro.display_name
    valores= fixarRand([membro.id],14,5)
  await enviar(seg.stat(texto,str(valores[0]+7),str(valores[1]+7),str(valores[2]+7),str(valores[3]+7),str(valores[4]+7)))

#17
async def palavras(enviar,numero:int=0):
  if numero>seg.lenPalavras or numero<1:
    numero=random.randint(0,seg.lenPalavras-1)
  else: numero-=1
  await enviar(seg.palavras[numero])

#18
async def tradução(msg,destino='pt',quantidade:int=5,especifico=None):
  canal=msg.channel
  conteúdos=[]
  autores=[]
  if especifico==None:
    async for i in canal.history(limit=quantidade, oldest_first=False):
      conteúdos.insert(0,nxc.utils.escape_markdown(i.clean_content))
      autores.insert(0,nxc.utils.escape_markdown(i.author.display_name))
  else:
    conteúdos=[nxc.utils.escape_markdown(especifico.clean_content)]
    autores=[nxc.utils.escape_markdown(especifico.author.display_name)]
  texto=""
  for i in range(quantidade):
    texto+="\n**`"+autores[i]+"`**: "+ts.translate_text(query_text=conteúdos[i]if conteúdos[i]!=""else"[]",to_language=destino)
  await msg.send(texto[1:],ephemeral=True)

#19
async def youtubemusic(msg,enviar):
  await asyncio.sleep(1.5)
  try:
    embed=msg.embeds[0]
  except: print("Erro de youtubemusic(): Sem embed.")
  try:
    link=spotify.pesquisar(embed.title,embed.author.name)
    await enviar(link)
  except: print("Erro de youtubemusic(): Outro.")

#20
async def itens(enviar,autor,indice:int=None,ação=None,mensagem=None):
  if mensagem!=None:
    mensagem=mensagem.split(" ",1)[1].strip()
    try:indice=int(mensagem)
    except: pass
  await Inventário(enviar,autor.id,indice,ação,en=seg.eng(autor))

#21
async def wiki(enviar,mensagem:str,l:str="pt"):
  wikipedia.set_lang(l)
  prompt=mensagem.removeprefix("+wiki").removeprefix("+wikipédia").removeprefix("+wiki").strip()
  try:
    await enviar(wikipedia.page(prompt).url)
  except wikipedia.exceptions.PageError:
    await enviar(":x:")

#22
async def música(enviar,mensagem:str):
  link=spotify.pesquisar(mensagem.removeprefix("+spotify").strip())
  await enviar(link)

#23
async def serverinfo(enviar,link:str,client):
  convite=await client.fetch_invite(link)
  if convite.expires_at==None:
    content="Não há data de vencimento para este convite.\n"
  else:
    content="Vencimento do convite: {0}\n".format(convite.expires_at.strftime("%d/%m/%Y às %H:%M:%S"))
  content+="Canal associado ao convite\n- Nome: `{0}` ({1})\n- Data de criação: {2}\n".format(convite.channel.name, convite.channel.mention, convite.channel.created_at.strftime("%d/%m/%Y às %H:%M:%S"))
  servidor=convite.guild
  if servidor==None:
    content+="Não há servidor associado a este convite."
  else:
    content+="Servidor\n- Nome: `{0}` (id {1})\n- Descrição: `{2}`\n- Criado: {3}.".format(servidor.name,servidor.id,servidor.description,servidor.created_at.strftime("%d/%m/%Y às %H:%M:%S"))
    content+="\n- Icone: {0}\n- Banner 1: {1}\n- Banner 2: {2}".format(str(servidor.icon),str(servidor.banner),str(servidor.splash))
  await enviar(content)



async def processar(msg,mensagem,autor,menciona,enviar,enviarE,client):

  lerDB(autor.id,1) #Score
  await níveis(autor,enviar,msg)
  
  #Verificações
  await simples(mensagem,enviar,enviarE,msg) #1
  if mensagem in ['+limpar','+clear']:await limpar(autor,msg,enviar) #2
  if mensagem.startswith(('+avatar','+pfp')):await avatar(menciona,mensagem,autor,enviar) #3
  if'nice'in mensagem: await nice(mensagem,msg) #4
  if mensagem.startswith(('+nome','+name')):await nome(autor,enviar) #5
  if mensagem.startswith(('+abraço','+hug')):await gif(0,menciona,enviarE,autor) #6a
  if mensagem.startswith(('+tapa','+slap')):await gif(1,menciona,enviarE,autor) #6b
  if mensagem.startswith(('+score','+pontos')):await pontos(mensagem,autor,menciona,enviar) #7
  if'loritta'in mensagem or'lorita'in mensagem:await loritta(msg,client) #8
  if mensagem in ['+pokemon','+pokémon']:await pokemon(enviar) #9
  if mensagem.startswith('+ship'):await ship(menciona,enviar) #10
  if mensagem in ['+rank','+ranking']:await rank(enviarE,msg,autor) #11
  if mensagem in ["+evento","+event"]and seg.eu(autor):await evento(msg.guild) #12
  if mensagem.startswith(("+dado","+die","dice")):await dado(enviar,mensagem=mensagem) #13
  if mensagem in ["+estatistica","+estatística","+stats"]:await stat(enviarE,None) #16
  if mensagem in ["+palavra","+word"]:await palavras(enviar) #17
  if mensagem=="+tradução":await tradução(interage,destino="pt") #18a
  if mensagem=="+translate":await tradução(interage,destino="en") #18b
  if "music.youtube.com/" in mensagem:await youtubemusic(msg,enviar) #19
  if mensagem=="+item":await itens(enviarE,autor,ação=0) #20a
  if mensagem.startswith(("+comer","+eat")):await itens(enviarE,autor,ação=1,mensagem=mensagem) #20b
  if mensagem.startswith(("+vender","+sell")):await itens(enviarE,autor,ação=2,mensagem=mensagem) #20c
  if mensagem.startswith("+wiki"):await wiki(enviar,mensagem) #21
  if mensagem.startswith("+spotify"):await música(enviar,mensagem) #22

  if mensagem=='+encerrar bot agora' and seg.eu(autor): #Comando debug
    os.system('start cmd /c cd "C:\Bot Discord" && python main.py')
    print("Reiniciando! :wave:")
    sys.exit(0)



def barra(client):
  Opção=nxc.SlashOption
  
  @client.slash_command(name="pergunta", description="O algoritmo dirá seu futuro.",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'ask'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'The algorithm will tell you your future.')
  ) #1a
  async def b01a(interage, pergunta:str):
    await interage.send(seg.prgt[seg.eng(interage.user)].format(random.choice(seg.rsp)))

  @client.slash_command(name="comandos", description="Quais as opções?",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'commands'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'What can I do?')
  ) #1b
  async def b01b(interage):
    await interage.send(embed=seg.LstCmds[1])

  @client.slash_command(name="limpar", description="😬⏪")
  async def b02(interage,i:int=
    Opção(min_value=1,max_value=100,required=False,default=30)
  ):
    await limpar(interage.user,interage,interage.send,i)

  @client.slash_command(name="avatar", description="Pegue seu avatar!",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'pfp'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Get it here!')
  ) #3
  async def b03(interage,m:nxc.Member=
    Opção(name="membro",required=False,default=[])
  ):
    if not m==[]: m=[m]
    await avatar(m,'', interage.user,interage.send)

  @client.slash_command(name="nome", description="Um novo nome saindo do forno!",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'name'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'A brand new name hot out of the oven!')
  ) #5
  async def b05(interage):
    await nome(interage.user,interage.send)

  @client.slash_command(name="abraco", description="Calor humano, digital!",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'hug'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Human warmth, digitally!')
  ) #6a
  async def b06a(interage, m:nxc.Member):
    async def enviarEB(embed):
      await interage.send(embed=embed)
    await gif(0,[m],enviarEB,interage.user)
  
  @client.slash_command(name="tapa", description="Agressão?",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'slap'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Aggression?')
  ) #6b
  async def b06b(interage, m:nxc.Member):
    async def enviarEB(embed):
      await interage.send(embed=embed)
    await gif(1,[m],enviarEB,interage.user)

  @client.slash_command(name="score", description="Veja seus pontos!",
    description_localizations=dict.fromkeys(['en-US',"en-GB"],'Check your score!')
  ) #7
  async def b07(interage,m:nxc.Member=
    Opção(name="membro",required=False,default=[])
  ):
    if not m==[]: m=[m]
    await pontos('',interage.user,m,interage.send)

  @client.slash_command(name="pokemon", description="Um pokémon aleatório!",
    description_localizations=dict.fromkeys(['en-US',"en-GB"],'A random pokémon!')
  ) #9
  async def b09(interage, id_:int=
    Opção(required=False,default="")
  ):
    await pokemon(interage.send,id_)

  @client.slash_command(name="ship", description="😳") #10
  async def b10(interage,m1:nxc.Member,m2:nxc.Member):
    await ship([m1,m2],interage.send)

  @client.slash_command(name="rank", description="Os tagarelas!",
    description_localizations=dict.fromkeys(['en-US',"en-GB"],'The babblers!')
  ) #11
  async def b11(interage):
    await interage.response.defer()
    async def enviarEB(embed):
      await interage.send(embed=embed)
    await rank(enviarEB,interage,interage.user)

  @client.slash_command(name="evento", description="COMEÇA LOGO!") #12
  async def b12(interage,n:str=
    Opção(name="nome", required=False,default="Live!")
  ):
    if seg.eu(interage.user):
      await interage.send("ok",ephemeral=True)
      await evento(interage.guild,n)
    else: await interage.send("não",ephemeral=True)

  @client.slash_command(name="dado", description="Role e boa sorte!",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'dice'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Roll and good luck!')
  ) #13
  async def b13(interage,d:int=
    Opção(name="lados",required=False, default=6)
  ):
    await dado(interage.send,d)

  @client.slash_command(name="aposta", description="Jogue, vença, ganhe!",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'bet'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Play, win, earn!')
  ) #14
  async def b14(interage, e=
    Opção(name="escolha", choices=["🪨","📄","✂"], required=True)
  ):
    await interage.response.defer()
    await aposta(interage.send, interage.user, e)

  @client.slash_command(name="pagar", description="Cryptomoedas.",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'pay'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Cryptocurrencies.')
  ) #15
  async def b15(interage, destino:nxc.Member, valor:int):
    await interage.response.defer()
    await pagar(interage.send,interage.user,destino,valor,eng(interage.author))

  @client.slash_command(name="estatistica", description="Veja seus atributos!",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'stats'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Find your attributes!')
   ) #16
  async def b16(interage,membro:nxc.Member=
    Opção(required=False,default=None)
  ):
    async def enviarEB(embed):
      await interage.send(embed=embed)
    await stat(enviarEB,membro)

  @client.slash_command(name="palavra", description="Leia novos termos!") #17
  async def b17(interage, id_:int=
    Opção(required=False,default=0,min_value=1,max_value=320139,name='id')
  ):
    await palavras(interage.send,id_)

  @client.slash_command(name="tradutor", description="Traduza!",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'translate')
  ) #18
  async def b18(interage,
    e=Opção(name="lingua",choices={"English":"en","Português":"pt"},required=True,
      name_localizations=dict.fromkeys(['en-US',"en-GB"],'language')
    ),
    v:int=Opção(name="quant", required=False, default=5, max_value=15, min_value=1)
  ):
    await interage.response.defer(ephemeral=True)
    if v not in range(1,16): v=5
    await tradução(interage,destino=e,quantidade=v)
  
  @client.slash_command(name="item",description="Ganhe!",
    description_localizations=dict.fromkeys(['en-US',"en-GB"],'Win!')
  ) #20a
  async def b20a(interage):
    await Inventário(interage.send,interage.user.id,ação=0,en=seg.eng(interage.user))

  @client.slash_command(name="comer",description="Você pode fazer isso se quiser!",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'eat'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'You can do this if you want!')
  ) #20b
  async def b20b(interage, indice:int=
    Opção(min_value=1,required=True,name="indice",
     name_localizations=dict.fromkeys(['en-US',"en-GB"],'index')
    )
  ):
    if indice<1: indice=None
    await Inventário(interage.send,interage.user.id,ação=1,indice=indice,en=seg.eng(interage.user))

  @client.slash_command(name="vender",description="Troque itens por score!",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'sell'), description_localizations=dict.fromkeys(['en-US',"en-GB"],'Earn score for items!')
  ) #20c
  async def b20b(interage, indice:int=
    Opção(min_value=1,required=True,name="indice",
      name_localizations=dict.fromkeys(['en-US',"en-GB"],'index')
    )
  ):
    if indice<1: indice=None
    await Inventário(interage.send,interage.user.id,ação=2,indice=indice,en=seg.eng(interage.user))

  @client.slash_command(name="wiki", description="Responda, rápido.",
    description_localizations=dict.fromkeys(['en-US',"en-GB"],'Answers, quick.')) #21
  async def b21(interage,
    n:str=Opção(required=True,name="nome",
      name_localizations=dict.fromkeys(['en-US',"en-GB"],'name')
    ),
    l=Opção(name="lingua",choices={"English":"en","Português":"pt"},required=True,
      name_localizations=dict.fromkeys(['en-US',"en-GB"],'language')
    )
  ):
    await interage.response.defer(ephemeral=False)
    await wiki(interage.send,n,l)

  @client.slash_command(name="spotify", description="🎵🎶") #22
  async def b22(interage, q:str):
    link=spotify.pesquisar(q)
    await interage.send(link)

  @client.slash_command(name="serverinfo", description="Busque conhecimento!",
    description_localizations=dict.fromkeys(['en-US','en-GB'],"Get a server's information!")) #23
  async def b23(interage, convite:str=Opção(required=True,name_localizations=dict.fromkeys(['en-US','en-GB'],"invite"))):
    await serverinfo(interage.send,convite,client)


  @client.message_command(name="Tranduzir para o português.") #18a (mensagem)
  async def m18a(interage:nxc.Interaction, contexto:nxc.message):
    await interage.response.defer(ephemeral=True)
    await tradução(interage,quantidade=1,especifico=contexto,destino="pt")

  @client.message_command(name="Translate to English.") #18b (mensagem)
  async def m18b(interage:nxc.Interaction, contexto:nxc.message):
    await interage.response.defer(ephemeral=True)
    await tradução(interage,quantidade=1,especifico=contexto,destino="en")
