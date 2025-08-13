import functools
import nextcord as nxc
from nextcord.ext import activities as ativ
from datetime import datetime
inicio=datetime.now()

#+comandos
def listaComandos(tipo,en):
  listas=[
  [
  '**"Comandos do Bot?":** *Isto.*\n'+
  '**"+YouTube":** *Meu canal!*\n'+ 
  '**"+Sobre":** *Info do bot!*\n'+
  '**"+Score:" e "+Rank"** *Ganhe pontos por falar!*\n'+
  '**"+Pergunta"** *Calcule seu futuro!*\n'+
  '**"+Doação":** *Me dê dinheiro que não mereço!*\n'+
  '**"+Avatar":** *Pegue a foto de alguém!*\n'+
  '**"+Abraço":** *Abraçoe alguém!*\n'+
  '**"+Tapa":** *Bem feito!*\n'+
  '**"+Nome":** *Um novo nome saindo do forno!*\n'+
  '**"+Limpar":** *Apaga 30 mensagens. (Para mods.)*\n'+
  '**"+Pokémon":** *Um pokémon aleatório!*\n'+
  '**"+Ship":** *O poder do amor?!*\n'+
  '**"+Dado":** *Role e boa sorte!*\n'+
  '**"+Palavra":** *Vocabulárise-se!*\n'+
  '**"+Estatistica":** *Nerd.*\n'+
  '**"+Item" ("+Comer" e "+Vender"):** *Loot box!*\n'+
#  '**"+Wiki":** *Informações imediatamente!*\n'+
  '**"+Spotify":** *Qual sua música favorita?*\n'+
  '**"+Serverinfo":** *Me de um link, te dou info.*\n'+
  '**"+Queanime":** *Ele vai descobrir...*'
  ,
  '**"+Help":** *This.*\n'+
  '**"+YouTube":** *My channel!*\n'+ 
  '**"+Score:" and "+Rank"** *Get points for talking!*\n'+
  '**"+Doação":** *I do not deserve others\' money!*\n'+
  '**"+PFP":** *Get someone\'s picture!*\n'+
  '**"+Hug":** *Hug someone!*\n'+
  '**"+Slap":** *That\'s what you get!*\n'+
  '**"+Name":** *A new brand new name for you!*\n'+
  '**"+Clear":** *Removes 30 messages. (Mods only.)*\n'+
  '**"+Pokémon":** *A random pokémon!*\n'+
  '**"+Ship":** *The power of love?!*\n'+
  '**"+Dice":** *Roll and good luck!*\n'+
  '**"+Palavra":** *Learn Portuguese!*\n'+
  '**"+Stats":** *You nerd.*\n'+
  '**"+Item" ("+Eat" and "+Sell"):** *Loot boxes!*\n'+
#  '**"+Wiki":** *Immediate information!*\n'+
  '**"+Spotify":** *What\'s your favorite song?*\n'+
  '**"+Serverinfo":** *Give me a link, I give you info.*\n'+
  '**"+Queanime":** *He\'ll find out what anime this is...*'
  ],[
  '**"/comandos":** *Isto*\n'+
  '**"/rank" e "/score":** *Ganhe pontos por falar!*\n'+
  '**"/pergunta":** *Calcule seu futuro!*\n'+
  '**"/avatar":** *Pegue a foto de alguém!*\n'+
  '**"/abraço":** *Abraçoe alguém!*\n'+
  '**"/tapa":** *Bem feito!*\n'+
  '**"/nome":** *Um novo nome saindo do forno!*\n'+
  '**"/pokémon":** *Um pokémon aleatório!*\n'+
  '**"/ship":** *O poder do amor?!*\n'+
  '**"/dado":** *Role e boa sorte!* \n'+
#  '**"/duelo":** *Batalhe! Ganhe?*'+
  '**"/pagar":** *Pix.*\n'+
  '**"/palavra":** *Vocabulárise-se!*\n'+
  '**"/estatistica":** *Nerd.*\n'+
  '**"/tradução":** *Traduza!*\n'+
  '**"/item" ("/comer" e "/vender"):** *Loot box!*\n'+
#  '**"/wiki":** *Informações imediatamente!*\n'+
  '**"/spotify":** *Qual sua música favorita?*\n'+
  '**"/serverinfo":** *Me de um link, te dou info.*'
  ,
  '**"/commands":** *This.*\n'+
  '**"/score:" and "/rank"** *Get points for talking!*\n'+
  '**"/avatar":** *Pegue a foto de alguém!*\n'+
  '**"/hug":** *Hug someone!*\n'+
  '**"/slap":** *That\'s what you get!*\n'+
  '**"/name":** *A new brand new name for you!*\n'+
  '**"/pokemon":** *A random pokémon!*\n'+
  '**"/ship":** *The power of love?!*\n'+
  '**"/dice":** *Roll and good luck!*\n'+
#  '**"/duel":** *Fight! Win?*'+
  '**"/pay":** *Wire transfer score.*\n'+
  '**"/palavra":** *Learn Portuguese!*\n'+
  '**"/stats":** *You nerd.*\n'+
  '**"/translate":** *Translate!*\n'+
  '**"/item" ("/comer" e "/vender"):** *Loot box!*\n'+
#  '**"/wiki":** *Immediate information!*\n'+
  '**"/spotify":** *What\'s your favorite song?*\n'+
  '**"/serverinfo":** *Give me a link, I give you info.*\n'
  ]
  ]
  return nxc.Embed(color=0x00ff90,title='Comandos:',description=listas[tipo][en])

