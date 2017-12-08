import networkx as nx
import itertools as it

#put edges in a list
edges = []
with open("data.txt","r") as f:
    for line in f:
        edges.append(line.split())

# build graph from edge list and set default probability and attributes
G = nx.from_edgelist(edges)
for node in G:
    G.nodes[node]['prob'] = 0.25
    G.nodes[node]['clicked'] = False
    G.nodes[node]['impression'] = False


def impressionList(M,k):
    ''' A method to return the possible ways to give impressions across stages. So supplied M=6
     and k=3 it will produce a list that starts like [006, 015, 105 ....... etc] '''
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
    ''' Method that scales the probabilities in a Graph based on who clicks. Uses a new metric'''
    alpha = 0.15
    beta = 0.01
    diam = nx.diameter(A)
    ecc = nx.eccentricity(A)
    numnodes = nx.number_of_nodes(A)
    # set attributes to show who got an impression and if they clicked
    for person,action in zip(comb,outcome):
        A.nodes[person]['impression'] = True
        if action == '1':
            A.nodes[person]['clicked'] = True        
    #Looks for nodes that have not yet been given an impression and checks who clicked in order to calculate scale factor
    for node in A:
        if A.nodes[node]['impression'] == True:
            continue
        n = 0
        for neighbors in A.neighbors(node):
            if A.nodes[neighbors]['clicked'] == True:
                n += 1
        f = len(A[node])
        A.nodes[node]['prob'] = max(0,min(1,(0.25+alpha*pow(n/f,0.5))))

def clicksfromoutcome(B, imp, comb, outcome):
    ''' Calculates the expected number of clicks from a particular outcome. 
        Since this is a 2 stage solution it just adds the best set of probabilites from the next stage if they are available'''
    clicks = 0
    temp = 1.0
    for person,action in zip(comb, outcome):
        if action == '1':
            clicks += 1
            temp *= B.nodes[person]['prob']
        else:
            temp *= (1 - B.nodes[person]['prob'])
    return (temp * (clicks + sum([x[0] for x in maxProbs(B, imp[1])])))

def maxProbs(C, num_probs):
    ''' returns a list containing the top probabilities of the last stage '''
    top_probs = []
    for node in C:
        if C.nodes[node]['impression'] == False:
            top_probs.append((C.nodes[node]['prob'],node))
    top_probs.sort(reverse=True)
    return top_probs[:num_probs]

M=5
k=2
results = {}
for imp in impressionList(M,k):
    # loops through (0,5) -> (1,4) -> (2,3) -> etc
    for comb in it.combinations(G.nodes(),imp[0]):
        # loops through combinations of nodes choosing x at a time where x is the first element of the imp tuple
        expectedClicksForCombination = 0 # reset the total clicks for this combination
        for outcome in it.product('01',repeat=imp[0]):
            # loops through the possible decision outcomes of the selected combination
            G1 = G.copy() # make a deep copy of the main graph
            scaleNodeProb(G1,comb,outcome) # scale the probabilities
            expectedClicksForCombination += clicksfromoutcome(G1, imp, comb, outcome) # accumulate the expected clicks
        results[(imp,comb)] = expectedClicksForCombination # add to a dictionary
ans = max(results.items(), key=lambda x:x[1])
print("The highest expected number of clicks is obtained by giving {} impressions in the first stage to {} and {} impressions in the last stage for a total of {} clicks"\
    .format(ans[0][0][0],ans[0][1],ans[0][0][1],ans[1]))