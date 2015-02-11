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
	
	t=1
	U=4
	methods = ['DCA']
	solver='CTAUX'
	
	params = [(20,12),(20,14),(20,16),(16,12)]
	
	#betas = [20]
	#sites = [12,14,16]
	mus = np.linspace(-1.0,-0.4,num=7)
	
	home = os.getcwd()
	
	for method in methods:		
		postfix = '_1D_'+'CTAUX'+'_dir'	
		os.chdir('Gap_'+method)
		for pa in params:
			beta=pa[0]
			S=pa[1]
			subdir = 'hub_t'+str(t)+'_U'+str(U)+'_B'+str(beta)
			os.chdir(subdir)
			
			postfix = '_1D_'+'CTAUX'+'_dir'
			if(S==2 and beta == 16):
				postfix = '_1D_'+'CTAUX'+'MaxIter10_dir'
			if(S==4 or S==6):
				postfix = '_1D_'+'CTAUX'+'MaxIter20_dir'
			N = []
			params = 'hub_S'+str(S)+'_t'+str(t)+'_U'+str(U)+'_B'+str(beta)
			for mu in mus:
				data_dir = 'hub_S'+str(S)+'_t'+str(t)+'_U'+str(U)+'_u'+str(mu)+'_B'+str(beta)+postfix
				os.chdir(data_dir)
				#average n
				print os.getcwd()
				sim = h5py.File('sim.h5','r')
				n=0
				for i in range(0,S):
					#get hdf5 data
					n += sim['simulation/results/density_down/mean/value'][i]
					n += sim['simulation/results/density_up/mean/value'][i]
				n /= S
				N.append(n)
				os.chdir('..')	
			#print n v mu
			filename = 'hub_S'+str(S)+'_t'+str(t)+'_U'+str(U)+'_B'+str(beta)+'_NvMU.dat'
			f = open(filename, 'w')
			for i in range(0,len(N)):
				f.write(str(mus[i])+'\t'+str(N[i])+'\n')
			f.close()
				
			#plot n v mu
			plt.plot(mus,N,'-^',label=params, linewidth=2)
			os.chdir('..')
		os.chdir(home)
		
	#add Bethe ansatz
	bethe_file = 'Gap_Bethe/hub_t'+str(t)+'_U'+str(U)+'_NvMU_N60.dat'
	f = open(bethe_file,'r')
	mus_bethe_strings = (f.readline()).split()
	mus_bethe = []
	N_bethe_strings = (f.readline()).split()
	N_bethe = []
	
	for mu in mus_bethe_strings:	
		mus_bethe.append(float(mu))
		
	for N in N_bethe_strings:
		N_bethe.append(float(N))
		
	plt.plot(mus_bethe, N_bethe,label='Bethe', linewidth=2)	
	
	#add ED
	Ls=[4,6]
	ED_Bs = [32]
	
	for L in Ls:
		for ED_B in ED_Bs:
			ED_file = 'Gap_ED/hub_S'+str(L)+'_t'+str(t)+'_U'+str(U)+'_B'+str(ED_B)+'_NvMU_1D_ED.dat'
			f=open(ED_file,'r')
			ED_mus=[]
			ED_N=[]
			print ED_file
			for line in f:
				data = line.split()
				ED_mus.append(float(data[0]))
				ED_N.append(float(data[1]))
			f.close()
			labelstring = 'ED L='+str(L)+' B='+str(ED_B)
			#plt.plot(ED_mus, ED_N, label=labelstring, linewidth=2)
	
	plt.legend(loc=2)
	plt.xlabel('$\mu$')
	plt.ylabel('<n>')
	plt.xlim((-1,-0.4))
	plt.ylim((0.8,1.1))
	plt.title('1D Hubbard model, t='+str(t)+', U='+str(U))
	matplotlib.rcParams.update({'font.size': 16})
	plt.show()
		
	
	
	
if __name__ == "__main__":
	main()
