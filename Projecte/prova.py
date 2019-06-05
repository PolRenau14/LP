#propies de Python
import csv
from math import asin, sin, cos, radians, atan2, degrees

#les definides en la especificació de la practica
import networkx as nx 
from staticmap import StaticMap, CircleMarker, Line
from haversine import haversine
from fuzzywuzzy import fuzz,process

#clase implementada de QuadTree, es especifica per aquest problema
from quadraticTree import QuadTree


def caclulaLat(lat, lon, distance):
  distance = distance * 1.5 # fem aixó per que hi ha error al buscar lat i lon li afegim una distancia de mes de la meitat per buscar la Lat
  lat = radians(lat)
  theta = distance/6371
  aux = degrees(asin(sin(lat)*cos(theta)+ cos(lat)*sin(theta)*cos(radians(0))))
  return abs(degrees(lat)-aux)


def calculaLon(lat,lon,distance):
  distance = distance * 1.5 # fem aixó per que hi ha error al buscar lat i lon li afegim una distancia de mes de la meitat per buscar la Lon
  lat = radians(lat)
  lon = radians(lon)
  theta = distance/6371
  aux =degrees( lon +atan2( sin(radians(90))*sin(theta)*cos(lat),cos(theta)-sin(lat)*sin(lat)))
  return abs(degrees(lon)-aux)


class WorkGraphMaps:

  def __init__(self):
    self.listaTodo = self.getData()
    self.lista = None
    self.tree = QuadTree(None,None)
    self.graph = nx.Graph()
    self.subgraph = nx.Graph()
    self.cities = {}
    self.choices = []

  def getData(self): 
    print("Entro")
    with open('worldcitiespop.csv', 'r') as f:
      reader = csv.reader(f)
      print(reader)
      your_list = list(reader)
    print("Surto")
    return your_list

  def generaGraph(self,distance,population):
    distance = float(distance)
    population = float(population)
    print("a por el Tree")
    self.createTree(population)
    print("a por el Graph")
    self.createGraph(distance)
    print("Todo hecho")

  def getNodes(self):
    if self.graph != None:
      return len(self.graph.nodes())
    return 0

  def getEdges(self):
    if self.graph != None:
      return len(self.graph.edges())
    return 0

  def getComponents(self):
    if self.graph != None:
      return nx.number_connected_components(self.graph)
    return 0


  #tree te el Quadtree de les ciutats que pasen el tall de població
  #La funció modifica self.llista amb les ciutat que estan al arbre
  def createTree(self,val):
    first = True
    pos = 0
    aux = []

    for i in self.listaTodo:
      if i[4] != '' and i[0] != 'Country' and float(i[4]) > val:
        if not first:
          lat = float(i[5])
          lon = float(i[6])
          self.tree.InsertValue(lat,lon,pos)
          aux.append(i)
        else:
          self.tree.lat = float(i[5])
          self.tree.lon = float(i[6])
          self.tree.index = pos
          first = False
          aux.append(i)
        codi = i[0]
        nom = i[1]
        self.cities[nom+' '+codi] = pos
        self.choices.append(nom+' '+codi)
        pos += 1
    self.lista = aux

  def createGraph(self,d):
    pos = 0
    for i in self.lista:
      lat = float(i[5])
      lon = float(i[6])
      #tornen les coordenades dels vertex del quadrat que circumscriu a la Circumferencia.
      sumLat = caclulaLat(lat,lon,d)
      sumLon = calculaLon(lat,lon,d)
      aux = self.tree.FoundQuadrant(lat-sumLat,lat+sumLat,lon-sumLon,lon+sumLon)
      for j in aux:
        lat1 = float(j[0])
        lon1 = float(j[1])
        index = int(j[2])
        dist = haversine((lat,lon),(lat1,lon1))
        if dist != 0 and dist <= d:
          self.graph.add_edge(pos,index,weight=dist)
      self.graph.add_node(pos)
      pos += 1

#en cas de que el subgraf generat sigui buit retorna 0, altrament 1
  def getSubgraph(self,lat,lon,d):
    sumLat = caclulaLat(lat,lon,d)
    sumLon = calculaLon(lat,lon,d)
    print("HI")
    auxList = self.tree.FoundQuadrant(lat-sumLat,lat+sumLat,lon-sumLon,lon+sumLon)
    aux = []
    for i in auxList:
      aux.append(i[2])

    graphAux = self.graph.subgraph(aux)
    self.subgraph = graphAux
    if len(self.subgraph.nodes) <= 0:
      return 0
    else:
      return 1

  def getLatandLonList(self,auxList):
    aux = [] 
    for i in auxList:
      lat = float(self.lista[i][5])
      lon = float(self.lista[i][6])
      point = (lon,lat)
      aux.append(point)
    return aux

  #def isInGraph(self,val):
  #  for i in self.graph.nodes():
   #   if i == val:
    #    return True
    #return False

  def paintMapGraph(self):
    m = StaticMap(2000,1500,20)
    for (n, nbrs) in self.subgraph.edges:
      origen = (float(self.lista[int(n)][6]),float(self.lista[int(n)][5]))
      desti = (float(self.lista[int(nbrs)][6]),float(self.lista[int(nbrs)][5]))
      m.add_line(Line([origen,desti],'blue',2))
    for n in self.subgraph.nodes:
      point = (float(self.lista[int(n)][6]),float(self.lista[int(n)][5]))
      m.add_marker(CircleMarker(point,'red',7))
    image = m.render()
    image.save('graph.png')

  def paintMapPop(self):
    m = StaticMap(2000,1500,20)
    for n in self.subgraph.nodes:
      point = (float(self.lista[int(n)][6]),float(self.lista[int(n)][5]))
      pob = float(self.lista[int(n)][4])
      tam = int(pob/100000)+1
      m.add_marker(CircleMarker(point,'red',tam))
    image = m.render()
    image.save("pop.png")

# si la coincdencia es menor al 70 % no es valida la entrada.
  def getCity(self,query):
    maxCoincident = process.extractOne(query,self.choices)
    print(maxCoincident)
    print(query)
    if float(maxCoincident[1]) > 70:
      return int(self.cities[maxCoincident[0]])
    else:
      return -1

#En cas d'error (no hi ha camí) retorna -1, si origen no es valid retorna -2
# si desti no es valid retorna -3, altrament 1.
  def paintRoute(self,ini,fin):
    ini = self.getCity(ini)
    fin = self.getCity(fin)
    print(self.lista[ini])
    print(fin)
    if ini == -1:
      return -2
    elif fin == -1:
      return -3
    elif (nx.has_path(self.graph,source=ini,target=fin)):
      listaRuta = nx.shortest_path(self.graph,source=ini,target=fin)
      auxListaRuta = self.getLatandLonList(listaRuta)
      m = StaticMap(2000,1500,20)
      m.add_line(Line(auxListaRuta,'blue',3))
      for i in auxListaRuta:
        m.add_marker(CircleMarker(i,'red',10))
      image = m.render()
      image.save('route.png')
      return 1
    else :
      return -1

