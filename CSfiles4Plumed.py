__author__ = "AMarinhoSN"

'''
CS_4Plumed.py

This script prepare files for chemical shift and/or Residual Dipolar Coupling 
restrained metadynamic simulations using Gromacs+Plumed based on a standard 
file available at BMRB.

'''
from sys import argv

#===| LOAD DATA |===*
try: 
    bmrb_cshift_f = argv[1]
except:
    print "ERROR: you do not specify input file"
    
scr_cshift_file = open(bmrb_cshift_f,'r')

#---| Create the individual *shift.dat files for Plumed |---#
Cshift_f = open('Cshift.dat', 'w')
CAshift_f = open('CAshift.dat', 'w')
CBshift_f = open('CBshift.dat', 'w')
HAshift_f = open('HAshift.dat', 'w')
Hshift_f = open('CAshift.dat', 'w')
Nshift_f = open('Nshift.dat','w')

#---| JUST DO IT! |---#
# Read the BMRB source file write its info into plumed format
# TODO : add '#' to the first and last files

for line in scr_cshift_file:
    if "_" in line or "'" in line:
        continue
    else:
        try:
            
            print line[18:22]
            line_n = int(line[0:9])
            res_i = int(line[18:21])
            atom = line[30]
            cs = float(line[35:42])
            atom_type = line[26:28].replace(" ","")
            
            print res_i

            if atom_type == 'C':
                 Cshift_f.write(str(res_i)+'\t'+str(cs)+'\n')
                 continue
            if atom_type == 'CA':
                 CAshift_f.write(str(res_i)+'\t'+str(cs)+'\n')
                 continue
            if atom_type == 'CB':
                 CBshift_f.write(str(res_i)+'\t'+str(cs)+'\n')
                 continue
            if atom_type == 'H':
                 Hshift_f.write(str(res_i)+'\t'+str(cs)+'\n')
                 continue
            if atom_type == 'HA':
                 HAshift_f.write(str(res_i)+'\t'+str(cs)+'\n')
                 continue
            if atom_type == 'N':
                 Nshift_f.write(str(res_i)+'\t'+str(cs)+'\n')
                 continue
        except:
            continue