#conptabilitza el nombre d'elements diferents d'una llista.
from functools import reduce
from itertools import islice

#7.1.1
def countDif(l):
	s = set(l)
	return len(s)

#7.1.4
# converteix llistes de llistes en una unica llista ( tot aplant)
def aplanaList(l):
	aux = []
	for x in l:
		if isinstance(x,list):
			aux =aux + aplanaList(x)
		else:
			aux.append(x)
	return aux

#7.2.3
#el reduce es com un foldl
def invertirList(l):
	ini = []
	return reduce(lambda acc, x: [x] + acc, l, [])

#7.3.1
#implementació zipwith python
def zipWith(f,l1,l2):
	aux = []
	for (x,y) in zip(l1,l2):
		aux.append(f(x,y))
	return aux

#7.4.4
#retorna els factors de n encara que no siguin primers
def factorsCompres(n):
	return [x for x in range(1,n) if n%x == 0]

#7.4.5
#retorna les ternes pitagoriques entre 1 i N.
def ternes(n):
	return [(x,y,z) for x in range(1,n) for y in range(1,n) for z in range(max(x,y),n) if x*x + y*y == z*z ]


#7.5.1
# Genera els fibonacci ( infinita)
def fibonacci():
	n1= 0
	n2 = 1
	yield n2
	while True:
		aux = n2
		n2 = n1 + n2
		n1 = aux	
		yield n2
 


#llista = [1,2,3,4,93,41,3,2,4,132,2,2,-1,32,24,21,42,132,21]
#print(countDif(llista))
#print(invertirList(llista))
#llista = [[2,3],[1],[[1,8,[2],[1,2,4]],5,3]]
#print(aplanaList(llista))
#print(factorsCompres(93718))

#print(ternes(64))

l1 = [1,2,3,4,6,4]
l2 = [1,1,1,4,8]
#print(zipWith("f",l1,l2))

print(list(islice(fibonacci(),49)))