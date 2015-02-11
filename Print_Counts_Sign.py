import h5py

f=h5py.File('sim.h5','r')
print '<sign> = ',f['simulation/results/Sign/mean/value'].value
print 'Counts = ',f['simulation/results/Sign/count'].value

