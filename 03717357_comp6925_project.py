import networkx
import itertools as it

edges = []
with open("data.txt","r") as f:
    for line in f:
        edges.append(line.split())

G = nx.from_edgelist(edges)
print(G.nodes)
print(G.edges)
print(G.adj)
print(G.degree)
print(G['Pat'])

M = 5
k = 2
def digitsum(M,k):
    l = []
    precision = k
    for i in range(pow(10,k)):
        s = f'{i:0{precision}}'
        tot = 0
        for x in s:
            tot += int(x)
        if tot == M:
            l.append(tuple(map(int,tuple(s))))
    return l
for outcome in it.product('01',repeat=4):
    print(tuple(map(int,outcome)))
for comb in it.combinations('ABCD',3):
    print(comb)
print(digitsum(5,2))