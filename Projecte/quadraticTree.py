class QuadTree:

	def __init__(self,lat,lon):

		self.left1 = None
		self.left2 = None
		self.right1 = None
		self.right2 = None
		self.lat = lat
		self.lon = lon

	def PrintTree(self):
		if self.left1:
			self.left1.PrintTree()
		if self.left2:
			self.left2.PrintTree()
		print("(Latitud %f, Longitud: %f)" %(self.lat,self.lon))

		if self.right1:
			self.right1.PrintTree()
		if self.right2:
			self.right2.PrintTree()


	def InsertValue(self,lat,lon):
		if lat < self.lat: # van a la part left
			if lon < self.lon: #left1
				if self.left1:
					self.left1.InsertValue(lat,lon)
				else:
					self.left1 = QuadTree(lat,lon)
			else:
				if self.left2: 
					self.left2.InsertValue(lat,lon)
				else:
					self.left2 = QuadTree(lat,lon)
		else: # van a la part right
			if lon < self.lon: # right 1
				if self.right1:
					self.right1.InsertValue(lat,lon)
				else:
					self.right1 = QuadTree(lat,lon)
			else:
				if self.right2:
					self.right2.InsertValue(lat,lon)
				else:
					self.right2 = QuadTree(lat,lon)

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
				aux.append((self.lat,self.lon))
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
					if self.left2 != None:
						aux.append(self.left2.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))
				#D4 
				elif self.lat > latMAX and self.lon < lonMIN:
					if self.right2 != None:
						aux.append(self.right2.FoundQuadrant(latMIN,latMAX,lonMIN,lonMAX))

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
		return aux



			
	


root = QuadTree(3,4)
root.InsertValue(3,6)
root.InsertValue(4,5)
root.InsertValue(3,3)

auxiliar = root.FoundQuadrant(3,5,3,6)

print(auxiliar)