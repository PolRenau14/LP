import csv
from staticmap import StaticMap, CircleMarker

# pinta totes les ciutats que tenen poblacio ( 46mil aprox.)
def pintaPoints(lista):
    m = StaticMap(2000,1500,100)
    for i in lista:
        lat = float(i[5])
        lon = float(i[6])
        m.add_marker(CircleMarker((lon,lat),'red',1))
    image = m.render()
    image.save('mapPoints.png')


def procesList(lista,val):
  return filter(lambda x: x[4] != '' and x[0] != 'Country' and int(x[4]) > val, lista)
  #aquest filter el que fa es que comproba que tinguin població.
  #tambe podem fer que al llegir del document csv, llegim per files 
  #( si la població es '' no la afegim a la llista ens estalviem un recorregut de la llista)


with open('worldcitiespop.csv', 'r') as f:
  reader = csv.reader(f)
  your_list = list(reader)


pintaPoints(procesList(your_list,89000))