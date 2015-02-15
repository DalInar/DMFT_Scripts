import numpy as np
import os
import subprocess as sp
import math


def main():
	t=1
	U=4

	S_source = 10
	B_source = 16
	
	S_dests = [12]
	B_dests = [16]
	
	dirsuffix = "_1D_CTAUX_dir"
	
	home = os.getcwd()
	source_dir = home+"/hub_t"+str(t)+"_U"+str(U)+"_B"+str(B_source)+"/"
	print "Interpolating self energy"
	for S in S_dests:
		for B in B_dests:
			for mu in np.linspace(-1,-0.4,7):
				source_sub_dir = source_dir + "hub_S"+str(S_source)+"_t"+str(t)+"_U"+str(U)+"_u"+str(mu)+"_B"+str(B_source)+dirsuffix
				source_param = source_sub_dir+"/paramfile"
				source_se = source_sub_dir+"/selfenergy_10"
				dest_dir = "hub_t"+str(t)+"_U"+str(U)+"_B"+str(B)+"/"
				dest_sub_dir = dest_dir + "hub_S"+str(S)+"_t"+str(t)+"_U"+str(U)+"_u"+str(mu)+"_B"+str(B)+dirsuffix
				os.chdir(dest_sub_dir)
				print os.getcwd()
				command = "~/alps_git/DMFT/AuxiliaryPrograms/sigma_interpolate --pfile_old "+source_param+" --pfile_new paramfile"+" --selfenergy "+source_se
				print command
				sp.call(command,shell=True)
				os.chdir(home)
				
				
				
				


if __name__ == "__main__":
	main()
    
			