#+nome
consoante=[
'','','b','b','b','c','c','c','d','d','d','f','f','f','g','g','g','j','j','j','l','l''l','m','m','m','n','n','n','p','p','p','r','r','r','s','s','t','t','t','v','v','v','z','z','z',
'br','cr','fr','gr','pr','tr','vr','bl','cl','fl','gl','pl','tl','gu','qu','ch','ss',
'h','ç','x','ch','k','w','wh','sh','kr']
vogal=['a','a','a','a','e','e','e','e','i','i','i','i','o','o','o','o',
'ai','ei','ão','ã','y',
'u','u','u','u']
fim=['','','','','','','r','l','s','n',
'v','k','c','ng','t','w']

#Comandos genéricos de links.
links=[
  nxc.Embed(title="Rafael Scarpa no YouTube",url="https://youtube.co/RafaelScarpa/live",color=0x00ff90),
  nxc.Embed(title="Em pausa. Tente 1.1.1.1?",url="https://1.1.1.1",color=0x00ff90),
  nxc.Embed(title="Doações?! :eyes:",url="https://streamelements.com/rafaelscarpa/tip",color=0x00ff90)]

#+pergunta
prgt=['O Algoritmo™ diz:\n"{}"','The Algorithm™ says:\n"{}"']
rsp=["Nah.","Achando que não, ein.","Não sei...","Tem uma boa chance.",":+1: Sim.","Pergunte de novo.","As aparências enganam.","Este futuro não é definido."]

