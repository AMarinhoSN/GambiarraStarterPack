__author__ = "AMarinhoSN"

'''
CS_4Plumed.py

This script prepare files for chemical shift and/or Residual Dipolar Coupling 
restrained metadynamic simulations using Gromacs+Plumed based on a standard 
NMR_STAR-v3.1 file available at BMRB.

'''
from sys import argv

def writeCShift(src_cshift_file):
    '''
    write residues with assgned CS and non assigned as "res_i 0.000"

    '''
    
    def writeNonAsgRes(pdb_res_idxs, res_i, prev_res, shift_file):
        '''
        write non CS assigned residues as "res 0.00"
        '''
        # get residues index 
        curr_res_idx = pdb_res_idxs.index(res_i)
        prev_res_idx = pdb_res_idxs.index(prev_res)
        # get gap between assigned residues
        non_asgn_gap =pdb_res_idxs[prev_res_idx:curr_res_idx]
        # write non assigned residue
        for each in non_asgn_gap:
            shift_file.write(str(each)+" 0.000\n")
            
    def writeSmart(res_i, prev_res, shift_f):
        '''
        write residues in 
        '''

        if res_i > prev_res:
            writeNonAsgRes(pdb_res_idxs,res_i,prev_res,shift_f)
            shift_f.write(str(res_i)+' '+str(cs)+'\n')  
        else:
            shift_f.write(str(res_i)+' '+str(cs)+'\n')
            writeNonAsgRes(pdb_res_idxs,res_i,prev_res,shift_f)


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

    is_a_comment = False
    is_on_data = False

    prev_res_C = first_pdb_res
    prev_res_CA = first_pdb_res
    prev_res_CB = first_pdb_res
    prev_res_H = first_pdb_res
    prev_res_HA = first_pdb_res
    prev_res_N = first_pdb_res

    for line in scr_cshift_file:

        if "#  Assigned chemical shift lists  #" in line:
            is_on_data = True
            continue
        if is_on_data == True:
            #print line
            # skip annotations
            if "_" in list(line) or "'" in line or "#" in line:
                continue
            #skip 'ENTER' lines
            if line.startswith('\n') or line.startswith(";\n"):
                continue
            else:
                line_n = int(line[0:10])
                res_i = int(line[17:21])
                atom = line[30]
                cs = float(line[39:46])
                atom_type = line[29:33].replace(" ","")
            
                ### DEBUG ###
                #print "line_n = ", line_n, "| atom =", atom, " | cs =", cs, " | atom_type = ", atom_type
                #############

                # write plumed files
                if atom_type == 'C':
                    writeSmart(res_i,prev_res_C,Cshift_f)
                    #update previous res
                    prev_res_C = res_i

                if atom_type == 'CA':
                    writeSmart(res_i,prev_res_CA,CAshift_f)
                    #update previous res
                    prev_res_CA = res_i
                    continue

                if atom_type == 'CB':
                    writeSmart(res_i,prev_res_CB,CBshift_f)
                    #update previous res
                    prev_res_CB = res_i
                    continue
                
                if atom_type == 'H':
                    writeSmart(res_i,prev_res_H,Hshift_f)
                    #update previous res
                    prev_res_H = res_i
                    continue
                if atom_type == 'HA':
                    writeSmart(res_i,prev_res_HA,HAshift_f)
                    #update previous res
                    prev_res_HA = res_i
                    continue

                if atom_type == 'N':
                    writeSmart(res_i,prev_res_N,Nshift_f)
                    #update previous res
                    prev_res_N = res_i
                    continue

#####################################################################################

#===| LOAD DATA |===*
try: 
    bmrb_cshift_f = argv[1]
except:
    print "ERROR: you do not specify input file"

pdb_template = open(argv[2], "r")
scr_cshift_file = open(bmrb_cshift_f,'r')

# get pdb atom numbering
pdb_res_idxs=[]

for line in pdb_template:
    if line.startswith("ATOM"):
        atom_n = int(line[5:11])
        pdb_res_idxs.append(atom_n)

first_pdb_res = pdb_res_idxs[0]

writeCShift(scr_cshift_file)

