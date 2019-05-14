import csv
#from staticmap import StaticMap, CircleMarker

# pinta totes les ciutats que tenen poblacio ( 46mil aprox.)
def pintaPoints(lista):
    m = StaticMap(400,400,10)
    for i in lista:
        lat = i[6]
        lon = i[5]
        m.add_marker(CircleMarker((lat,lon),'red',6))
    image = m.render()
    image.save('mapa.png')


def procesList(lista):
  return filter(lambda x: x[4] != '', lista)
  #aquest filter el que fa es que comproba que tinguin població.


with open('worldcitiespop.csv', 'r') as f:
  reader = csv.reader(f)
  your_list = list(reader)



print(procesList(your_list)[4])