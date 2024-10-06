import spotipy,os
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()
cid = os.getenv('SPOTIFY1')
secret = os.getenv('SPOTIFY2')
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
def pesquisar(titulo, artista=""):
  artista = artista.lower()
  if "various artists" in artista:
    artista==""
  else:
    artista="artist:"+artista.removesuffix(' - topic').removesuffix(' - tópico').replace(" ","")
  resultado= sp.search(limit=1,type='track',q=(titulo+" "+artista).strip())['tracks']['items']
  if len(resultado)==0:
    resultado= sp.search(limit=1,type='track',q=(titulo))['tracks']['items']
    if len(resultado)==0: return "Nenhum resultado."
  link= resultado[0]['external_urls']['spotify']
  return link
