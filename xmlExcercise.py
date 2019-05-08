import urllib.request
import xml.etree.Element.Tree as ET
from math import sin,cos,swrt,atan2,radians

url = 'https://wservice.viabicing.cat/v1/getstations.php?v=1'
response = urllib.request.urlopen(url)
xml = response.read()

root = ET.fromstring(xml)
print(root.tag)
#print(root.atrib)
#print(root.text)

##mostra el crrrer de l'estació amb major nombre de slots
mx = (0,'')
for child in root.findall('station'):
	slots = int(child.find('slots').text)
	if slots > mx[0]:
		mx = (slots, child.find('street').text + ', ' + child.find('streetNumber').text)
print(mx)

def getDistance(lat,lon,latAcc,lonAcc):
	R = 6373.0 #Radi de la terra aprox.
	dlon = lonAcc - lon
	dlat = latAcc - lat

	a = sin(dlat / 2 )**2 + cos(lat)*cos(latAcc)*sin(dlon/2)**2
	c = 2* atan2(sqrt(a),sqrt(1-a))

	distance = R * c

	return distance

def calcProxim(lat,lon):
	lat = radians(lat)
	lon = radians(lon)
	estacioMesProx = (4930949032,'No tens cap estació amb Bicibletes Disponibles')

	for child in root.findall('station'):
		if int(child.find('bikes').text) > 0: # vol dir que te bicis disponibles
			latAcc = radians(float(child.find('lat').text))
			lonAcc = radians(float(child.find('long').text))
			aux = getDistance(lat,lon,latAcc,lonAcc)
			if aux < estacioMesProx[0]:
				estacioMesProx = (aux,child.find('street').text + ', ' + child.find('streetNumber').text)

	return estacioMesProx