import csv
import networkx as nx

with open('./worldcitiespop.csv', 'r') as f:
	reader = csv.reader(f)
	your_list = list(reader)

if your_list[1][4] == "" :
	print("Null")
else:
	print(your_list[1][4])
