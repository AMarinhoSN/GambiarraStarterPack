__author__="AMarinho"
import PDBClass
import os
import NMRdataClasses

script_dir = os.path.dirname(os.path.realpath(__file__))
c_working_dir = os.getcwd()

#---| List of implemented options |---#
NMRdata_opt_list = ['CS']
sim_opt_list =['NMR-REMetaD (CS)']
cvs_opt = ['CS']
#-------------------------------------#        

#---| DEFINE CLASSES |---#
# TODO add a decent comment

class CV:
    ''' '''
    def __init__(self, name, type):
        self.name = name 
        #self.protein = PDBobj
        self.type = type # the cv kind (ex: Chemical Shift, Angle)

    def writeCSasCV(self, dat_file, atoms_i, atoms_f, data_dir_nm):
        '''
        write chemical shift as a cv on your .dat input file 
        dat_file = the file to be written on.

        '''
        # 1 - copy camshift.db to data dir
        os.system('mkdir ./data')
        os.system('cp '+script_dir+'/plumed_in_db/camshift.db '+c_working_dir+'/data/camshift.db')
        # 2 - Check file on data 
        # TODO : escrever uma funcao para isso
        files_on_data_dir = [f for f in os.listdir(c_working_dir+"/data/") if os.path.isfile(os.path.join(c_working_dir+"/data/", f))]
        there_is_cshifdat = False
        cshift_files = []
        print "| Checking for cshift data files..."
        for each in files_on_data_dir:
            if "shift.dat" in each:
                there_is_cshifdat = True
                cshift_files.append(each)
                break
            else:
                continue

        if there_is_cshifdat == True:
            print "| There are the following cshift.dat files on data dir: "
            print "| ", (f+" " for f in cshift_files)
            print "| Assuming that those are all the files you need. "

        # write cshift.dat files?

        if there_is_cshifdat == False:
            print "| No cshift.dat files were found on data dir: "
            print "| Do you want to write it now? (yes / no) "
            valid_entry = False

            while valid_entry == False:
                
                want_cshift_answ = raw_input("| :")
                want_cshift = False

                # Yes, please, noble man.

                if want_cshift_answ == '' or want_cshift_answ == "yes" or want_cshift_answ == "y":
                    want_cshift = True
                    valid_entry = True

                    # Would kindly give me a BMRB file format?
                    print "| Be sure that the BMRB is on the current working directory" 
                    print "| and is valid NMR-START v3.1 file."
                    print "| What is the BMRB filename? "
                    valid_name = False
                    while valid_name == False:
                        #try:

                        bmrb_file = raw_input("| : ")
                        CSobj = NMRdataClasses.CSdata("CSdata", bmrb_file)
                        CSobj.loadData()
                        valid_name = True

                        #except(IOError):
                           #print "| !! ERROR: the ", bmrb_file, " was not found. Try again."

                    print "| What is the first residue on your PDB? "
                    # TODO : write a function to do this kind of thing
                    valid_entry = False
                    while valid_entry == False:
                        try:
                            res_i = int(raw_input("| "))
                            valid_entry = True

                        except(TypeError):
                            print "| ERROR: not a valid integer. Try again, looser."
                    print "| What is the final residue on PDB? "
                    valid_entry = False
                    while valid_entry == False:
                        try:
                            res_f = int(raw_input("| "))
                            valid_entry = True
                            
                        except(TypeError):
                            print "| ERROR: not a valid integer. Try again, looser."
                    CSobj.writeCShiftDAT(res_i,res_f)
                    continue
                # aaaaaaaahh, no.
                
                if want_cshift_answ == 'no' or want_cshift_answ == "n":
                    valid_entry = True
                    continue
                # abargungabanda dnaweret viure**&D.
                
                else:
                    print "| Not a valid answer, are you kiding me? Try again."
                    continue

        # 2 - define de CV on your .dat
        #TODO: - set default mode
        #      - set non-default mode
        dat_file.write("### SET CS as CV ###\n")
        dat_file.write("prot: GROUP ATOMS="+str(atoms_i)+"-"+str(atoms_f)+"\n")
        dat_file.write(self.name+": CS2BACKBONE ATOMS=prot DATA="+data_dir_nm+" NRES="+str(atoms_f-atoms_i)+" CAMSHIFT\n")
        dat_file.write("PRINT ARG="+self.name+" FILE="+self.name+" STRIDE=10\n") #Should add the stride option
        dat_file.write("####################\n")

