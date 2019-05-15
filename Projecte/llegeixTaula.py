import csv
import networkx as nx

with open('./worldcitiespop.csv', 'r') as f:
	reader = csv.reader(f)
	your_list = list(reader)

print(your_list[1][3])

G = nx.petersen_graph()
nx.draw(G, with_labels = True, font_weight='bold')