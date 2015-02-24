import numpy as np
import math
import sys
import os
import os.path
import subprocess as sp
import argparse
import json
from pprint import pprint


def main():
	#All paths are relative to home directory
	#home = os.environ['HOME']
	#Remember current location
	curloc = os.getcwd()
	
	#Get the name of the json file containing the parameters
	parser = argparse.ArgumentParser(description='Interpolates the self energy from one temperature and lattice to another')
	parser.add_argument('old_param_folder',help='folder with old parameter file')
	parser.add_argument('new_param_folder',help='folder with new parameter file')
	args = parser.parse_args()
	
	#Change to source folder to clean paramfile
	os.chdir(args.old_param_folder)
	print "Cleaning source paramfile\n"
	command = "python ~/alps_git/DMFT_Scripts/Clean_ALPS_Param.py paramfile paramfile"
	sp.call(command,shell=True)
	os.chdir(curloc)	
	
	#Change to destination folder for new self energy
	os.chdir(args.new_param_folder)
	print os.getcwd()
	print "Cleaning dest paramfile\n"
	command = "python ~/alps_git/DMFT_Scripts/Clean_ALPS_Param.py paramfile paramfile"
	sp.call(command,shell=True)
	
	source_param = curloc+"/"+args.old_param_folder + "/paramfile"
	source_selfenergy = "selfenergy_"
	i=1
	while(os.path.isfile(curloc+"/"+args.old_param_folder+"/"+source_selfenergy+source_selfenergy+str(i))):
		i+=1
	source_selfenergy = curloc+"/"+args.old_param_folder+"/"+source_selfenergy+str(i-1)
	
	print "Interpolating self energy"	
	
	command = "~/alps_git/DMFT/AuxiliaryPrograms/sigma_interpolate --pfile_old "+source_param+" --pfile_new paramfile"+" --selfenergy "+source_selfenergy
	print command
	sp.call(command,shell=True)
	
	
	os.chdir(curloc)
				
				
				
				


if __name__ == "__main__":
	main()
    
			
