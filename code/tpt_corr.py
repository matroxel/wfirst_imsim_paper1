import numpy as np
import fitsio
import os
import treecorr
import matplotlib.pyplot as plt

path = '/fs/scratch/PCON0003/osu10670/wfirst_sim_out/ngmix'
files = os.listdir(path)

ra=np.array([],dtype='>f8')
dec=np.array([],dtype='>f8')
e1=np.array([],dtype='>f8')
e2=np.array([],dtype='>f8')

for file in files:
	ra_tmp = fitsio.read(path+'/'+file,columns='ra')
	dec_tmp = fitsio.read(path+'/'+file,columns='dec')
	e1_tmp = fitsio.read(path+'/'+file,columns='e1')
	e2_tmp = fitsio.read(path+'/'+file,columns='e2')
	ra=np.append(ra,ra_tmp)
	dec=np.append(dec,dec_tmp)
	e1=np.append(e1,e1_tmp)
	e2=np.append(e2,e2_tmp)

cat = treecorr.Catalog(ra=ra, dec=dec, g1=e1, g2=e2,ra_units='deg', dec_units='deg')

gg = treecorr.GGCorrelation(min_sep=0.1, max_sep=400, nbins=20, sep_units='arcmin')
gg.process(cat)

r = np.exp(gg.meanlogr)
xip = gg.xip
xim = gg.xim
sig = np.sqrt(gg.varxip)

ra_min = np.min(cat.ra)
ra_max = np.max(cat.ra)
dec_min = np.min(cat.dec)
dec_max = np.max(cat.dec)
print('ra range = %f .. %f' % (ra_min, ra_max))
print('dec range = %f .. %f' % (dec_min, dec_max))

plt.plot(r, xip, color='blue')
plt.plot(r, -xip, color='blue', ls=':')
plt.errorbar(r[xip>0], xip[xip>0], yerr=sig[xip>0], color='blue', lw=0.1, ls='')
plt.errorbar(r[xip<0], -xip[xip<0], yerr=sig[xip<0], color='blue', lw=0.1, ls='')
lp = plt.errorbar(-r, xip, yerr=sig, color='blue')

plt.plot(r, xim, color='green')
plt.plot(r, -xim, color='green', ls=':')
plt.errorbar(r[xim>0], xim[xim>0], yerr=sig[xim>0], color='green', lw=0.1, ls='')
plt.errorbar(r[xim<0], -xim[xim<0], yerr=sig[xim<0], color='green', lw=0.1, ls='')
lm = plt.errorbar(-r, xim, yerr=sig, color='green')

plt.xscale('log')
plt.yscale('log', nonposy='clip')
plt.xlabel(r'$\theta$ (arcmin)')

plt.legend([lp, lm], [r'$\xi_+(\theta)$', r'$\xi_-(\theta)$'])
plt.xlim( [0.1,200] )
plt.ylabel(r'$\xi_{+,-}$')
plt.savefig("ggcorr")
plt.show()
