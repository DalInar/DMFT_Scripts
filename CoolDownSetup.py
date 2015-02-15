import sys
import os
import subprocess as sp
import argparse
import json
from pprint import pprint

#Sets up calculations to cool down a system through a series of temperatures
#Creates a folder with a parameter file for each temperature
#Creates a batch file that will go into each folder in order, run the job, and interpolate the results for the next temperature

def main():
	#All paths are relative to home directory
	home = os.environ['HOME']
	#Remember current location
	curloc = os.getcwd()
	
	#Get the name of the json file containing the parameters
	parser = argparse.ArgumentParser(description='Creates a batch file and parameter files that will perform a series of calculations on a system as progessively lower temperatures.')
	parser.add_argument('input_file',help='JSON file containing the parameters')
	args = parser.parse_args()		
	
	#Open and read the json file
	in_filename = args.input_file
	print 'Reading parameter file: ',in_filename
	json_data = open(in_filename)
	params = json.load(json_data)	
	json_data.close()
	
	#Get all the different parameters
	ind_params = params["independent parameters"]
	phys_const_params = params["physics constant parameters"]
	sim_const_params = params["simulation constant parameters"]
	phys_var_params = params["physics variable parameters"]
	sim_var_params = params["simulation variable parameters"]
	interp_params = params["interpolation parameters"]
	
	#Save the keys for the variable parameters
	ind_keys = ind_params.keys()
	phys_var_keys = phys_var_params.keys()
	sim_var_keys = sim_var_params.keys()
	
	if(len(phys_var_keys) == 0 and len(sim_var_keys) == 0):
		NumJobs = 1
	elif(not len(phys_var_keys) == 0):
		NumJobs = len(phys_var_params[phys_var_keys[0]])
	else:
		NumJobs = len(sim_var_params[sim_var_keys[0]])	
		
	#Find out how many independent parameter sets there are
	NumIndParams = 1
	for i in ind_keys:
		NumIndParams *= len(ind_params[i])
		
	if("MAX_IT" in sim_const_params.keys()):
		Max_It = [sim_const_params["MAX_IT"]]
	else:
		Max_It = sim_var_params["MAX_IT"]	
		
	if("MAX_TIME" in sim_const_params.keys()):
		Max_Time = [sim_const_params["MAX_TIME"]]
	else:
		Max_Time = sim_var_params["MAX_TIME"]	
		
	if(len(Max_Time)==1):
		Max_Time *= NumJobs
	if(len(Max_It)==1):
		Max_It *= NumJobs
	
	#Estimate the total amount of time to run all jobs
	TotalTime = 0
	for i in range(0,NumJobs):
		TotalTime += Max_It[i]*Max_Time[i]
	
	#Echo the parameters that were read
	if(not NumIndParams ==0):
		print 'Acquired the following independent parameters:'
		for i in ind_keys:
			print i,': ',ind_params[i]
		
	print 'Acquired the following constant physics parameters:'
	for i in phys_const_params.keys():
		print i,': ',phys_const_params[i]
	print 'Acquired the following variable physics parameters:'
	for i in phys_var_keys:
		print i,': ',phys_var_params[i]
	
	print 'Acquired the following simulation parameters:'
	print 'Number of Jobs: ',NumJobs
	print 'Maximum Iterations per Job: ',Max_It
	print 'Maximum Time per Iteration (s): ', Max_Time
	print 'Total Time per Series (h): ', TotalTime/3600.0
	print 'Total Time for all Series (h): ', NumIndParams*TotalTime/3600.0	
	print 
	
	#Create a directory for each set of independent parameters
	indep_dirs = ["hub"]
	for field in ind_keys:
		old_len = len(indep_dirs)
		for k in range(0,len(indep_dirs)):
			for param in ind_params[field]:
				indep_dirs.append(str(indep_dirs[k]+"_"+field+'_'+str(param)))
		del indep_dirs[0:old_len]
	#print indep_dirs
	#print indep_dirs[0].split('_')
	
	for indep_dir in indep_dirs:
		command = "mkdir -p ./"+indep_dir
		sp.call(command,shell=True)
		temp = indep_dir.split('_')
		del temp[0]
		independent_parameters = {}
		#Get the current independent parameters from the directory name and save them in a dictionary
		for k in range(0,len(temp),2):
			independent_parameters[temp[k]] = temp[k+1]
		print independent_parameters
		
		#Create a directory and parameter file for each job
		for i in range(0,NumJobs):
			dirname = indep_dir+"/"+indep_dir
			for field in phys_var_keys:
				dirname = str(dirname +"_"+field+"_"+str(phys_var_params[field][i]))
			for field in sim_var_keys:
				dirname = str(dirname+"_"+field+"_"+str(sim_var_params[field][i]))
			print dirname
			
			print 'Creating directory: ',dirname
			command = 'mkdir -p ./'+dirname
			sp.call(command,shell=True)
			paramfile = dirname+"/paramfile"
			output = open(paramfile,'w')
			
			for field in independent_parameters.keys():
				output.write(field + " = " + str(independent_parameters[field])+'\n')
			
			for field in phys_const_params.keys():
				output.write(field + " = " + str(phys_const_params[field])+'\n')
				
			for field in phys_var_params.keys():
				output.write(field + " = " + str(phys_var_params[field][i])+'\n')
				
			for field in sim_const_params.keys():
				output.write(field + " = " + str(sim_const_params[field])+'\n')			
	
			for field in sim_var_params.keys():
				output.write(field + " = " + str(sim_var_params[field][i])+'\n')			
		
			
		
			output.close()
		
	
	


	
if __name__ == "__main__":
	main()
