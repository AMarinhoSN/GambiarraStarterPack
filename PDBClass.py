__author__="AMarinhoSN"

"""
Classes for common operations with PDB files
NOT FINISHED!!!!
"""
from sys import exit
class PDB:
    '''

    '''
    def __init__(self,name, pdb_file_name):
        
        try:
            self.pdb_file = open(pdb_file_name, "r")
        except(IOError):
            print "ERROR: ", pdb_file_name, " not found."
            exit()
        
        def load_1confData(self):
            '''
            load the general data of the first conformation. Its usefull to get reference
            data for MD simulation common input files writing (ex: template for metadynamics)
            without the need to load the data for other conformations. 

            '''
            for line in self.pdb_file:
                if line.startswith("ATOM"):
                    print line[5:12]
                    res_i = int(line[23:26])
                    res_i_type = line[17:20]
                    print line[23:26]
                    pdb_res_idxs.append(res_i)
                    #print res_i    
                if line.startswith('ENDMDL') or line.startswith('TER'):
                    break
            

