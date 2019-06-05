# importa l'API de Telegram
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

#clases creades que faran tot el que ens interesa.
from prova import WorkGraphMaps
import download
# al fer el import no hem ficat cap funció perque les dades només s'han de descomprimir, al principi de tot,
# amb lo que si fem import directament s'executa sense haver-ho de crear :P


def errors(numErr,bot,update):
	if numErr == 1:
		bot.send_message(chat_id=update.message.chat_id,text="No has inicialitzat la conversa, executa /start per començar")
	elif numErr == 2:
		bot.send_message(chat_id=update.message.chat_id,text ="No has creat el graf previament, executa la comanda /graph <distance> <poblation> per continuar")
	elif numErr == 3:
		bot.send_message(chat_id=update.message.chat_id,text="Error el subgrafGraph generat no te cap ciutat, introdueixi altres valors als parametres")
	elif numErr == 4:
		bot.send_message(chat_id=update.message.chat_id,text="No has definit [lat lon] previament, has de introduirlos en la comanda")


def comandes(comanda,bot,update):
	if comanda == "start":
		bot.send_message(chat_id=update.message.chat_id,text="/start  => aquesta comanda es necesaria per poder usar la resta de comandes que veiem en el /help")
	elif comanda == "author":
		bot.send_message(chat_id=update.message.chat_id,text="/author  => retorna el nom del Creador del programa i el seu correu de la fib")
	elif comanda == "graph":
		bot.send_message(chat_id=update.message.chat_id,text="/graph <distance> <poblation> => crea un graph on els nodes son les ciutats amb població major al parametre població i les arestes que conecten aquests graph com a molt son de distancia del parametre")
	elif comanda == "nodes":
		bot.send_message(chat_id=update.message.chat_id,text="/nodes => mostra el nombre de ciutats que conformen el graf")
	elif comanda == "edges":
		bot.send_message(chat_id=update.message.chat_id,text="/edges => mostra el nombre de connexions entre ciutats que conformen el graf")
	elif comanda == "components":
		bot.send_message(chat_id=update.message.chat_id,text="/components => mostra el nombre components conexes que conformen el graf")
	elif comanda == "plotpop":
		bot.send_message(chat_id=update.message.chat_id,text="/plotpop <distance> [lat lon] => mostra un mapa relacionant cada ciutat amb el volum de població d'aquestes, la relació es de 1 pixel de radi per 100000 habitants")
	elif comanda == "plotgraph":
		bot.send_message(chat_id=update.message.chat_id,text="/plotgraph <distance> [lat lon] => mostra en un mapa les ciutats i les seves respectives connexions")
	elif comanda == "plotpop":
		bot.send_message(chat_id=update.message.chat_id,text="/route <Nom ciutat 1> <codi país ciutat 1> <Nom ciutat2> <codi país ciutat2> => retorna un mapa printant la ruta mes curta entre Ciutat 1 i Ciutat 2 en cas de que la hi hagi")



