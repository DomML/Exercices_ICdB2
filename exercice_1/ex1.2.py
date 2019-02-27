import MDAnalysis, numpy as np
from MDAnalysis.coordinates.PDB import PDBReader, PDBWriter
from MDAnalysis.core.AtomGroup import Atom

rec = MDAnalysis.Universe("./receptor.pdb")

# # COM et ecriture du pdb
allAtoms = rec.select_atoms("all")
COM =  np.around(allAtoms.center_of_mass(compound="group"), 3)
print("COM :", np.around(allAtoms.center_of_mass(compound="group"), 3))

COM_atom = rec.select_atoms("protein and name CA and resid 67 and segid AP1")

COM_atom[0].position = COM
COM_atom[0].name = "DUM"
COM_atom.write("COM.pdb")

# # Rayon de gyration
print("Rg :", allAtoms.radius_of_gyration())