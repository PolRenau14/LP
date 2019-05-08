import xml.sax

class ChgHandler(xml.sax.ConentHandler):
	mx = (0,'')

	def __init__(self):
		self.adreça = ''
		self.lliures = ''
		self.street = False
		self.number = False
		self.slots = False
	
	def startElement(self,name,attrs):
		if name == 'street':
			self.street = True
			self.adreça = ''
		elif name == 'streetNumber':
			self.number = True
			self.adreça += ', '
		elif name == 'slots':
			self.slots = True
			self.lliures = ''
	
	def characters(self, ch):
		if self.street or self.number:
			self.adreça += ch
		elif self.slots:
			self.lliures += ch
	
	def endElement(self,name):
		if name == 'street':
			self.street = False
		elif name == 'streetNumber':
			self.number = False
		elif name == 'slots':
			self.slots = False
		elif name == 'station':
			lliures = int(self.lliures)
			if lliures > ChgHandler.mx[0]:
				ChgHandler.mx = (lliures,self.adreça)
		
url = 'https://websevice.viabicing.cat/v1/getstations.php?v=1'

parser = xml.sax.make_parser()
parser.setContentHandler(ChgHandler())

parser.parse(url)

print(ChgHandler.mx)