class Simulation:
    def __init__(self, type):
        ''' '''
        self.type = type

    def writeCS_REMD_on_dat(self, dat_file,CVobj):
        ''' '''
        print "| ! WARNING: The slope is set to 0, you should check if this is the optimal value for your system."
        print "| !          What? How can you do that? Don't worry i got you covered:"
        print "| !                1 - set a given value (ex: 1) and run the simulation"
        print "| !                2 - if simulation go without crash, increase the slope value"
        print "| !                3 - if simulation crash, use the previous slope value, else, do from 2 again" 
        print "| !                   "
        dat_file.write("### DEFINE CHEMICAL SHIFT REPLICA EXCHANGE METADYNAMICS ###\n")
        dat_file.write("enscs: ENSEMBLE ARG=("+CVobj.name+"\.hn_.*),("+CVobj.name+"\.nh_.*),("+CVobj.name+"\.ca_.*),("+CVobj.name+"\.cb_.*),("+CVobj.name+"\.co_.*),("+CVobj.name+"\.ha_.*)\n")
        dat_file.write("stcs: STATS ARG=enscs.* SQDEVSUM PARARG=("+CVobj.name+"\.exphn_.*),("+CVobj.name+"\.expnh_.*),("+CVobj.name+"\.expca_.*),("+CVobj.name+"\.expcb_.*),("+CVobj.name+"\.expco_.*),("+CVobj.name+"\.expha_.*)\n")
        dat_file.write("res: RESTRAINT ARG=stcs.sqdevsum AT=0. KAPPA=0. SLOPE=0\n")
        dat_file.write("PRINT ARG=("+CVobj.name+"\.hn_.*),("+CVobj.name+"\.nh_.*),("+CVobj.name+"\.ca_.*),("+CVobj.name+"\.cb_.*),("+CVobj.name+"\.co_.*),("+CVobj.name+"\.ha_.*) FILE=CS STRIDE=1000\n")
        dat_file.write("PRINT ARG=res.bias FILE=COLVAR STRIDE=10\n")
        dat_file.write("###########################################################\n")

class PlumedSetup:
    ''' '''
    def __init__(self, datName):
        print "|---| Seting up ", datName,".dat file |---|"
        print "| "
        
        self.dat_file_nm = datName
        # 1 - Create .dat file
        self.dat_file = open(self.dat_file_nm+'.dat','a+')

        self.cvs = [] # A list of CV objects
    
    def write_dat(self):
        '''        '''
        
        # 2 - Define Collective Variables (CV)

        cv_setup_has_finished = False
        print "|---| SYSTEM SETUP |---|"
        print "| "
        print "|---| ATOMS GROUPS |"
        print "| Do you want to setup groups of atoms? "
        print "| : NOT IMPLEMENTED, SO YOU DON'T"
        print "|---| CV SETUP |"

        while cv_setup_has_finished == False:
            
            # 2.1 - Choose CV

            print '| Please choose a CV type:'
            print '| 0 - Chemical Shift'
            cv_idx = int(raw_input('| : '))
            cv_type = cvs_opt[cv_idx]
            print '| Give a name to the CV: '
            cv_name = raw_input('| : ')
            
            # 2.2 - Get the CV type and procced accordingly

            if cv_type == 'CS':
                
                print "| Set the number of first atom on PDB: "
                non_int = True

                # 2.1.1 - Get the fisrt and last residue on PDB

                while non_int == True:
                    try:
                        atom_i = int(raw_input("| : "))
                        print "| Set the number of final atom on PDB: "
                        atom_f = int(raw_input("| : "))
                        non_int = False

                    except(TypeError):
                        print "| ERROR: non integer value. "
                        print "| Try again, you can do it!"

                # 2.1.2 - Write on .dat

                CS = CV(cv_name, cv_type) 
                CS.writeCSasCV(self.dat_file, atom_i, atom_f, "data")
                self.cvs.append(CS)

            # 3 - More CVs?

            print '| Do you want to setup another CV? (yes/no)'
            want_to_continue = raw_input("| : ")

            # 3.1 - No, but thanks for asking S2            

            if want_to_continue == 'no' or want_to_continue=="n":
                cv_setup_has_finished = True

            # 3.1 - Yes, please.

            if want_to_continue == "yes" or want_to_continue=="y":
                continue
        
        # 4 - Setup Molecular Dynamics protocol

 
        print "|---| SIMULATION SETUP |---|"
        
        # 4.1 - What do you want to do?

        print "| For what kind of simulation you want to use Plumed? "
        self.dat_file.write("### MD SETUP ###\n")
        for idx, each in enumerate(sim_opt_list):
            print '| ', idx, ' - ', each
        sim_idx = int(raw_input('| : '))
        profile_chosen = sim_opt_list[sim_idx]
        
        # 4.1 - Get the simulation type and act accordingly

        if profile_chosen == 'NMR-REMetaD (CS)': 
            print "| What is the NMR data you will use? "
            for idx, each in enumerate(NMRdata_opt_list):
                print '| ', idx, ' - ', each
            is_a_valid_entry= False

            while is_a_valid_entry==False:
                try: 
                    NMRdata_idx = int(raw_input('| : '))
                    NMRdata_chosen = sim_opt_list[NMRdata_idx]
                    is_a_valid_entry = True
                except(IndexError):
                    print "|   ERROR: ", NMRdata_idx," is not a valid index"
            
            # 4.1.1 - Check for CS on defined CVs:

            if NMRdata_chosen == 'NMR-REMetaD (CS)':
                print "| The following CVs were defined: "
                have_defined_CS = False

                for idx, each in enumerate(self.cvs):
                    print"| ", idx, " - ", each.name
                    if each.type == "CS":
                        have_defined_CS = True
                        CS_idx = idx

                if have_defined_CS ==True:
                    print "| The ", self.cvs[CS_idx], " is a Chemical Shift CV will use it"
                else:
                    print "| ! WARNING: You need to define Chemical Shift as a Collective Variable First "
                    # TODO : - Back to CV definition
                    exit()
                
                cs_cv = self.cvs[CS_idx]
                CS_METAD = Simulation(profile_chosen)
                CS_METAD.writeCS_REMD_on_dat(self.dat_file, cs_cv)

        print "| :: DONE :: |"