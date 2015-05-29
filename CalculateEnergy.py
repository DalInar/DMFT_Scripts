import sys
import math
import os
import os.path
import subprocess as sp

def readparams():
	params = {}
	with open("paramfile") as f:			
		for line in f:
			data = line.split()
			params[data[0]] = data[2]			
	return params

def main():
	home = os.getcwd()
	print "Calculating energy in ",home
	
	niteration = 1
	fname = "selfenergy_"+str(niteration)
	while(os.path.isfile(fname) ):
		niteration += 1
		fname = "selfenergy_"+str(niteration)
	niteration -= 1
	
	siteration = max(niteration - 3, 1)
	
	if(niteration == 0):
		print "No data here"
		return
	
	print "niterations = ", niteration
	
	params = readparams()
	
	nfreq = params['N']
	nsite = params['SITES']
	mu = params['MU']
	beta = params['BETA']
	U = params['U']
	t = params['t']
	
	command = "~/alps_git/Energy/energy-joe --niteration "+str(niteration)+" --siteration "+str(siteration)+" --directory . --nfreq "+nfreq+" --nsite "+str(nsite)+" --mu "+str(mu)+" --beta "+str(beta)+" --U "+str(U)+ " > energy.dat"
	
	print "Calculating energy with command:"
	print command	
	sp.call(command,shell=True)


if __name__ == "__main__":
	main()
