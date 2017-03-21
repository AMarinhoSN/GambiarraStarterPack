__author__ = "AMarinhoSN"

'''
Define classes of NMR data

'''
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
c_working_dir = os.getcwd()

class CSdata:
    "Class of Chemical Shift data obtained from a NMR-STAR v3.1"

    def __init__(self, name, source_file_name):
        
        self.name = name
        self.src_file = source_file_name
        self.data = []

    def loadData(self):
        """ Load data on NMR-STAR v3.1 source file """
        #print "|    > Loading CS data from ", self.src_file,"."
        
        #try: 
        bmrb_cshift_f = self.src_file
        scr_cshift_file = open(bmrb_cshift_f,'r')
        
        #except(IOError):
        #    print "ERROR: the ", self.src_file, " was not found"
        #    exit()
        
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
    
    def writeCShiftDAT(self, res_i, res_f):
        ''' 
        Write cshift.dat files based on a NMR-STAR v3.1 file
        '''
        list_of_res = range(res_i, res_f+1)
        #print list_of_res
        #print stop
        # 2 - Create *shift.dat
        print "| @ Writing *shift.dat"
        Cshift_f = open(c_working_dir+"/data/"+'Cshifts.dat', 'w')
        CAshift_f = open(c_working_dir+"/data/"+'CAshifts.dat', 'w')
        CBshift_f = open(c_working_dir+"/data/"+'CBshifts.dat', 'w')
        HAshift_f = open(c_working_dir+"/data/"+'HAshifts.dat', 'w')
        Hshift_f = open(c_working_dir+"/data/"+'Hshifts.dat', 'w')
        Nshift_f = open(c_working_dir+"/data/"+'Nshifts.dat','w')

        first_res = list_of_res[0]
        final_res = list_of_res[-1]

        prev_res_C = first_res
        prev_res_CA = first_res
        prev_res_CB = first_res
        prev_res_H = first_res
        prev_res_HA = first_res
        prev_res_N = first_res
        
        Absent_PDB_res = []

        if len(self.data) == 0:
                print "| ERROR: no data stored, you should check the source file."
    
        C_asgnd_values =[]
        C_asgnd_res =[]
        CA_asgnd_values =[]
        CA_asgnd_res =[]
        CB_asgnd_values =[]
        CB_asgnd_res =[]
        HA_asgnd_values =[]
        HA_asgnd_res =[]
        H_asgnd_values =[]
        H_asgnd_res =[]
        N_asgnd_values =[]
        N_asgnd_res =[]

        # Get individual asingned data

        for idx, cs in enumerate(self.data):

            curr_res = cs['author_seq_id']

            # Check if the cs res is on the system:

            if curr_res < first_res:
                Absent_PDB_res.append(curr_res)
                continue
            if curr_res > final_res:
                Absent_PDB_res.append(curr_res)
                continue
            
            if cs['atom_id'] == "C":
                C_asgnd_values.append(cs['value'])
                C_asgnd_res.append(cs["author_seq_id"])
            if cs['atom_id'] == "CA":
                CA_asgnd_values.append(cs['value'])
                CA_asgnd_res.append(cs["author_seq_id"])
            
            if cs['atom_id'] == "CB":
                CB_asgnd_values.append(cs['value'])
                CB_asgnd_res.append(cs["author_seq_id"])
            
            if cs['atom_id'] == "N":
                N_asgnd_values.append(cs['value'])
                N_asgnd_res.append(cs["author_seq_id"])

            if cs['atom_id'] == "H":
                H_asgnd_values.append(cs['value'])
                H_asgnd_res.append(cs["author_seq_id"])

            if cs['atom_id'] == "HA":
                HA_asgnd_values.append(cs['value'])
                HA_asgnd_res.append(cs["author_seq_id"])

        def smartwrite(list_of_res, cshift_f, asgnd_res, asgnd_values):
            '''
            write CS and non CS residues 
            '''
            
            for res in list_of_res:
                # if non asigned res
                if res not in asgnd_res:
                    cshift_f.write(str(res)+" 0.00\n")
                # if asigned res
                if res in asgnd_res:
                    cs_idx = asgnd_res.index(res)
                    cshift_f.write(str(res)+ " "+str(asgnd_values[cs_idx])+"\n")
        
        # write C data
        
        smartwrite(list_of_res, Cshift_f, C_asgnd_res,C_asgnd_values)
        smartwrite(list_of_res, CAshift_f, CA_asgnd_res, CA_asgnd_values)
        smartwrite(list_of_res, CBshift_f, CB_asgnd_res, CB_asgnd_values)
        smartwrite(list_of_res, Nshift_f, N_asgnd_res, N_asgnd_values) 
        smartwrite(list_of_res, Hshift_f, H_asgnd_res, H_asgnd_values)
        smartwrite(list_of_res, HAshift_f,HA_asgnd_res, HA_asgnd_values)

        # 3 - Warning for absent residues on the PDB

        if len(Absent_PDB_res) > 0:
            print "| WARNING: ", len(Absent_PDB_res), " res have Chemical Shift data asigned but are absent on PDB file"
        # DONE

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