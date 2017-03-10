# -*- coding: utf-8 -*-
'''
 >> Gambiarra Toolkit Starter Pack <<
	Plumed Package

A script written to fix unusual characteres "\x0" on HILLS file, probably added by the servants of the Besta Fera (a legendary supernatural entity that haunt PhD students working on theoretical and computational oriented projects report for decades).
USAGE: python FixHillsFile.py 

Author: AMarinhoSN
'''
from sys import argv

hills_path_in = argv[1]
f_hills_in = open(hills_path_in,"r")

hills_path_out = argv[1]+"_fixed"
f_hills_out = open(hills_path_out,"w")

for line in f_hills_in:
    line_data = line.split()
    if len(line_data) != 5:
        #print line
        if len(line_data) == 8:
            #print line_data            
            coment_idx= line.rfind("#")
            new_line = line[coment_idx:-1]            
            f_hills_out.write(new_line+"\n")
            continue            
            
        if line.startswith("#") == False:
            #print line_data
            f_hills_out.write(line.replace("\x00", ""))
        
        else:
            f_hills_out.write(line)
    
    else:
        f_hills_out.write(line)
        
