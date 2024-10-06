import os, sys, asyncio
import nextcord as nxc
import segundario as seg #Constantes.
from datetime import datetime as dt, timedelta as td
import random
from time import time
from math import ceil
import re
from db import lerDB
import translators as ts
import wikipedia
import pypokedex as poke
from LeeSpork1 import ship as Ship
import spotify
from inventário import inv as Inventário

random.seed(time())
delay={}
#ts.preaccelerate_and_speedtest(timeout=21.0)
print(dt.now().strftime("%d/%m/%Y %H:%M:%S"))



async def níveis(u,enviar,msg):
  p = lerDB(u.id) #Obter pontuação
  #Se tiver pontuação mínima e não tiver nível máximo
  if p>=200 and (ouro:=msg.guild.get_role(seg.cargo[1])) not in (cargos:=u.roles):
    #Se tiver pontuação máxima.
    if p >= 2500:
      print("aaaaaaaaaaaaaaa "+str(u.id))
      try: await u.remove_roles(msg.guild.get_role(seg.cargo[0])) #"prata"
      except: pass
      await u.add_roles(ouro)
      await enviar(["Você está no nível Ouro!","You're at Gold level!"][seg.eng(u)])
    #Se não tiver cargo mínimo.
    elif (prata:=msg.guild.get_role(seg.cargo[0])) not in cargos:
      await u.add_roles(prata)
      await enviar(["Você está no nível Prata!","You're at Silver level!"][seg.eng(u)])

def fixarRand(s:int,limite:int,rep=1):
  gera=[]
  for seed in s:
    random.seed(seed)
    for i in range(0,rep):
      gera.append(random.randint(0, limite))
  random.seed(time())
  if len(gera)==1: gera=[0]
  return gera



#14
class botõesJokenpô(nxc.ui.View):
    def __init__(si,desafiador,desafiado):
      super().__init__()
      si.escolha1=False
      si.escolha2=False
      si.cancelado=False
      si.desafiador=desafiador
      si.desafiado=desafiado
      #si.interage=None

    def terminar(si):
      if si.escolha1 and si.escolha2:
        #si.interage=interage
        si.stop()

    @nxc.ui.button(label="🪨", style=nxc.ButtonStyle.green)
    async def pedra(si, botão: nxc.ui.Button, interage: nxc.Interaction):
      match interage.user.id:
        case si.desafiador.id:
          si.escolha1 = "🪨"
        case si.desafiado.id:
          si.escolha2 = "🪨"
        case _: pass
      return si.terminar()
    @nxc.ui.button(label="📄", style=nxc.ButtonStyle.green)
    async def papel(si, botão: nxc.ui.Button, interage: nxc.Interaction):
      match interage.user.id:
        case si.desafiador.id:
          si.escolha1 = "📄"
        case si.desafiado.id:
          si.escolha2 = "📄"
        case _: pass
      return si.terminar()
    @nxc.ui.button(label="✂", style=nxc.ButtonStyle.green)
    async def tesoura(si, botão: nxc.ui.Button, interage: nxc.Interaction):
      match interage.user.id:
        case si.desafiador.id:
          si.escolha1 = "✂"
        case si.desafiado.id:
          si.escolha2 = "✂"
        case _: pass
      return si.terminar()

    @nxc.ui.button(label="✖", style=nxc.ButtonStyle.red)
    async def cancelar(si, botão: nxc.ui.Button, interage: nxc.Interaction):
      if interage.user.id in [si.desafiador.id,si.desafiado.id]:
        si.cancelado=True
        si.interage=interage
        si.stop()



#2
async def limpar(autor,msg,enviar,limite:int=31):
  canal=msg.channel
  if canal.permissions_for(autor).manage_messages:
    await canal.purge(limit=limite)
    await enviar(str(limite)+' mensangens apagadas por {}.'.format(autor.display_name),delete_after=23)
  else:await enviar(['Você não tem as permissões certas.','Wrong permissions.'][seg.eng(autor)])