class areaTreball:
	def __init__(self):
		self.started = False
		self.wgm = None
		self.lat = None
		self.lon = None

	def start(self,bot, update):
		if not self.started:
			self.started = True
			bot.send_message(chat_id=update.message.chat_id,text="HOLA, a partir d'ara ja pots usar totes les comandes, consulta el /help per a més info al respecte. \n Estic llegint totes les dades, espera fins que et confirmi que les he llegit, gracies.")
			self.wgm = WorkGraphMaps()
			bot.send_message(chat_id=update.message.chat_id,text="Ja he acabat de llegir totes les dades, endevant utilitzant-me :D")
		else:
			bot.send_message(chat_id=update.message.chat_id,text="HOLA, a partir d'ara ja pots usar totes les comandes, consulta el /help per a més info al respecte")


	def help(self,bot,update):
		bot.send_message(chat_id=update.message.chat_id,text="A continuació veuras un recull de les comandes disponibles, i una breu explicació del que fan.")
		comandes("start",bot,update)
		comandes("author",bot,update)
		comandes("graph",bot,update)
		comandes("nodes",bot,update)
		comandes("edges",bot,update)
		comandes("components",bot,update)
		comandes("plotpop",bot,update)
		comandes("plotgraph",bot,update)
		comandes("route",bot,update)

	def author(self,bot, update):
		if self.started:
			bot.send_message(chat_id = update.message.chat_id, text ="Pol Renau Larrodé, amb correu pol.renau@est.fib.upc.edu")
		else:
			errors(1,bot,update)
			
	def graph(self,bot,update,args):
		if self.started :
			if len(args) != 2 : 
				bot.send_message(chat_id=update.message.chat_id,text="No has fet la comanda correctament: /graph <distance> <population>")
			else:	
				distance = float(args[0])
				population = float(args[1])
				self.wgm.generaGraph(distance,population)
				bot.send_message(chat_id= update.message.chat_id, text ="OK")
		else:
			errors(1,bot,update)	

	def nodes(self,bot,update):
		if self.started:
			if self.wgm != None:
				numnodes = self.wgm.getNodes()
				bot.send_message(chat_id=update.message.chat_id,text="En el graf hi han %d nodes" %(numnodes) )
			else:
				errors(2,bot,update)
		else:
			errors(1,bot,update)
		
	def edges(self,bot,update):
		if self.started:
			if self.wgm != None:
				numedges = self.wgm.getEdges()
				bot.send_message(chat_id=update.message.chat_id,text="En el graf hi han %d arestes" %(numedges) )
			else:
				errors(2,bot,update)
		else:
			errors(1,bot,update)

	def components(self,bot,update):
		if self.started:
			if self.wgm != None:
				numedges = self.wgm.getComponents()
				bot.send_message(chat_id=update.message.chat_id,text="En el graf hi han %d components" %(numedges) )
			else:
				errors(2,bot,update)
		else:
			errors(1,bot,update)
	
	def plotpop(self,bot,update,args):
		if self.started:
			if self.wgm != None:
				if len(args) != 1 and len(args) != 3:
					bot.send_message(chat_id=update.message.chat_id,text="No has fet la comanda correctament: /plotpop <distance> [<lat> <lon>]")
				else:
					distance = float(args[0])
					if len(args) == 3:
						self.lat = float(args[1])
						self.lon = float(args[2])
					elif self.lat == None or self.lon == None:
						errors(4,bot,update)

					Err = self.wgm.getSubgraph(self.lat,self.lon,distance)
					if Err > 0:
						self.wgm.paintMapPop()
						bot.send_photo(chat_id=update.message.chat_id,photo=open('pop.png','rb'))
					else:
						errors(3,bot,update)
			else:
				errors(2,bot,update)
		else:
			errors(1,bot,update)

	def plotgraph(self,bot,update,args):
		if self.started:
			if self.wgm != None:
				if len(args) != 1 and len(args) != 3:
					bot.send_message(chat_id=update.message.chat_id,text="No has fet la comanda correctament: /plotpop <distance> [<lat> <lon>]")
				else:
					distance = float(args[0])
					if len(args) == 3:
						self.lat = float(args[1])
						self.lon = float(args[2])
					elif self.lat == None or self.lon == None:
						errors(4,bot,update)
				
					Err = self.wgm.getSubgraph(self.lat,self.lon,distance)
					if Err > 0:
						self.wgm.paintMapGraph()
						bot.send_photo(chat_id=update.message.chat_id,photo=open('graph.png','rb'))
					else:
						errors(3,bot,update)
			else:
				errors(2,bot,update)
		else:
			errors(1,bot,update)
			
	def route(self,bot,update,args):
		if self.started:
			if self.wgm != None:
				if len(args) == 4:
					ciutat1 = args[0] + ' ' + args[1]
					ciutat2 = args[2] + ' ' + args[3]
					Err = self.wgm.paintRoute(ciutat1,ciutat2)
					if Err > 0:
						bot.send_photo(chat_id = update.message.chat_id, photo = open('route.png','rb'))
					elif Err == -1:
						bot.send_message(chat_id=update.message.chat_id,text= "No exsiteix cami entre aquestes dues ciutats")
					elif Err == -2:
						bot.send_message(chat_id=update.message.chat_id,text= ciutat1 +" no esta en el graf, o be no coincideix en un 70 per cent de possibilitats amb una entrada possible, revisa l'entrada")
					elif Err == -3:
						bot.send_message(chat_id=update.message.chat_id,text= ciutat2 + " no esta en el graf, o be no coincideix en un 70 per cent de possibilitats amb una entrada possible, revisa l'entrada")
				else:
					bot.send_message(chat_id=update.message.chat_id,text="No has passat correctament els arguments, /route NomCiutat1, pais1 NomCiutat2, pais2")
			else:
				errors(2,bot,update)
		else:
			errors(1,bot,update)
			



# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()
# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


areaT = areaTreball()

dispatcher.add_handler(CommandHandler('start', areaT.start))

#aquesta funció no es necesari que estigui en el areaTreball, pero ho posem tot junt per concistencia.
dispatcher.add_handler(CommandHandler('help',areaT.help))

dispatcher.add_handler(CommandHandler('author',areaT.author))

dispatcher.add_handler(CommandHandler('graph',areaT.graph,pass_args =True))

dispatcher.add_handler(CommandHandler('nodes',areaT.nodes))

dispatcher.add_handler(CommandHandler('edges',areaT.edges))

dispatcher.add_handler(CommandHandler('components',areaT.components))

dispatcher.add_handler(CommandHandler('plotpop',areaT.plotpop,pass_args =True))

dispatcher.add_handler(CommandHandler('plotgraph',areaT.plotgraph,pass_args =True))

dispatcher.add_handler(CommandHandler('route',areaT.route,pass_args=True))


# engega el bot
updater.start_polling()
