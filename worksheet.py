from modules.open_digraph import *


n0 = [node(0, 'i', {}, {1:1})]
inp= [1,2,3] 
outputs = [5]
g = open_digraph(inp , outputs , n0)
n = node(0, 'i', {}, {1:1})
print(g)