#3
async def avatar(m,mensagem:str,autor,enviar):
  if not(m) or len(mensagem)==7:
    await enviar(autor.display_avatar.url)
  else:await enviar(m[0].display_avatar.url)

#4
async def nice(mensagem:str,enviar,autor):
  with open("nice.txt","r") as txt:
    contador=int(txt.readlines()[0])
  #Adicionar número de vezes.
  contador+=mensagem.count("nice")
  #Mensagem
  await enviar(seg.nice[seg.eng(autor)].format(str(contador)), delete_after=10)
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
    await enviar(embed=
      seg.gif(random.choice(seg.gifs[i]), nick, autor.display_name, random.choice(seg.frases[i])[seg.eng(autor)])
    )

#7
async def pontos(msg,autor,menção,enviar):
  en=seg.eng(autor)
  if not(menção) or msg in ['+score','+pontos']:
    await enviar(['Você tem {} Score!','You have {} Score'][en].format(str(lerDB(autor.id))))
  else:
    if len(menção)==1 and not menção[0].bot:
      lerDB(menção[0].id)
      await enviar(['Score de {}: ',"{}'s Score: "][en].format(menção[0].mention,str(lerDB(menção[0].id))))
    else: await enviar(["Mencione um humano ou ninguém para usar este comando.","Mention a human or no one to use this command."][en])

#8
async def reações(msg,client,emoji):
  if type(emoji)==int: reação= client.get_emoji(emoji)
  else: reação=emoji
  await msg.add_reaction(reação)

#9
async def pokemon(enviar,numero:int=""):
  if numero=="" or numero not in range(1,1008):
    numero = random.randint(1,1008)
  p = poke.get(dex=numero)
  await enviar(seg.pokemon.format(numero,p.name.title(),', '.join(p.types)))

#10
async def ship(menções,autor,enviar):
  en=seg.eng(autor)
  match len(menções):
    case 1: menções.append(autor)
    case 2: pass
    case _: return await enviar(['Escolha ao menos uma pessoa para usar este comando.','Choose at least one person to use this command.'][en])
  try:
    await enviar(Ship(
      menções[0].display_name,int(menções[0].id),
      menções[1].display_name,int(menções[1].id),
      en
    ))
  except Exception as e:
    await enviar("Erro"+["!","r!"][en])
    print("Erro em +ship!\nIDs:",menções[0].id,menções[1].id)
    raise e

#11
async def rank(enviar,msg,autor):
  async with msg.channel.typing():
    scores=lerDB(tudo=True)
    scores= sorted(scores.items(),reverse=True,key=lambda par:par[1])
    await enviar(embed=seg.ranking(scores,seg.eng(autor)))

#12
async def evento(servidor,n:str="Live!"):
  tempo=dt.now()
  tempo+=td(hours=3,minutes=6)
  canal=servidor.get_channel(779403680096452639)
  await servidor.create_scheduled_event(name=n, start_time=tempo, entity_type= seg.nxc.ScheduledEventEntityType.voice, channel=canal)

#13
async def dado(enviar,lados:int=6,quantidade:int=1,mensagem=None,autor=None):
  if autor is not None:
    en=seg.eng(autor)
  else:
    en=0
  soma=0
  if mensagem !=None:
    for i in ["+dado","+dice","+die"]: mensagem=mensagem.replace(i,"")
    try: lados=int(mensagem.strip())
    except ValueError: pass
  if lados<1:lados=6
  texto="🎲" if not lados==2 else "🪙"
  if quantidade > 3000:
    return await enviar(["Não. Muito.","No. Too many."][en])
  if quantidade > 1:
    if quantidade < 11:
      resposta=["Seus números são:\n","Your numbers are:\n"][en]
      for i in range(quantidade):
        valor=random.randint(1,lados)
        soma+=valor
        resposta+="- "+str(valor)+"\n"
      resposta+=["Soma: ","Sum: "][en]+str(soma)
    else:
      for i in range(quantidade):
        soma+=random.randint(1,lados)
      resposta=["A soma dos seus números é ","The sum of your numbers is "][en]+str(soma)+"."
  else:
    resposta=["Seu número é ","Your number is "][en]+str(random.randint(1,lados))+". ("+texto+str(lados)+")"
  await enviar(resposta)

