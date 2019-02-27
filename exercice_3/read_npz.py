import numpy as np

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
