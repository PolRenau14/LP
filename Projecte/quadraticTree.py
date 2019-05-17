
#aplana les llistes (llistes de llistes en una unica llista)
def aplanaList(l):
	aux = []
	for x in l:
		if isinstance(x,list):
			aux =aux + aplanaList(x)
		else:
			aux.append(x)
	return aux

		


class QuadTree:

	def __init__(self,lat=None,lon=None,index = None):

		self.left1 = None
		self.left2 = None
		self.right1 = None
		self.right2 = None
		self.lat = lat
		self.lon = lon
		self.index = index

	
	def PrintTree(self,x,s):
		if self.left1:
			self.left1.PrintTree(x+1,"left1 => ")
		if self.left2:
			self.left2.PrintTree(x+1,"left2 => ")
		print("\t" * x + s+"(Latitud %f, Longitud: %f   Numero %d)" %(self.lat,self.lon,self.index))

		if self.right1:
			self.right1.PrintTree(x+1,"right1 => ")
		if self.right2:
			self.right2.PrintTree(x+1,"right2 => ")
		print("--------------------------------------------------")

	def InsertValue(self,lat,lon,index):
		if lat < self.lat: # van a la part left
			if lon < self.lon: #left1
				if self.left1:
					self.left1.InsertValue(lat,lon,index)
				else:
					self.left1 = QuadTree(lat,lon,index)
			else:
				if self.left2: 
					self.left2.InsertValue(lat,lon,index)
				else:
					self.left2 = QuadTree(lat,lon,index)
		else: # van a la part right
			if lon < self.lon: # right 1
				if self.right1:
					self.right1.InsertValue(lat,lon,index)
				else:
					self.right1 = QuadTree(lat,lon,index)
			else:
				if self.right2:
					self.right2.InsertValue(lat,lon,index)
				else:
					self.right2 = QuadTree(lat,lon,index)

	def IsinQuadrant(self,latMIN,latMAX,lonMIN,lonMAX):
		#print("lat min: %f, lat max: %f, lonMin: %f, lonMAX: %f. En LAT: %f, LON: %f" %(latMIN,latMAX,lonMIN,lonMAX,self.lat,self.lon))
		if self.lat >= latMIN and self.lat <= latMAX:
			if self.lon >= lonMIN and self.lon <= lonMAX:
				return True
		return False

	def FoundQuadrant(self,latMIN,latMAX,lonMIN,lonMAX):
		aux = []
		if self != None:
			if self.IsinQuadrant(latMIN,latMAX,lonMIN,lonMAX):
				aux.append((self.lat,self.lon,self.index))
				if self.left1 != None:
					aux.append(self.left1.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
				if self.left2 != None:
					aux.append(self.left2.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
				if self.right1 != None:
					aux.append(self.right1.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
				if self.right2 != None:
					aux.append(self.right2.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
			else:

				#D1 
				if self.lat > latMAX and self.lon > lonMAX:
					if self.left1 != None:
						aux.append(self.left1.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
				#D2 
				elif self.lat < latMIN and self.lon > lonMAX:
					if self.right1 != None:
						aux.append(self.right1.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
				#D3 
				elif self.lat < latMIN and self.lon < lonMIN:
					if self.right2 != None:
						aux.append(self.right2.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
				#D4 
				elif self.lat > latMAX and self.lon < lonMIN:
					if self.left2 != None:
						aux.append(self.left2.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))

				elif self.lat <= latMAX and self.lat >= latMIN: #estic en range en la lat
					if self.lon > lonMAX:
						if self.left1 != None:
							aux.append(self.left1.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
						if self.right1 != None:
							aux.append(self.right1.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
					else:
						if self.right2 != None:
							aux.append(self.right2.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
						if self.left2 != None:
							aux.append(self.left2.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))

				elif self.lon <= lonMAX and self.lon >= lonMIN:
					if self.lat > latMAX:
						if self.left1 != None:
							aux.append(self.left1.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
						if self.left2 != None:
							aux.append(self.left2.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
					else:
						if self.right1 != None:
							aux.append(self.right1.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
						if self.right2 != None:
							aux.append(self.right2.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
				else:
					print("No Soc Res")
		return aplanaList(aux)