#14
async def duelo(enviar,desafiador,desafiado,escolha1,escolha2,en=0,valor=0):
#  if desafiado.guild.get_role(1243957980206989425) in desafiado.roles: #Se precisar proibir alguem.
#    return await enviar(["Não!","No!"][en])
  resultado=(["{2} escolheu {0}. {3} escolheu","{2} chose {0}. {3} chose"][en] +" {1}.\n").format(escolha1,escolha2,desafiador.mention,desafiado.mention)
  if escolha1==escolha2:
    resultado+=["É um empate!","It's a tie!"][en]
    substituição=False
  if (escolha1=="🪨" and escolha2=="📄") or (escolha1=="📄" and escolha2=="✂") or (escolha1=="✂" and escolha2=="🪨"): #VERIFIQUE SE ABAXIO DESSA LINHA FAZ SENTIDO
    substituição=(desafiador,desafiado,valor)
  elif (escolha2=="🪨" and escolha1=="📄") or (escolha2=="📄" and escolha1=="✂") or (escolha2=="✂" and escolha1=="🪨"):
    substituição=(desafiado,desafiador,valor)
  if substituição!=False:
    resultado+=(["{0.mention} ganhou! {1.mention} perdeu {2} Score.","{0.mention} won! {1.mention} loses {2} Score."][en]).format(*substituição)
    lerDB(substituição[0].id,valor,True)
    lerDB(substituição[1].id,0-valor,True)
  await enviar(resultado)

#15
async def pagar(enviar,autor,destino,valor:int):
  en=seg.eng(autor)
  if destino.bot or destino.id==autor.id:
    return await enviar(["Isso não é aceito.","This is not accepted."][en])
  saldo1=[lerDB(autor.id),lerDB(destino.id)]
  if valor>0 and saldo1[0]>=valor:
    saldo2=[lerDB(autor.id,-valor,True),lerDB(destino.id,valor,True)]
    await enviar(seg.pagar[en].format(saldo1[0],saldo2[0],saldo1[1],saldo2[1]))
  else: await enviar(["Não? 🤨","No? 🤨"][en])

#16
async def stat(enviar,membro=None):
  if membro==None:
    texto= await nome(sub=True)
    valores=[random.randint(0,14),random.randint(0,14),random.randint(0,14),random.randint(0,14),random.randint(0,14)]
  else:
    texto=membro.display_name
    valores= fixarRand([membro.id],14,5)
  await enviar(embed=seg.stat(texto,str(valores[0]+7),str(valores[1]+7),str(valores[2]+7),str(valores[3]+7),str(valores[4]+7)))

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
  for i in range(len(conteúdos)):
    texto+="\n**`"+autores[i]+"`**: "+ts.translate_text(query_text=conteúdos[i]if conteúdos[i]!=""else"[]",to_language=destino)
  await msg.send(texto[1:],ephemeral=True)

#19
async def youtubemusic(msg,enviar):
  await asyncio.sleep(0.5)
  try:
    embed=msg.embeds[0]
  except: print("Erro de youtubemusic(): Sem embed.")
  try:
    link=spotify.pesquisar(embed.title,embed.author.name)
    await enviar(link)
  except Exception as e:
    print("Erro de youtubemusic(): Outro. Abaixo.")
    raise e

#20
async def itens(enviar,autor,indice:int=None,ação=None,mensagem=None):
  if mensagem!=None:
    mensagem=mensagem.split(" ",1)
    if len(mensagem)>1:
      try: indice=int(mensagem[1].strip())
      except ValueError: pass
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
  try:
    convite=await client.fetch_invite(link)
  except: return await enviar("Ocorreu um erro. Tenha certeza de que enviou um URL válido de convite.")
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

