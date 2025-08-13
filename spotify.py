import spotipy,os
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()
cid = os.getenv('SPOTIFY1')
secret = os.getenv('SPOTIFY2')
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def pesquisar(titulo, artista="",tipo="track"):
  #Limpeza
  if artista==None: artista=""
  artista = artista.lower()
  if "various artists" in artista:
    artista==""
  else:
    artista="artist:"+artista.removesuffix(' - topic').removesuffix(' - tópico')
  #Pesquisa
  resultado= sp.search(limit=2,type=tipo,q=(titulo+" "+artista).strip())[tipo+'s']['items']
  if len(resultado)==0:
    resultado= sp.search(limit=2,type=tipo,q=(titulo))[tipo+'s']['items']
    if len(resultado)==0:
  #Resultados
      return "❌"
  link= resultado[0]['external_urls']['spotify']
  return link
