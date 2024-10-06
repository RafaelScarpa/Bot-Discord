from nextcord import Embed

títulos=["Mensagem apagada em ","Mensagem editada em "]
cores=[0xff0000,0xffff00]
class canal:
  pass #Caso inicialização falhe.
inicializado=False

async def inicializarLog(client):
  try:
    global canal
    canal=await client.fetch_channel(1152337743788134471)
  except:
    print("Log desativado!")
  else:
    global inicializado
    inicializado=True


async def registrar(msg,tipo:int):
  global inicializado
  if not inicializado:
    return
  global canal
  anexos=[]
  
  for anexo in msg.attachments:
    try:
      anexos.append(await anexo.to_file())
    except:
      print("Erro de log: Anexo não era arquivo.")
  if anexos==[]:anexos=None
  await canal.send(
    embed=Embed(
      color=cores[tipo],
      title=títulos[tipo]+((msg.channel if tipo==0 else msg).jump_url),
      description=msg.content
    ).set_author(name=msg.author.name),
    files=anexos
  )
