# GambiarraStarterPack

The GambiarraStarterPack is a collection of scripts designed to solve common problems on daily tasks related to Molecular Biophysics projects find by myself.
I must warning you all that all scripts on this project were designed following the great Gambiarra School of Coding, therefore all scripts are working but sometimes we can't explain how.
Only the initiated on the Gambiarra Honor Code should use it, but feel free to try by yourself.

AMarinhoSN 

Requirements:
	- python2.7

Scripts:

 - PLUMED


	- CSfiles4Plumed.py
		A script to generate the Chemical Shift (CS) files input for NMR-restrained Metadynamics using Gromacs+Plumed based on CS source files on BMRB format.

		USAGE:python CSfiles4Plumed.py sourceBRMBfilename

	- FixHillsFile.py
		A script written to fix unusual characteres "\x0" on HILLS file, probably added by the servants of the Besta Fera (a legendary supernatural entity that haunt PhD students working on theoretical and computational oriented projects report for decades on several countries).

		USAGE: python FixHillsFile.py
	- prep_RMSD_ref.py
		Set the w' and w weight sets on the PDB reference structure.The w' is used for center of mass calculation and is written on OCCUPANCY column (the first collumn after coordinates). The w is used to calculate how far the atoms have been displaced.
		USAGE: python prep_RMSD_ref.py reference.pdb
 