#+abraço/tapa
frases=[[
  ['Abraço dado para __{0}__.','Hug given to ___{0}__]'],
  ['/give __{0}__ hug 64','/give __{0}__ hug 64'],
  ['Abração enviado pra __{0}__.','Big hug sent to __{0}__.'],
  ['__{1}__ usou abraço.\nFoi super efetivo!','__{1}__ used hug.\nIt was super effective!'],
  ['`await abraço(__{1}__, __{0}__)`','`await hug(__{1}__, __{0}__)`'],
],[
  ['__{1}__ esbofeteou __{0}__.','__{1}__ hit __{0}__.'],
  ['__{1}__ tapeou __{0}__.','__{1}__ slapped __{0}__.'],
  ['__{1}__ bateu em __{0}__.','__{1}__ beat up __{0}__.'],
  ['__{1}__ usou Tapa.\nUm ataque crítico!','__{1}__ used slap.\nA critical hit!'],
  ['__{0}__ levou uma pra ficar esperto(a).','__{0}__ got a wake up call.'],
  ['__{1}__ atacou __{0}__.','__{1}__ attacked __{0}__.'],
  ['__{0}__ tentou colar na prova de __{1}__.','__{1}__ feels __{0}__ cheated on them.'],
  ['__{0}__ levou só uma de __{1}__.','__{0}__ just took one from __{1}__.'],
  ['__{0}__ mereceu uma bicuda.','__{0}__ deserved it.'],
  ['__{0}__ está sendo vítma de assédio.','__{0}__ becomes a victim of harassment.'],
  ['__{1}__ agrediu __{0}__.','__{1}__ hurt __{0}__.'],
  ['__{0}__ e __{1}__ entram em conflito.','__{0}__ and __{1}__ are in conflict.'],
  ['__{1}__ assou __{0}__ na porrada.','__{1}__ absolutely destroyed {0}.'],
  ['__{1}__ espancou __{0}__.','__{1}__ kicked {0} with bare hands.']
]]
gifs=[[
  'https://media4.giphy.com/media/l4FGy5UyZ1KnVZ7BC/giphy.gif',
  'https://media4.giphy.com/media/l8ooOxhcItowwLPuZn/giphy.gif',
  'https://media4.giphy.com/media/U4LhzzpfTP7NZ4UlmH/giphy.gif',
  'https://media4.giphy.com/media/VbawWIGNtKYwOFXF7U/giphy.gif',
  'https://media4.giphy.com/media/k9Jw0MW9TV6Dbewyx2/giphy.gif',
  'https://media4.giphy.com/media/3oEjI72YdcYarva98I/giphy.gif',
  'https://media4.giphy.com/media/RJEIl2fBX3jAJOqSau/giphy.gif',
  'https://media4.giphy.com/media/Lb3vIJjaSIQWA/giphy.gif',
  'https://media4.giphy.com/media/IzXiddo2twMmdmU8Lv/giphy.gif',
  'https://media4.giphy.com/media/M8o1MOwcwsWOmueqN4/giphy.gif'
],[
  'https://c.tenor.com/feYx-Pe4s4AAAAAM/tapa-2345.gif',
  'https://c.tenor.com/G615xUCziBoAAAAC/globo-tapa.gif',
  'https://media.tenor.com/ED4tqjm3jcAAAAAC/will-smith-oscars.gif',
  'https://media4.giphy.com/media/uG3lKkAuh53wc/giphy.gif',
  'https://media4.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif',
  'https://media4.giphy.com/media/13dRJkj5wgKq9q/giphy.gif',
  'https://media4.giphy.com/media/lX03hULhgCYQ8/giphy.gif',
  'https://media4.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif',
  'https://media4.giphy.com/media/LD8TdEcyuJxu0/giphy.gif',
  'https://media4.giphy.com/media/3ohfFOrOAW9GaczHc4/giphy.gif',
  'https://media4.giphy.com/media/Qvwc79OfQOa4g/giphy.gif',
  'https://media4.giphy.com/media/UbzayP2FNPWbm/giphy.gif',
  'https://i.imgflip.com/4qxugy.gif'
]]
def gif(i,n=False,u='Você',f=0): 
  a= nxc.Embed(title=f.format(n,u)) if n else nxc.Embed()
  a= a.set_image(url=i)
  return a

#+sobre
sobre= 'Diretriz secundária: Servir todas as necessidades do servidor.\nDiretriz primária: Remover qualquer necessidade de bots com nomes que começam com "L".'
hora = 'Normalmente a live começa às 15:00(BRT/GMT-3) na sexta ou no sabado.'

#+pokemon
@functools.cache
def pokemon(en,numero,nome,tipo):
  embed = nxc.Embed(title=nome,description=["Tipo: ","Type: "][en]+tipo)
  embed.set_author(name="#"+str(numero))
  embed.set_image(url=f"https://img.pokemondb.net/artwork/{nome.lower()}.jpg")
  return embed

#+rank
def ranking(scores,en):
  rank=''
  for i in range(0,10):
    rank+=('__{a}__ **<@!{b}>:** {c}\n').format(a=i+1,b=scores[i][0],c=scores[i][1])
  return nxc.Embed(color=0x00ff90,title=['Ranking de Score:','Score ranking:'][en],description=rank)

#evento
def eu(u): return u.id==439609946175438858

cargo = [
  975549281945657396,
  979846270741016626
]

