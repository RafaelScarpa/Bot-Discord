from nextcord import Embed
import asyncio

títulos=["Mensagem apagada em ","Mensagem editada em "]
cores=[0xff0000,0xffff00]
class canal: #Caso inicialização falhe.
    async def send(embed=0,content=0,attachments=0):pass

async def inicializarLog(client):
  try:
    global canal
    canal=await client.fetch_channel(1152337743788134471)
  except:
    print("Log desativado!")

async def registrar(msg,i:int):
  anexos=[]
  for anexo in msg.attachments:
    try:
      anexos.append(await anexo.to_file())
    except:
      pass
  if anexos==[]:anexos=None
  await globals()["canal"].send(
    embed=Embed(
      color=cores[i],
      title=títulos[i]+((msg.channel if i==0 else msg).jump_url),
      description=msg.content
    ).set_author(name=msg.author.name),
    files=anexos
  )
