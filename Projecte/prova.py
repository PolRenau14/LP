import csv
from staticmap import StaticMap, CircleMarker, Line
from haversine import haversine
import networkx as nx 
from math import asin, sin, cos, radians, atan2, degrees

#clase implementada de QuadTree, es especifica per aquest problema
from quadraticTree import QuadTree


#Nomes per les probes
import timeit


  #Funciona Bé
def caclulaLat(lat, lon, distance):
  lat = radians(lat)
  theta = distance/6371
  aux = degrees(asin(sin(lat)*cos(theta)+ cos(lat)*sin(theta)*cos(radians(0))))
  return abs(degrees(lat)-aux)

#Funciona Bé
def calculaLon(lat,lon,distance):
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

  def getData(self): 
    with open('worldcitiespop.csv', 'r') as f:
      reader = csv.reader(f)
      your_list = list(reader)

    return your_list

  #tree te el Quadtree de les ciutats que pasen el tall de població
  #La funció retornara la llista de ciutats plenes
  def createTree(self,val):
    first = True
    pos = 0
    aux = []
    for i in self.listaTodo:
      if i[4] != '' and i[0] != 'Country' and int(i[4]) > val:
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
        nom = i[1]
        self.cities[nom] = pos
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

  def getSubgraph(self,lat,lon,d):
    sumLat = caclulaLat(lat,lon,d)
    sumLon = calculaLon(lat,lon,d)
    auxList = self.tree.FoundQuadrant(lat-sumLat,lat+sumLat,lon-sumLon,lon+sumLon)
    aux = []
    for i in auxList:
      aux.append(i[2])

    graphAux = self.graph.subgraph(aux)
    self.subgraph = graphAux

  def getLatandLonList(self,auxList):
    aux = [] 
    for i in auxList:
      lat = float(self.lista[i][5])
      lon = float(self.lista[i][6])
      point = (lon,lat)
      aux.append(point)
    return aux

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

  def paintRoute(self,ini,fin):
    listaRuta = nx.shortest_path(self.graph,source=ini,target=fin)
    auxListaRuta = self.getLatandLonList(listaRuta)
    m = StaticMap(2000,1500,20)
    m.add_line(Line(auxListaRuta,'blue',3))
    for i in auxListaRuta:
      m.add_marker(CircleMarker(i,'red',10))
    image = m.render()
    image.save('route.png')

#cami entre Zaragoza 1094, y marsella 1125

wgm = WorkGraphMaps()

start = timeit.default_timer()

wgm.createTree(100000)
wgm.createGraph(200)

stop = timeit.default_timer()
print("Time: ", stop-start)

wgm.getSubgraph(41,2,1500)

wgm.paintMapPop()
wgm.paintMapGraph()
print(wgm.lista[1094])
print(wgm.lista[1125])
num = wgm.cities['zaragoza'] 
print(num)
wgm.paintRoute(num,wgm.cities['marseille'])
