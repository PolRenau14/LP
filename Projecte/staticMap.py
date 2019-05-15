from staticmap import StaticMap, Line, CircleMarker

#tracem una linea del origen al desti (linea recta en el mapa)

origen = (1.932048, 41.386759) #Valliran
desti = (2.081834,41.471379) #SantCugat

m = StaticMap(300,400,0)
m.add_line(Line((origen, desti), 'blue', 1))
m.add_marker(CircleMarker(origen,'red',6))
m.add_marker(CircleMarker(desti,'red',6))
image = m.render()
image.save('map.png')