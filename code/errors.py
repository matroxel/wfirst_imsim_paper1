import os
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import csv

path = '/fs/scratch/PCON0003/osu10670/wfirst_sim_out/ngmix'
files = os.listdir(path)
shear = []

for file in files:
        print(file)
	hdul = fits.open(path+'/'+file)
	for i in hdul[1].data:
		e1 = i[7]
		e2 = i[8]
		int_e1 = i[9]
		int_e2 = i[10]
                g1 = i[17]
                g2 = i[18]
		shear.append([e1,e2,g1,g2,int_e1,int_e2])

header = ['e1','e2','g1','g2','int_e1','int_e2']
with open('/fs/scratch/PCON0003/osu10670/wfirst_sim_out/error/info.csv','w') as f:
	writer = csv.writer(f, delimiter=',')
	writer.writerow(header)

	for l in shear:
		writer.writerow(l)

e1 = [i[0] for i in shear]
e2 = [i[1] for i in shear]
g1 = [i[2] for i in shear]
g2 = [i[3] for i in shear]

A1 = np.vstack([g1, np.ones(len(g1))]).T
m1, c1 = np.linalg.lstsq(A1, e1, rcond=None)[0]
m1 = m1-1
A2 = np.vstack([g2, np.ones(len(g2))]).T
m2, c2 = np.linalg.lstsq(A2, e2, rcond=None)[0]
m2 = m2-1
print(m1,c1, m2, c2)

plt.plot(g1,(m1+1)*g1+c1)
plt.plot(g2,(m2+1)*g2+c2)
plt.plot(g1,g1)
plt.show()
