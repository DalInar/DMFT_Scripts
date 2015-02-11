import sys
import os
import subprocess as sp
import argparse

#Reads a DMFT parameter file and rewrites it to include quotes " " around the appropriate fields
def main():
	#Get the names of the input and output parameter files
	parser = argparse.ArgumentParser(description='Reads a DMFT parameter file and rewrites it to include quotes " " around the appropriate fields.')
	parser.add_argument('input_file',help='Name of input parameter file to be cleaned')
	parser.add_argument('output_file',help='Where to put the cleaned version of the parameter file')
	parser.add_argument('-iter',help='Set the current iteration in the new parameter file')
	parser.add_argument('-beta',help='Set a new value of beta in the new parameter file')
	args = parser.parse_args()
		
	in_filename = args.input_file
	out_filename = "paramfile_temp"
	in_param = open(in_filename,'r')
	out_param = open(out_filename,'w')
	
	#Read all of the parameters in the file
	for line in in_param:
		data = line.split('=')
		#Get the name of the parameter
		field = data[0].strip()
		#Get the value of the parameter, and add quotes to certain values if they do not already have quotes
		#Also, change current iteration and beta if needed
		value = data[1].strip()
		if(field == "SOLVER" or field == "LATTICE" or field == "LATTICE_LIBRARY"):
			if(not value[0] == '"'):
				value = '"'+value+'"'
		elif (field == "BETA"):
			if(not args.beta == None):
				value = args.beta
		elif (field == "CURRENT_IT"):
			if(not args.iter == None):
				value = args.iter
		out_param.write(field+' = '+value+'\n')
	
	in_param.close()
	out_param.close()
	#Move the temporary parameter file to the specified destination
	command = "mv paramfile_temp "+args.output_file
	sp.call(command,shell=True)


if __name__ == "__main__":
	main()