#24 (incompleto)
async def nitro(msg,enviar,client):
  emoji=...
  #se possivel e for uma resposta, pegar mensagem original
  mensagens=[msg]
  if msg.reference and type(msg.reference.resolved)==nxc.Message:
    mensagens+=[msg.reference.resolved]
  #encontrar emoji no texto ou nas reações
  for fonte in mensagens:
    if (emoji:=re.search(r"<a?:\w+:\d+>",fonte.content))!=None:
      id_emoji=int(re.search(r"\d+",emoji[0])[0])
      emoji=client.get_emoji(id_emoji)
      break
    elif fonte.reactions and (emojis:=filter((lambda x: x.is_custom_emoji()),fonte.reactions)):
      try:
        emoji = next(emojis).emoji
      except StopIteration:
        continue
      else:
        break
    else:
      continue
  else:
    return await enviar("❓")
  #formar a resposta
  resposta="\n".join([
    "url: "+emoji.url,
    "nome: "+emoji.name,
    "criado: "+emoji.created_at.strftime("%B %d, %Y"),
    "id: "+str(emoji.id)
  ])
  #adicionar à resposta se possivel
  try:
    resposta+="\n"+"\n".join([
      "por: "+emoji.guild.name,
#      "convite: "+...
    ])
  except:
    pass #sem acesso ao servidor
  return await enviar(resposta)
  pass

#25
async def twitter(mensagem:str, enviar):
  partes=mensagem.split(" ")
  for parte in partes:
    if parte.startswith(("https://x.com/","https://twitter.com/","http://x.com/","http://twitter.com/")):
      mensagem=parte
      break
    else:
      return
  mensagem2= mensagem.replace("://x.com/","://pxtwitter.com/",1).replace("://twitter.com/","://pxtwitter.com/",1)
  await enviar(mensagem2+"   [(cache)](<https://webcache.googleusercontent.com/search?q=cache:"+mensagem+">)")