#pagar
pagar=["**Transferência concluída!**\n{0}»{1}\n{2}»{3}","**Transfer complete!**\n{0}»{1}\n{2}»{3}"]

#estatistica
def stat(n,v1,v2,v3,v4,v5):
  embed=nxc.Embed(title="Atributos:")
  embed.set_author(name=n)
  embed.add_field(name="Força", value=v1+"/21", inline=True)
  embed.add_field(name="Destreza", value=v2+"/21", inline=True)
  embed.add_field(name="Inteligência", value=v3+"/21", inline=True)
  embed.add_field(name="Sabedoria", value=v4+"/21", inline=True)
  embed.add_field(name="Carisma", value=v5+"/21", inline=True)
  return embed

#palavra
palavras=''
with open("palavras.txt", encoding="utf8") as p:
  palavras=p.readlines()
lenPalavras=len(palavras)

#nice
nice=["Contador de nice: {}","Nice counter: {}"]

#natal
natal=["Contador de natal: {}","Christmas counter: {}"]

#inglês
@functools.cache
def eng(m): return m.guild.get_role(832738572486049824) in m.roles

#noite
noite=[
  ["Sleep","Night","Evening","Rest","Eep"],
  ["well","nice","good","great","stellar","fantasic"]
]

#inventário
itens=[
  ["Carrinho de mão",7,"Rico em ferro!","Wheelbarrow","","Rich in iron!"],
  ["Patinho de borracha",2,"Parece chiclete sem gosto.","Rubber duck","","It's like flavorless gum."],
  ["Sorvete",5,"Sabor misto, docinho.","Ice cream", "", "Sweet swirl."],
  ["Sorvete",4,"Sabor baunilia, docinho.","Ice cream","","A nice vanilla."],
  ["Chá gelado",4,"Energético!","Ice tea","","Energizing!"],
  ["Ferrocianeto férrico",1,"hmmmmmmmm fumaça", "Ferric ferrocyanide", "", "blue and smoky"],
  ["Disco de Fortnite (Xbox One), lacrado",8,"Gosto épico de Victory Royale.", "Fortnite (Xbox One) Disc, sealed","","Epic taste of victory royale."],
  ["PC da Xuxa",9,"???","Potato PC","","Tastes like chips."],
  ['DVD "Barquinhos" Lacrado',11,"","Vídeo Brinquedo DVD movie, sealed","",""],
  ["Chinelo",3,"Parece chiclete sem gosto.","Flip flops","","It's like flavorless gum."],
  ["Caixa",1,"Acho que tinha algo dentro...","Box","","I think it wasn't empty..."],
  ["Sanduíche",5,"","Sandwich","",""],
  ["Nokia",8,"Gosto de dentes. ...Deve ser só seus dentes.","Nokia phone","","Tastes like teeth. ...Your teeth broke."],
  ["Bolo",6,"Doce!","Cake","","Sweet."], ["Bolo",7,"Doce!","Cake","","Very sweet!"],
  ["Muito queijo",8,"Nunca é muito queijo.","Too much cheese","","It's never too much cheese."],
  ["Queijo",7,"","Cheese","",""],
  ["MasterCard",0,"Não tem preço.","MasterCard","","Priceless"],
  ["Sanduiche de frango",3,"","Chicken sandwich","",""],
  ["Sanduiche de frango deluxe picante",5,"","Deluxe spicy chicken sandwich","",""],
  ["Batata Frita",2,"Salgado.","Fries","","Salty."],
  ["Tijolo",1,"Um gosto concreto.","Brick","","Concrete taste."],
  ["Boneco de ação 'My World'",4,"Plástico.","Knock-off action figure","","Plastic."],
  ["Cadeira de plástico",4,"Foi bem grande.","Plastic chair","","That was big."],
  ["Ovo",5,"Crocante.","Egg","","Crunchy."],
  ["Prato platônico",3,"Porém pra simplificar a apresentação no plural é sempre completamente aplicável e prático, pular uma pura placa pluvial de plástico.","Platonic plate","",'"Plate-o" lol /p'],
  ["Banana",2,r"\*som hilário de escorregar em algo\*","Banana","","potassium"]
]
