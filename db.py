import pickle
from datetime import datetime as dt, timedelta as td
dicionário={}
delay={}

def lerDB(id_=0,soma=0,jogo=0,tudo=0):
  id_=str(id_)
  sai=None
  if not (jogo or (id_ not in delay) or delay[id_]<dt.now()):
    soma=0
  with open("scores.pkl", "rb") as f:
    dicionário = pickle.load(f)
    if tudo:
      return dicionário
    if id_ in dicionário:
      dicionário[id_]+=soma
      sai=dicionário[id_]
    else:
      dicionário[id_]=0+soma
      sai=dicionário[id_]
  if soma!=0:
    delay[id_]=dt.now()+td(seconds=20)
    with open("scores.pkl","wb") as f:
      pickle.dump(dicionário,f)
  return sai
