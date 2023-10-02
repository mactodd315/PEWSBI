import matplotlib.pyplot as plt
import numpy as np
import h5py, os

plots_folder = os.path.dirname(__file__)[:-5]+'/plots/'
posteriors_folder = os.path.dirname(__file__)[:-5] +'/posteriors/'

#------------------------- posterior plotting---------------------------------
posteriors = [f for f in os.listdir(posteriors_folder) if f.split('.')[1]=='hdf']

fig, s1 = plt.subplots(1,1)

for each in posteriors:
    with h5py.File(posteriors_folder+each, 'r') as f:
        posterior = f['posteriors'][0,:]
        s1.plot(np.linspace(10,100,len(posterior)),posterior, label = each.split('.')[0])

plt.legend()
plt.savefig(plots_folder+'posterior0.png')

#-----------------------pp-test plotting---------------------------------------
traces = [f for f in os.listdir(plots_folder) if f.split('.')[1]=='hdf']

fig, s1 = plt.subplots(1,1)

for each in traces:
    with h5py.File(plots_folder+each, 'r') as f:
        s1.plot(f['traces'][0],f['traces'][1], label = each.split('.')[0])

plt.legend()
plt.title('TS:1000, OS: 50')
plt.savefig(plots_folder+'pptest.png')