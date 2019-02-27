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
unique_input_id = np.unique(interactions[0][:,0])
unique_output_id = np.unique(interactions[3][:,1])

unique_input_node = [i for i in DG.nodes() if "_0" in i]
unique_output_node = [i for i in DG.nodes() if "_4" in i]


def countPath(node, DG):
    if len(list(DG.successors(node))) == 0:
        return 1
    else:
        return sum([countPath(p_node, DG) for p_node in DG.successors(node)])


print("Nombre de chemins possibles : ")
print(sum([countPath(start_node, DG) for start_node in unique_input_node]))


# ### C'est rassurant, les méthodes brutes (voir notebook) et dynamiques donnent les mêmes résultats !