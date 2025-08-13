import pickle, random
from segundario import inicio, itens
from datetime import timedelta as td, datetime as dt
from db import lerDB as Score
from nextcord import utils as nxc, Embed
delay={}
dicionário={}

def caixa(itens,bruh=0,há=1):
  saida=Embed(title=["Seus itens (","Your items ("][bruh]+str(len(itens) if há else "0")+"/25):")
  nome= -3 if bruh==1 else 0
  i=0
  for item in itens:
    i+=1
    saida.add_field(name="Item "+str(i), value=item[nome], inline=True)
  return saida

def ganhar(id_,en):
  #if dt.now()<minimo:
  #  return ["Bot reiniciou recentemente!","Bot has recently rebooted!"][en]
  if (id_ not in delay) or dt.today().date()>delay[id_].date():
    item=random.choice(itens)
    with open("itens.pkl", "rb") as f:
      dicionário=pickle.load(f)
      if id_ not in dicionário: dicionário[id_]=[]
      if len(dicionário[id_])<25: dicionário[id_].append(item)
      else: return ["Inventário cheio!","Inventory full!"][en]
    with open("itens.pkl","wb") as f:
      pickle.dump(dicionário,f)
    delay[id_]=dt.today()
    return (
      [f"**Você ganhou __{item[0]}__! 🎉**\nUse `/comer` ou `/vender` para usá-los.\nVolte novamente ",
      f"**You got __{item[-3]}__! 🎉**\nUse `/eat` or `/sell` to use them. Come back "][en]+
      nxc.format_dt(delay[id_]+td(days=1),style="R")+"."
    )
  else: return(
    ["Para ganhar um item, volte ","To get an item, come back "][en]+
    nxc.format_dt(delay[id_]+td(days=1),style="R")+"."
  )

def inventário(id_,en):
  with open("itens.pkl", "rb") as f:
    dicionário=pickle.load(f)
    cont=dicionário.get(id_)
    if cont is not None:
      return caixa(dicionário[id_],en)
    else: return caixa([[["Você não tem itens.","You have no items."][en],0,"???"]],en,vazio=0)
  
def comer(id_,i,en):
  item=[]
  with open("itens.pkl", "rb") as f:
    dicionário=pickle.load(f)
    if id_ not in dicionário or i >= len(dicionário[id_]) or i <= 0:
      return ["Item especificado não existe.","Specified item out of bounds."][en]
    item=dicionário[id_].pop(i)
  with open("itens.pkl","wb") as f:
    pickle.dump(dicionário,f)
  variavel= [f"Você comeu {item[0]}",f"You ate {item[-3]}"][en]+"! :yum::yum:"
  if item[2]!="": variavel+=(" "+((item[-1]) if en else (item[2])))
  return variavel

def vender(id_,i,en):
  item=[]
  with open("itens.pkl", "rb") as f:
    dicionário=pickle.load(f)
    if id_ not in dicionário or i >= len(dicionário[id_])  or i < 0:
      return ["Item especificado não existe.","Specified item out of bounds."][en]
    item=dicionário[id_].pop(i)
  with open("itens.pkl","wb") as f:
    pickle.dump(dicionário,f)
  Score(id_,item[1],jogo=1)
  return [f"Você vendeu {item[0]} e ganhou",f"You sold {item[-3]} and got"][en]+f" {item[1]} score!"


async def inv(enviar,id_,indice=None,ação=None,en=0):
  mensagem=":x:"
  if ação==None or ação==0:
    mensagem=ganhar(id_,en)
  elif ação==1 and (type(indice) is int):
    mensagem=comer(id_,indice-1,en)
  elif ação==2 and (type(indice) is int):
    mensagem=vender(id_,indice-1,en)
  embed=inventário(id_,en)
  return await enviar(embed=embed,content=mensagem)