async def processar(msg,mensagem,autor,menciona,enviar,client):

  lerDB(autor.id, 1) #Score
  await níveis(autor,enviar,msg)

  #Verificações
  if mensagem.startswith("+"): #1 (simples)
    match mensagem:
      case '+twitter': #1b
        await enviar(embed=seg.links[1])
      case '+doação'|'+donate': #1c
        await enviar(embed=seg.links[2])
      case '+links': #1d
        await enviar(embed=seg.links[3])
      case '+sobre'|'+about': #1e
        await enviar(embed=seg.sobre)
      case "+queanime": #1f
        await enviar("<@!594211566581186646> que anime é esse?")

      case '+limpar'|'+clear': await limpar(autor,msg,enviar) #2
      case '+nome'|'+name': await nome(autor,enviar) #5
      case '+pokemon'|'+pokémon': await pokemon(enviar) #9
      case '+rank'|'+ranking': await rank(enviar,msg,autor) #11
      case "+evento"|"+event": #12
        if seg.eu(autor): await evento(msg.guild)
      case "+estatistica"|"+estatística"|"+stats": await stat(enviar,None) #16
      case "+palavra"|"+word": await palavras(enviar) #17
      case "+tradução": await tradução(msg,destino="pt") #18a
      case "+translate": await tradução(msg,destino="en") #18b
      case "+item": await itens(enviar,autor,ação=0) #20a

    if mensagem.startswith('+pergunta'): #1g
      await enviar(seg.prgt[seg.eng(autor)].format(random.choice(seg.rsp)))

    if mensagem.startswith(('+avatar','+pfp')): await avatar(menciona,mensagem,autor,enviar) #3
    if mensagem.startswith(('+abraço','+hug')): await gif(0,menciona,enviar,autor) #6a
    if mensagem.startswith(('+tapa','+slap')): await gif(1,menciona,enviar,autor) #6b
    if mensagem.startswith(('+score','+pontos')): await pontos(mensagem,autor,menciona,enviar) #7
    if mensagem.startswith('+ship'): await ship(menciona,enviar) #10
    if mensagem.startswith(("+dado","+die","+dice")): await dado(enviar,quantidade=1,mensagem=mensagem,autor=autor) #13
    if mensagem.startswith(("+comer","+eat")): await itens(enviar,autor,ação=1,mensagem=mensagem) #20b
    if mensagem.startswith(("+vender","+sell")): await itens(enviar,autor,ação=2,mensagem=mensagem) #20c
    if mensagem.startswith("+wiki"): await wiki(enviar,mensagem) #21
    if mensagem.startswith("+spotify"): await música(enviar,mensagem) #22
    if mensagem.startswith("+nitro"): await nitro(msg,enviar,client) #24 (incompleto)

  if mensagem=="good night everyone": #1a
    await enviar((random.choice(seg.noite[0])+" "+random.choice(seg.noite[1])+"!"),mention_author=False)
  if ('comando'in mensagem and'bot'in mensagem) or mensagem in ['+comandos','+?','+help','+commands']: #1h
    await enviar(embed=seg.listaComandos(0,seg.eng(autor)))
  if mensagem in ['+youtube','+live'] or'[btlnk]'in mensagem: #1i
    await enviar(embed=seg.links[0])
  if mensagem in ['!help','!commands','!ajuda','!comandos']: #1j
    await enviar(["O prefixo certo é `+`.","The right prefix is `+`."][seg.eng(autor)])

  if'nice'in mensagem: await nice(mensagem,enviar,autor) #4
  if'loritta'in mensagem or'lorita'in mensagem: await reações(msg,client,776145108689092639) #8a
  if ' eep'in mensagem or mensagem.startswith('eep'): await reações(msg,client,str("\N{SLEEPING FACE}")) #8b
  if 'hmm' in mensagem: await reações(msg,client,str("\N{THINKING FACE}")) #8c
  if "music.youtube.com/" in mensagem: await youtubemusic(msg,enviar) #19
  if "https://x.com/" in mensagem or "https://twitter.com/" in mensagem: await twitter(mensagem,enviar) #25

  if mensagem=='+encerrar bot agora' and seg.eu(autor): #Comando debug
    os.system('start cmd /c cd "C:/Bot Discord" && python main.py')
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
    await interage.send(embed=seg.listaComandos(1,seg.eng(interage.user)))

  @client.slash_command(name="limpar", description="😬⏪") #2
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
    await gif(0,[m],interage.send,interage.user)

  @client.slash_command(name="tapa", description="Agressão?",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'slap'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Aggression?')
  ) #6b
  async def b06b(interage, m:nxc.Member):
    await gif(1,[m],interage.send,interage.user)

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
    description_localizations=dict.fromkeys(['en-US',"en-GB"],'Who yapped most?')
  ) #11
  async def b11(interage):
    await interage.response.defer()
    await rank(interage.send,interage,interage.user)

  @client.slash_command(name="evento", description="COMEÇA LOGO!") #12
  async def b12(interage,n:str=
    Opção(name="nome", required=False,default="Live!")
  ):
    if seg.eu(interage.user):
      await interage.send("ok",ephemeral=True)
      await evento(interage.guild,n)
    else: await interage.send("não",ephemeral=True)

  @client.slash_command(name="dado", description="Role e boa sorte!",
    name_localizations={'en-US':'dice',"en-GB":'die'},description_localizations=dict.fromkeys(['en-US',"en-GB"],'Roll and good luck!')
  ) #13
  async def b13(interage,
    d:int=Opção(
      name="lados",required=False,default=6,min_value=1,
      name_localizations=dict.fromkeys(['en-US',"en-GB"],'sides')
    ), q:int=Opção(
      name="quantidade",required=False,default=1,min_value=1,max_value=3000,
      name_localizations=dict.fromkeys(['en-US',"en-GB"],'quantity')
    )
  ):
    await dado(interage.send,d,q,autor=interage.user)

