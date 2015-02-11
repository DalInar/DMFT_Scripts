import sys
import os
import math
import numpy as np
from pylab import *
import h5py
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt

def main():
	print "Starting"
	print 'Number of arguments:', len(sys.argv), 'arguments.'
	print 'Argument List:', str(sys.argv)
	t=1
	U=7
	
	if(not len(sys.argv) == 4):
		print "usage: python Plot_SE.py OldSEIteration NewSEIteration NumFreqs"
		return
	
	seold = sys.argv[1]
	senew = sys.argv[2]
	NumFreqs = int(sys.argv[3])
	
	home = os.getcwd()
	
	freqs = []
	SEreal_new = []
	SEreal_old = []
	SEimag_new = []
	SEimag_old = []	
	
	filename = "selfenergy_"+seold
	f = open(filename, 'r')
	
	for i in range(0,NumFreqs):	
		line=f.readline()
		data = line.split()
		freq  = float(data[0])	
		SEreal  = float(data[1])
		SEimag  = float(data[2])
		
		freqs.append(freq)
		SEreal_old.append(SEreal)	
		SEimag_old.append(SEimag)
	
	f.close()
	
	filename = "selfenergy_"+senew
	f = open(filename, 'r')
	
	for i in range(0,NumFreqs):	
		line=f.readline()
		data = line.split()
		SEreal  = float(data[1])
		SEimag  = float(data[2])
		
		SEreal_new.append(SEreal)	
		SEimag_new.append(SEimag)
	
	f.close()
		
		
	plt.figure()
	plt.plot(freqs, SEreal_old, '-^', label=seold)
	plt.plot(freqs, SEreal_new, '-x', label=senew)
	plt.legend(loc=4)
	plt.xlabel('i$\omega_n$')
	plt.ylabel('SE real')
	#plt.xlim((-1,-0.4))
	#plt.ylim((0.8,1.1))
	plt.title('Self Energy Real, t='+str(t)+', U='+str(U))
	matplotlib.rcParams.update({'font.size': 16})
	
	plt.figure()
	plt.plot(freqs, SEimag_old, '-^', label=seold)
	plt.plot(freqs, SEimag_new, '-x', label=senew)
	plt.legend(loc=4)
	plt.xlabel('i$\omega_n$')
	plt.ylabel('SE imag')
	#plt.xlim((-1,-0.4))
	#plt.ylim((0.8,1.1))
	plt.title('Self Energy Imag, t='+str(t)+', U='+str(U))
	matplotlib.rcParams.update({'font.size': 16})
	plt.show()	
	
	
if __name__ == "__main__":
	main()
