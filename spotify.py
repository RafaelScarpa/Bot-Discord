import spotipy,os
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()
cid = os.getenv('SPOTIFY1')
secret = os.getenv('SPOTIFY2')
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
def pesquisar(titulo, artista=""):
  artista=artista.lower().removesuffix(' - topic').removesuffix(' - tópico')
  link= sp.search(limit=1,type='track',q=(titulo+' '+artista).strip())['tracks']['items'][0]['external_urls']['spotify']
  return link