#  @client.slash_command(name="aposta", description="Jogue, vença, ganhe!",
#    name_localizations=dict.fromkeys(['en-US',"en-GB"],'bet'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Play, win, earn!')
#  ) #14
#  async def b14(interage,
#    v:int= Opção(name="valor", min_value=1, required=False, name_localizations=dict.fromkeys(['en-US',"en-GB"],'amount'), default=None),
#    e= Opção(name="escolha", choices=["🪨","📄","✂"], required=False, name_localizations=dict.fromkeys(['en-US',"en-GB"],'choice'),default=None),
#  ):
#    await interage.response.defer()
#    await aposta(interage.send, interage.user, v, e)

  @client.slash_command(name="duelo", description="Desafie alguem!",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'duel'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Challenge someone!')
  ) #14
  async def b14(interage,
    m:nxc.Member= Opção(name="desafiar",name_localizations=dict.fromkeys(['en-US',"en-GB"],'challange')),
    v:int= Opção(name="aposta", min_value=0, required=False, name_localizations=dict.fromkeys(['en-US',"en-GB"],'bet'), default=0)
  ):
    en1=seg.eng(interage.user)
    en2=seg.eng(m)
    if interage.user.id == m.id:
      return await interage.send(["Não é possível jogar só.","Cannot play alone."][en1])
    if lerDB(interage.user.id)<v:
      return await interage.send(["Você não tem saldo suficiente para apostar esse valor. ","You don't have enough Score to bet this high."][en1])
    elif lerDB(m.id)<v:
      return await interage.send(m.mention+[" não tem saldo suficiente para apostar esse valor."," doesn't have enough Score to bet this high."][en2])
    entrada = botõesJokenpô(interage.user,m)
    texto=["{0}, escolha um dos items.","{0}, pick one of the items."][en1]+"\n"
    if v>0:
      texto+=["Apostando {1} score.","Betting {1} Score."][en2]
    else:
      texto+=["Jogo amistoso.","Friendly game."][en2]
    texto+=[" Selecione um dos itens para aceitar, {2}."," Pick one of the items to accept, {2}."][en2]
    mensagem= await interage.send(texto.format(interage.user.mention,v,m.mention), view=entrada)
    await entrada.wait()
    if entrada.cancelado:
      return await mensagem.channel.send(["Jogo cancelado por jogador.","Game cancelled by player."][en1])
    if False in [entrada.escolha1,entrada.escolha2]:
      return await mensagem.channel.send(["Jogo cancelado por inatividade.","Game cancelled for inactivity."][en1])
    await duelo(mensagem.channel.send,interage.user,m,entrada.escolha1,entrada.escolha2,en1,v)

  @client.slash_command(name="pagar", description="Cryptomoedas.",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'pay'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Cryptocurrencies.')
  ) #15
  async def b15(interage, destino:nxc.Member, valor:int):
    await interage.response.defer()
    await pagar(interage.send,interage.user,destino,valor)

  @client.slash_command(name="estatistica", description="Veja seus atributos!",
    name_localizations=dict.fromkeys(['en-US',"en-GB"],'stats'),description_localizations=dict.fromkeys(['en-US',"en-GB"],'Find your attributes!')
   ) #16
  async def b16(interage,membro:nxc.Member=
    Opção(required=False,default=None)
  ):
    await stat(interage.send,membro)

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

#  @client.slash_command(name="wiki", description="Responda, rápido.",
#    description_localizations=dict.fromkeys(['en-US',"en-GB"],'Answers, quick.')) #21
#  async def b21(interage,
#    n:str=Opção(required=True,name="nome",
#      name_localizations=dict.fromkeys(['en-US',"en-GB"],'name')
#    ),
#    l=Opção(name="lingua",choices={"English":"en","Português":"pt"},required=True,
#      name_localizations=dict.fromkeys(['en-US',"en-GB"],'language')
#    )
#  ):
#    await interage.response.defer(ephemeral=False)
#    await wiki(interage.send,n,l)

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

  @client.message_command(name="Emoji (beta)")
  async def m24(interage:nxc.Interaction, contexto:nxc.message):
    await nitro(contexto,interage.send,client)
