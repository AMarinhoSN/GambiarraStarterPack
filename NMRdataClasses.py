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
        list_of_res = range(res_i, res_f)

        # 2 - Create *shift.dat
        print "| @ Writing *shift.dat"
        Cshift_f = open(c_working_dir+"/data/"+'Cshift.dat', 'w')
        CAshift_f = open(c_working_dir+"/data/"+'CAshift.dat', 'w')
        CBshift_f = open(c_working_dir+"/data/"+'CBshift.dat', 'w')
        HAshift_f = open(c_working_dir+"/data/"+'HAshift.dat', 'w')
        Hshift_f = open(c_working_dir+"/data/"+'Hshift.dat', 'w')
        Nshift_f = open(c_working_dir+"/data/"+'Nshift.dat','w')

        first_res = list_of_res[0]
        final_res = list_of_res[-1]

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

        if len(self.data) == 0:
                print "| ERROR: no data stored, you should check the source file."
    
        for cs in self.data:

            #print cs['atom_id']
            #print cs['value']
            #print cs['author_seq_id']
            curr_res = cs['author_seq_id']

            # Check if the cs res is on the system:

            if curr_res < first_res:
                Absent_PDB_res.append(curr_res)
                continue
            if curr_res > final_res:
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