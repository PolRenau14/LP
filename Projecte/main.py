from prova import WorkGraphMaps


#Nomes per les probes
import timeit


wgm = WorkGraphMaps()

start = timeit.default_timer()

wgm.generaGraph("200","100000")

stop = timeit.default_timer()
print("Time: ", stop-start)

Err = wgm.getSubgraph(41,2,1000)

if Err > 0 :

  Err = wgm.paintRoute('bojnurd','marseille fr')

  if Err < 1:
    print("No hi ha cami")
else:
  print("El subgraph era vuit")
