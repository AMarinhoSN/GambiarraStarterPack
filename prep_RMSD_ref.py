__author__='AMarinhoSN'

from sys import argv
from sys import exit
'''
'
 >> Gambiarra Toolkit Starter Pack <<
	Plumed Package

>> prep_RMSD_ref.py 
USAGE: python prep_RMSD_ref.py reference.pdb
 
Set the w' and w weight sets on the PDB reference structure.
The w' is used for center of mass calculation and is written on OCCUPANCY
column (the first collumn after coordinates). The w is used to calculate 
how far the atoms have been displaced. 

'''
print "|-------------------------------------------------------------|"
print "|            >> Gambiarra Toolkit Starter Pack <<             |"
print "|                    >> prep_RMSD_ref.py <<                   |"
print "|                                                             |"
print "| This script write write the w' and w weight sets on a copy  |"
print "| of a given PDB input                                        |"
print "| structure.                                                  |"
print "| The w' is used for center of mass calculation and is written|"
print "| on OCCUPANCY column (the first collumn after coordinates).  |"
print "| The w is used how far the atoms have been displaced and is  |" 
print "| written on the BFACTOR column                               |" 
print "|-------------------------------------------------------------|"
print "| USAGE: python prep_RMSD_ref.py reference.pdb                |"
print "|_____________________________________________________________|"

# load input files
try:
    pdb_in_nm = argv[1]
    pdb_in = open(pdb_in_nm,'r')

except IndexError:
    print "!! ERROR: You should specify a valid input .pdb file !!"
    exit()

pdb_out_nm = argv[1].replace('.pdb','_ref.pdb')
pdb_out = open(pdb_out_nm,'w')

# define atom masses

AtomMasses={'C':12.0107, 'N':14.0067, 'H':1.0079, 'O':15.9994,'S':32.065}

# DO IT!

for line in pdb_in:
    if line.startswith('ATOM'):
        line_list = list(line)

        #1 - set w' as the mass of the atom:
        atom_type = line[13:15]
        atom_mass = str(round(AtomMasses[atom_type[0]]))[0:4]
        line_list[55:60] = atom_mass

        #2 - set w as the number of the atom
        atom_n = str(float(line[5:11]))
        line_list[60:66] = atom_n

        new_line = ''.join(line_list)
        ### DEBUG ###
        #print 'old: ', line
        #print 'new: ', new_line
        #############

        #3 - write line on new file:
        pdb_out.write(new_line)

pdb_out.write('TER')
pdb_out.close()

print ":: DONE ::"