__author__ = "AMarinhoSN"

'''
Define classes of NMR data

'''

class CSdata:
    "Class of Chemical Shift data obtained from a NMR-STAR v3.1"

    def __init__(self, name, source_file_name):
        
        self.name = name
        self.src_file = source_file_name
        self.data = []

    def loadData(self):
        """ Load data on NMR-STAR v3.1 source file """
        #print "|    > Loading CS data from ", self.src_file,"."
        
        try: 
            bmrb_cshift_f = self.src_file
            scr_cshift_file = open(bmrb_cshift_f,'r')
        except(IOError):
            print "ERROR: the ", self.src_file, " was not found"
            exit()
        
        is_on_data = False
        for line in scr_cshift_file:
            
            if "#  Assigned chemical shift lists  #" in line:
                is_on_data = True
                continue
            if is_on_data == True:
            
                # skip annotations
                if "_" in list(line) or "'" in line or "#" in line:
                    continue
            
                #skip 'ENTER' lines
                if line.startswith('\n') or line.startswith(";\n"):
                    continue
            
                else:
                    # get a list of the current values on the line
                    line_split = line.split(' ')
                    line_2 =[]

                    for item in line_split:
                        if item == '' or item == '\n':
                            continue
                        else:
                            line_2.append(item)
                    
                    ### DEBUG ###
                    #print line_2
                    #print len(line_2)
                    #############cshift_file = open(argv[1],"r")
    
                    
                    # get actual atom data and store it on a dict
                    Atom_cs = {
                               'id': int(line_2[0]),
                               'assbly_id':line_2[1],
                               'entd_assbly_id':line_2[2],
                               'entd_id':line_2[3],
                               'comp_idx_id':line_2[4],
                               'seq_id':line_2[5],
                               'comp_id':line_2[6],
                               'atom_id':line_2[7],
                               'atom_type':line_2[8],
                               'atom_isotope_number':line_2[9],
                               'value':float(line_2[10]),
                               'value_error':float(line_2[11]),
                               'assign_fig': line_2[12],
                               'ambiguity_code':line_2[13],
                               'occupancy':line_2[14],
                               'resonance_ID':line_2[15],
                               'author_entitity_id':line_2[16],
                               'author_asym_id':line_2[17],
                               'author_seq_id':int(line_2[18]),
                               'author_comp_id':line_2[19],
                               'author_atom_id':line_2[20],
                               'details':line_2[21],
                               'entry_id':line_2[22],
                               'asgnd_cs_list_id':line_2[23]
                               }
                    
                    ### DEBUG ###
                    #print Atom_cs
                    #############
                    
                    # store on data atribute 
                    self.data.append(Atom_cs)

        print "|        --> ", len(self.data), " chemical shift data found"

if __name__ == "__main__":

    from sys import argv
    from sys import exit
    
    try:
        src_file_nm = argv[1]
    except(IndexError):
        print "ERROR: You should specify an input file."
        exit()
    
    CSDATA = CSdata('cshift',src_file_nm)
    CSDATA.loadData()
    #CSDATA.data[0]['id']