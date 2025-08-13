print("Bem vindo ao command line Pickle Inventory Viewing Tool (PIVeTe)\n")

import pickle
pontuações={}
inventários={}

def abrir():
  with open("scores.pkl", "rb") as f:
    global pontuações
    pontuações=pickle.load(f)
  with open("itens.pkl", "rb") as f:
    global inventários
    inventários=pickle.load(f)

def ver(qual,quem):
  abrir()
  if qual==1:
    if quem in pontuações:
      print(pontuações[quem])
    else:
      for usuário, pontuação in pontuações.items():
        print(f"{usuário}: {pontuação}")
  if qual==2:
    if int(quem) in inventários:
      print(quem+":")
      for item in inventários[int(quem)]:
        print(f'  {item[0]}: {item[1]}, "{item[2]}"')
    else:
      for usuário, itens in inventários.items():
        print(f"{usuário}:")
        for item in itens:
          print(f"    {item[0]}")
  print("")

def interação():
  entrada=input("PIVeTe> ")
  entrada=entrada.split(" ")
  quem=""
  if entrada[0]=="sair": exit()
  try:
    if entrada[0]=="ver":
      if entrada[1]=="pontos": qual=1
      elif entrada[1]=="itens": qual=2
      if len(entrada)==3: quem=entrada[2]
      ver(qual,quem)
    else: print("Não entendi.")
  except:
    print("Não entendi.")
  interação()

interação()
