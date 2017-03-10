# -*- coding: utf-8 -*-
'''
 >> Gambiarra Toolkit Starter Pack <<
	Plumed Package

This script was written to fix common problems find on HILLS file processing.
Author: AMarinhoSN
'''

hills_path_in = "/home/antonio/Docbox/E1/NewMetad/18/HILLS_to_fix_2"
f_hills_in = open(hills_path_in,"r")

hills_path_out = "/home/antonio/Docbox/E1/NewMetad/18/HILLS_fixed_2"
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
        
