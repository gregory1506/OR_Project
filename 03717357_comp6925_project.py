import networkx as nx
import itertools as it

edges = []
with open("data_frompaper.txt","r") as f:
    for line in f:
        edges.append(line.split())

G = nx.from_edgelist(edges)
for node in G:
    G.nodes[node]['prob'] = 0.25
    G.nodes[node]['clicked'] = False
    G.nodes[node]['impression'] = False


def impressionList(M,k):
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

def scaleNodeProb(A,comb,outcome):
    alpha = 0.15
    for person,action in zip(comb,outcome):
        A.nodes[person]['impression'] = True
        if action == '1':
            A.nodes[person]['clicked'] = True        
    for node in A:
        n = 0
        for neighbors in A.neighbors(node):
            if A.nodes[neighbors]['clicked'] == True:
                n += 1
        f = len(A[node])
        if n >= 0:
            A.nodes[node]['prob'] += max(0,min(1,(0.25+alpha*n/f)))

def clicksfromoutcome(B, imp, comb, outcome):
    clicks = 0
    temp = 1
    for person,action in zip(comb, outcome):
        if action == '1':
            clicks += 1
            temp *= B.nodes[person]['prob']
        else:
            temp *= (1 - B.nodes[person]['prob'])
    return (temp * (clicks + maxProbs(B, imp[1])))

def maxProbs(C, num_probs):
    list_of_probs = []
    for node in C:
        if C.nodes[node]['impression'] == False:
            list_of_probs.append(C.nodes[node]['prob'])
    list_of_probs.sort(reverse=True)
    return sum(list_of_probs[:num_probs]) 

M=4
k=2
results = {}
for imp in impressionList(M,k):
    for comb in it.combinations(G.nodes(),imp[0]):
        expectedClicksForCombination = 0
        for outcome in it.product('01',repeat=imp[0]):
            G1 = G.copy()
            scaleNodeProb(G1,comb,outcome)
            expectedClicksForCombination += clicksfromoutcome(G1, imp, comb, outcome)
        results[(imp,comb)] = expectedClicksForCombination


print(max(results.items(), key=lambda x:x[1]))
# for key in results:
#     if results[key] > 2.6:
#         print(key, results[key])

