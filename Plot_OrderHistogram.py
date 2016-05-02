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
	
	home = os.getcwd()
	
	count = []
	
	f=h5py.File('sim.h5','r')
	max_order = len(f['simulation/results/orders/mean/value'])
	order = range(0,max_order)
	for i in order:
		count.append(f['simulation/results/orders/mean/value'][i])
	
	f.close()
		
		
	plt.figure()
	plt.plot(order, count)
	#plt.legend(loc=1)
	plt.xlabel('Order')
	plt.ylabel('Normalized Counts')
	#plt.xlim((-1,-0.4))
	#plt.ylim((0.8,1.1))
	plt.title('Distribution of Diagram Orders')
	matplotlib.rcParams.update({'font.size': 16})
	
	plt.show()	
	
	
if __name__ == "__main__":
	main()
