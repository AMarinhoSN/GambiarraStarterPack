__author__="AMarinhoSN"

from NMRdataClasses import CSdata
from sys import argv, exit

print "|-------------------------------------------------------------|"
print "|            >> Gambiarra Toolkit Starter Pack <<             |"
print "|                >> PlumedPrepCSfiles.py <<                   |"
print "|                                                             |"
print "| This script write *shift.dat files based on a NMR-STAR v3.1 |"
print "| file, those *shift.dats are used by Plumed on NMR data inte |"
print "| gration on Molecular Dynamics Protocol.                     |"
print "|-------------------------------------------------------------|"
print "| USAGE: python PlumedPrepCSfiles.py BMRB_file res_i res_n    |"
print "|_____________________________________________________________|"

# 1 - load pdb reference and CS data 

try: 
    cshift_file_name = argv[1]
except(IndexError):
    print "| ERROR: You do not specify the CShift source file"
    exit()
try: 
    start_res = int(argv[2])
    final_res = int(argv[3])
    list_of_res = range(start_res, final_res+1)
except(IndexError):
    print "| ERROR: You do not specify PDB start and/or final residues numbers."
    exit()
except(ValueError):
    print "| ERROR: You do not set start and/or final residues as valid integers"
    exit()

#print list_of_res
print "| @ Loading CS data: "
CSdata = CSdata("src", cshift_file_name)
CSdata.loadData()

# 2 - write *shift.dat
print "| @ Writing *shift.dat"
Cshift_f = open('Cshift.dat', 'w')
CAshift_f = open('CAshift.dat', 'w')
CBshift_f = open('CBshift.dat', 'w')
HAshift_f = open('HAshift.dat', 'w')
Hshift_f = open('Hshift.dat', 'w')
Nshift_f = open('Nshift.dat','w')

first_res = list_of_res[0]

prev_res_C = first_res
prev_res_CA = first_res
prev_res_CB = first_res
prev_res_H = first_res
prev_res_HA = first_res
prev_res_N = first_res

def writeNonAsgnedRes(curr_res, prev_res, Xcshift_file):
    '''
    Write non asigned res on file
    '''
    ### DEBUG ###
    #print curr_res, " | ", prev_res
    #############
    res_gap = range(prev_res, curr_res)

    for res in res_gap:
        Xcshift_file.write(str(res)+" 0.00\n")

Absent_PDB_res = []

for cs in CSdata.data:

    #print cs['atom_id']
    #print cs['value']
    #print cs['author_seq_id']
    curr_res = cs['author_seq_id']

    if curr_res < first_res:
        Absent_PDB_res.append(curr_res)
        continue

    if cs['atom_id'] == "C":
         Cshift_f.write(str(cs['author_seq_id'])+" "+str(cs['value'])+"\n")
         #print cs['author_seq_id']," ",str(cs['value'])
         #get non asigned gap
         if curr_res == prev_res_C+1:
            prev_res_C = curr_res
            continue
         else:
            writeNonAsgnedRes(curr_res, prev_res_C, Cshift_f)
         prev_res_C = curr_res


    if cs['atom_id'] == "CA":
         CAshift_f.write(str(cs['author_seq_id'])+" "+str(cs['value'])+"\n")
         #get non asigned gap
         if curr_res == prev_res_CA+1:
            prev_res_CA = curr_res
            continue
         else:
            writeNonAsgnedRes(curr_res, prev_res_CA, CAshift_f)
         prev_res_CA = curr_res

    if cs['atom_id'] == "CB":
         CBshift_f.write(str(cs['author_seq_id'])+" "+str(cs['value'])+"\n") 
         if curr_res == prev_res_CB+1:
            prev_res_CB = curr_res
            continue
         else:
            writeNonAsgnedRes(curr_res, prev_res_CB, CBshift_f)
         prev_res_CB = curr_res

    if cs['atom_id'] == "H":
         Hshift_f.write(str(cs['author_seq_id'])+" "+str(cs['value'])+"\n")
         if curr_res == prev_res_H+1:
            prev_res_H = curr_res
            continue
         else:
            writeNonAsgnedRes(curr_res, prev_res_H, Hshift_f)
         prev_res_H = curr_res
 
    if cs['atom_id'] == "HA":
         HAshift_f.write(str(cs['author_seq_id'])+" "+str(cs['value'])+"\n")
         if curr_res == prev_res_HA+1:
            prev_res_HA = curr_res
            continue
         else:
            writeNonAsgnedRes(curr_res, prev_res_HA, HAshift_f)
         prev_res_HA = curr_res
 
    if cs['atom_id'] == "N":
         Nshift_f.write(str(cs['author_seq_id'])+" "+str(cs['value'])+"\n")
         if curr_res == prev_res_N+1:
            prev_res_N = curr_res
            continue
         else:
            writeNonAsgnedRes(curr_res, prev_res_N, Nshift_f)
         prev_res_N = curr_res

# 3 - Warning for absent residues on the PDB
if len(Absent_PDB_res) > 0:
    print "| WARNING: ", len(Absent_PDB_res), " res have Chemical Shift data asigned but are absent on PDB file"

print "| :: DONE ::"