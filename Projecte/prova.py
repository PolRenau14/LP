import csv
from staticmap import StaticMap, CircleMarker, Line
from quadraticTree import QuadTree
from haversine import haversine
import networkx as nx 

#Nomes per les probes
import timeit

def getData(): 
  with open('worldcitiespop.csv', 'r') as f:
    reader = csv.reader(f)
    your_list = list(reader)

  return your_list

#tree te el Quadtree de les ciutats que pasen el tall de població
#La funció retornara la llista de ciutats plenes
def createTree(lista,val,tree):
  first = True
  pos = 0
  aux = []
  for i in lista:
    if i[4] != '' and i[0] != 'Country' and int(i[4]) > val:
      if not first:
        lat = float(i[5])
        lon = float(i[6])
        tree.InsertValue(lat,lon,pos)
        aux.append(i)
      else:
        tree.lat = float(i[5])
        tree.lon = float(i[6])
        tree.index = pos
        first = False
        aux.append(i)
      pos += 1
  return aux

def createGraph(graph,tree,lista,d):
  pos = 0
  for i in lista:
    lat = float(i[5])
    lon = float(i[6])
    aux = tree.FoundQuadrant(lat-1,lat+1,lon-1,lon+1)
    for j in aux:
      lat1 = float(j[0])
      lon1 = float(j[1])
      index = int(j[2])
      dist = haversine((lat,lon),(lat1,lon1))
      if dist != 0 and dist <= d:
       # print("Dist entre: ",lista[index]," y la :  ", lista[pos])
        print("La latt del primer es: %f y la lon %f" %(lat1,lon1))
        #print(dist)
        graph.add_edge(pos,index,weight=dist)
    graph.add_node(pos)
    pos += 1


def getSubgraph(graph,lat,lon,distance,tree):
  auxList = tree.FoundQuadrant(lat-15,lat+15,lon-15,lon+15)
  print("He acabat")
  aux = []
  for i in auxList:
    aux.append(i[2])

  graphAux = graph.subgraph(aux)
  return graphAux

def paintMapGraph(graph,lista):
  m = StaticMap(2000,1500,100)
  for (n, nbrs) in graph.edges:
    origen = (float(lista[int(n)][6]),float(lista[int(n)][5]))
    desti = (float(lista[int(nbrs)][6]),float(lista[int(nbrs)][5]))
    m.add_line(Line((origen,desti),'blue',1))
  for n in graph.nodes:
    point = (float(lista[int(n)][6]),float(lista[int(n)][5]))
    m.add_marker(CircleMarker(point,'red',5))
  image = m.render()
  image.save('graph.png')



def paintMapPop(graph,lista):
  for n in graph.nodes:
    point = (float(lista[int(n)][6]),float(lista[int(n)][5]))
    pob = float(lista[int(n)][4])

your_list = getData()
start = timeit.default_timer()
tree = QuadTree(None,None)
lista = createTree(your_list,100000,tree)
G = nx.Graph()
createGraph(G,tree,lista,400)
stop = timeit.default_timer()
print("Time: ", stop-start)
print("GRAF creat")
#paintMapGraph(G,lista)
Gaux = getSubgraph(G,41,2,90,tree)

paintMapGraph(Gaux,lista)
