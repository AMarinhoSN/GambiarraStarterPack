__author__="AMarinhoSN"

'''
'''
import PlumedClasses
#from sys import argv

#1 - write plumed common .dat
DATSetup = PlumedClasses.PlumedSetup("plumed")
DATSetup.write_dat()
