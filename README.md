# GambiarraStarterPack

The GambiarraStarterPack is a collection of scripts designed to solve common problems on daily tasks related to biomolecular physics projects that I am working on.
If you find anything that could be usefull for your own selfish desires, feel free to use any script here.
I must warning you all that all scripts on this project were designed following the great Gambiarra School of Coding, therefore all scripts are working but sometimes they don't and we can't explain how. Sometimes they work and we also can't explain how. Only the initiated on the Gambiarra Honor Code should use it, but feel free to try by yourself.

Author: AMarinhoSN 

Requirements:
	- Python2.7

Scripts:

 - PLUMED

	- PlumedPrepCSfiles.py : Generate the Chemical Shift (CS) files input based on CS source files on BMRB format. Those files are used for NMR-restrained Metadynamics using Gromacs+Plumed
		
		USAGE:python PlumedPrepCSfiles.py sourceBRMBfilename res_start res_final
		
		TO DO: Use the actual PDB file to get correspondence of CS and simulated system. 

	- FixHillsFile.py: Fix unusual characteres "\x0" on HILLS file, probably added by the servants of the Besta Fera (a legendary supernatural entity that haunt PhD students working on theoretical and computational oriented projects, there are decades of reports on this subject all around the world).

		USAGE: python FixHillsFile.py
		
	- prep_RMSD_ref.py: Set the w' and w weight sets on the PDB reference structure.The w' is used for center of mass calculation and is written on OCCUPANCY column (the first collumn after coordinates). The w is used to calculate how far the atoms have been displaced.
		
		USAGE: python prep_RMSD_ref.py reference.pdb
 
