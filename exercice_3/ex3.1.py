import numpy as np
import networkx as nx
import itertools
import matplotlib.pyplot as plt

a=np.load("UUU-top1000-5frag-4A.npz")
'''
a.keys() = ['max_rmsd',
             'interactions-2',
             'interactions-3',
             'interactions-0',
             'interactions-1',
             'nfrags']
'''

interactions = [a['interactions-%i'%i] for i in range(4)]
interactions_nn = []

for int_level in range(len(interactions)):
    curIntLevel = []
    for int_pair in range(interactions[int_level].shape[0]):
        curIntLevel.append([str(interactions[int_level][int_pair][0]) + "_" + str(int_level),
                            str(interactions[int_level][int_pair][1]) + "_" + str(int_level+1)])
    interactions_nn.append(curIntLevel)


DG = nx.DiGraph()
for int_level in range(len(interactions_nn)):
    for edge in interactions_nn[int_level]:
        DG.add_edge(*edge)
DG.number_of_nodes(), DG.number_of_edges()


# In[7]:
unique_input_node = [i for i in DG.nodes() if "_0" in i]


def initCount(DG):
    for node in DG.nodes:
        DG.nodes[node]['count_path_value'] = -1

def countPath(node, DG):
    if DG.nodes[node]['count_path_value'] == -1:
        if len(list(DG.successors(node))) == 0:
            DG.nodes[node]['count_path_value']  = 1
        else:
            DG.nodes[node]['count_path_value']  = sum([countPath(p_node, DG) for p_node in DG.successors(node)])
    return DG.nodes[node]['count_path_value']

initCount(DG)
print("Nombre de chemins possibles : ")
print(sum([countPath(start_node, DG) for start_node in unique_input_node]))


# ### C'est rassurant, les méthodes brutes (voir notebook) et dynamiques donnent les mêmes résultats !

def initPath(DG):
    for node in DG.nodes:
        DG.nodes[node]['bestSuccessor'] = None
        DG.nodes[node]['bestPath'] = []
        DG.nodes[node]['bestPath_value'] = 0
        DG.nodes[node]['node_value'] = int(node.split("_")[0])
        
def bestPath(node, DG):
    if DG.nodes[node]['bestSuccessor'] == None:
        if len(list(DG.successors(node))) == 0:
            DG.nodes[node]['bestSuccessor'] = (DG.nodes[node]['node_value'], node)
            DG.nodes[node]['bestPath_value'] = DG.nodes[node]['node_value']
        else:
            unsorted_successors = [[bestPath(p_node, DG)[0] + DG.nodes[node]['node_value'], p_node]
                                   for p_node in DG.successors(node)]
            sorted_successors = sorted(unsorted_successors, key=lambda tup: tup[0])
            DG.nodes[node]['bestSuccessor'] = sorted_successors[0]
            DG.nodes[node]['bestPath'] = [sorted_successors[0][1]] + DG.nodes[sorted_successors[0][1]]['bestPath']
            DG.nodes[node]['bestPath_value'] = DG.nodes[node]['node_value'] + DG.nodes[sorted_successors[0][1]]['bestPath_value']
    return DG.nodes[node]['bestSuccessor']

initPath(DG)
allBest = sorted([[bestPath(start_node, DG)[0] + DG.nodes[start_node]['node_value'], start_node]
                 for start_node in unique_input_node], 
                 key=lambda tup: tup[0])


print("Meilleur chemin et score associé : ")
print([allBest[0][1]] + DG.nodes[allBest[0][1]]['bestPath'], DG.nodes[allBest[0][1]]['bestPath_value'])