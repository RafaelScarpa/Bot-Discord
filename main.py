import discord
import os
import keep_alive

client = discord.Client()
keep_alive.keep_alive()


#Só pra avisar que tudo deu certo.
@client.event
async def on_ready():
	print('-----')
	print('Login como {0.user}!'.format(client))
	print('Versão do discord.py: ' + discord.__version__)
	print('-----')


#Parte legal.
@client.event
async def on_message(message):

	#Só umas variáveis pra deixar bonito.
	mensagem = message.content.lower()
	autor = message.author
	canal = message.channel
	async def enviar(Entrada):
		await message.channel.send(Entrada)

	#Impedir loops infinitos.
	if message.author == client.user:
		return

	#Comando para ignorar comandos.
	if "[ign]" in mensagem:
		return

	#Comando da lista de comandos.
	if (('comando' in mensagem) and ('bot' in mensagem)) or mensagem == '+comandos':
		EMBED1 = discord.Embed(title='Comandos:',description=(
		  '**"Comandos do Bot?"** (Esta lista.)' +
		  '\n**"Hora da Live?"** (Programação padrão do canal.)' +
		  '\n**"+YouTube"** (Link para o canal do YouTube.)' +
		  '\n**"+Live"** (Link para a live, se estiver acontecendo.)' +
		  '\n**"+Avatar"** (Avatar de alguém.)' +
		  '\n**"+Sobre"** (Info do bot.)' +
		  '\n**"+Clear"** (Apaga 30 mensagens. Apenas mods.)' +
		  '\n**"+Silenciar"** (Não funciona ainda. Apenas mods.)'))
		await message.channel.send(embed=EMBED1)

	#Comando 1
	if (mensagem == '+youtube') or (mensagem == '+live') or ('[btlnk]' in mensagem):
		await enviar('https://youtube.co/RafaelScarpa/live')
	if mensagem == '+twitch':
		await enviar('https://twitch.tv/Rafael_Scarpa')
	if mensagem == '+twitter':
		await enviar('https://twitter.com/ScarpaYT')

	#Comando 2
	if ('live' in mensagem) and ('hora' in mensagem):
		await enviar('Normalmente, 15:00(BRT/GMT-3) na sexta.')

	#Comando 3
	if mensagem == '+clear':
		if autor.permissions_in(canal).manage_messages:
			await canal.purge(limit=31)
			await enviar('30 mensangens apagadas por {0.display_name}.'.format(autor))
		else:
			await enviar('Você não tem as permissões certas.')

	#Comando 4
	if mensagem == '+avatar':
		await enviar(autor.avatar_url)
	elif mensagem.startswith('+avatar'):
		try:
			await enviar(message.mentions[0].avatar_url)
		except:
			await enviar('Você não marcou ninguém. Tente enviar apenas "+avatar".')

	#Comando 5
	if mensagem == '+sobre':
		await enviar('Fui criado para servir o Scopistão e substituir Scarpa. Para sugerir um comando, vá ao canal de sugestões.'
		)

	#Comando 6
	if mensagem == '+silenciar':
		await enviar('Este comando aceita apenas um usuário mencionado de cada vez e só pode ser usado por um moderador. Para desfazer, tire o cargo "Silenciado" do usuário.'
		)
	elif mensagem.startswith('+silenciar'):
		if autor.permissions_in(canal).manage_messages:
			if (len(message.mentions) == 1):
				try:
					cargo = autor.guild.get_role(800783416752472095)
					await message.mentions[0].add_roles(cargo)
					await message.mentions[0].send('Você foi silenciado no Scopistão. Contate um moderador se acha que isso é um erro.')
					await enviar('Sucesso.')
				except:
					await enviar('Eu acho que deu certo.')
			else:
				await enviar('Algo deu errado. Para mais informações, digite "+silenciar".')
		else:
			await enviar('Você não tem as permissões certas.')


client.run(os.getenv('TOKEN'))