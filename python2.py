class Tree:
	def __init__(self,x):
		self.rt = x
	def addChild(self,a):
		self.child.append(a)
	def root(self):
		return self.rt
	def ithChild(self,n):
		if n < len(self.child) and n >= 0 :
			return self.child[n]
		else:
			return "Fora de rang"
	def numChildren(self):
		return len(self.child)
	
class Pre(Tree):
	def preorder(self):
		aux = self.rt
		aux.append(self.child)
		return aux
		
			