import sys, os
import fitsio as fio
import numpy as np
import treecorr
import matplotlib
from astropy.io import fits
import pickle
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import healpy as hp

class field_methods:

	def __init__(self, sca, scax, scay):
		self.sca = sca
		self.scax=scax
		self.scay=scay
		self.sca_centers = {
		'SCA1':[-21.94, 13.12], 
		'SCA2':[-22.09, -31,77], 
		'SCA3':[-22.24, -81.15], 
		'SCA4':[-65.82, 23.76], 
		'SCA5':[-66.32, -20.77], 
		'SCA6':[-66.82, -70.15], 
		'SCA7':[-109.70, 44.12], 
		'SCA8':[-110.46, 0.24], 
		'SCA9':[-111.56, -49.15], 
		'SCA10':[21.94, 13.12], 
		'SCA11':[22.09, -31.77],
		'SCA12':[22.24, -81.15],
		'SCA13':[65.82, 23.76],
		'SCA14':[66.32, -20.77],
		'SCA15':[66.82, -70.15],
		'SCA16':[109.70, 44.12],
		'SCA17':[110.46, 0.24],
		'SCA18':[111.56, -49.15]}

		self.scaid=['SCA1','SCA2','SCA3','SCA4','SCA5','SCA6','SCA7','SCA8','SCA9','SCA10','SCA11','SCA12','SCA13','SCA14','SCA15','SCA16','SCA17','SCA18']
		self.sca_length_x=4096.*10.e-6*1000.
		self.sca_length_y=4096.*10.e-6*1000.

	def sca_centres(self):		
		centrex=[]
		centrey=[]

		for i,x in enumerate(self.scaid):
			centrex=np.append(centrex,self.sca_centers.get(x,None)[0])
			centrey=np.append(centrey,self.sca_centers.get(x,None)[1])

		return np.vstack((centrex,centrey)).T

	def sca_corners(self):

		centre=np.zeros((18,4,2))

		for i,x in enumerate(self.scaid):
			c=self.sca_centers.get(x,None)
			centre[i-1][0][0]=c[0]-self.sca_length_x/2. # lower left
			centre[i-1][1][0]=c[0]-self.sca_length_x/2. # lower right
			centre[i-1][3][0]=c[0]+self.sca_length_x/2. # upper left
			centre[i-1][2][0]=c[0]+self.sca_length_x/2. # upper right
			centre[i-1][0][1]=c[1]-self.sca_length_y/2.
			centre[i-1][1][1]=c[1]+self.sca_length_y/2.
			centre[i-1][3][1]=c[1]-self.sca_length_y/2.
			centre[i-1][2][1]=c[1]+self.sca_length_y/2.
		return centre

	def sca_to_field(self,sca,scax,scay):
 	    centre=self.sca_centres()
 	    centrex=(centre[:,0])[[sca-1]]
 	    centrey=(centre[:,1])[[sca-1]]
 	    return scax*10e-6*1000+centrex, scay*10e-6*1000+centrey

	def get_field_pos(self):
		x, y = self.sca_to_field(self.sca,self.scax,self.scay)
		return x, y

	# def fid(self):
	# 	shape = fio.FITS('/fs/scratch/cond0083/fiducial_H158_final.fits.gz')[-1].read()
	# 	shape = shape[(shape['ra']>0)&(shape['flags']==0)]

	# 	index = self.index[np.in1d(self.index['ind'],shape['ind'],assume_unique=False)]
		

	# 	u,i,c = np.unique(index['ind'],return_counts=True,return_index=True)
	# 	shape_index = fid_shape[np.repeat(np.arange(len(fid_shape)),c)]
		
	# 	self.fid_e1=fid_shape['e1']
	# 	self.fid_e2=fid_shape['e2']
	# 	self.fid_field_e1=fid_shape_index['e1']
	# 	self.fid_field_e2=fid_shape_index['e2']
	# 	with open('corr_fid.cPickle','wb') as f:
	# 		pickle.dump(np.vstack((self.x,self.y,self.fid_e1,self.fid_e2,self.fid_field_e1,self.fid_field_e2)),f)
	# 	print('done fiducial')

class corr_func:

	def __init__(self,psf_name):

		index=fio.FITS('/fs/scratch/cond0083/wfirst_sim_fiducial/truth/fiducial_H158_index_sorted.fits.gz')[-1].read()
		self.index=index[index['dither']>-1]
		self.psf_name=psf_name

	def psf_shape(self):

		print(self.psf_name)

		fid_shape0 = fio.FITS('/fs/scratch/cond0083/fiducial_H158_final.fits.gz')[-1].read(columns=['ind','flags','ra','dec','e1','e2'])
		shape0 = fio.FITS('/fs/scratch/cond0083/'+self.psf_name+'_H158_final.fits.gz')[-1].read(columns=['ind','flags','ra','dec','e1','e2'])
		shape = shape0[(shape0['ra']>0)&(shape0['flags']==0)&(fid_shape0['ra']>0)&(fid_shape0['flags']==0)]
		fid_shape = fid_shape0[(shape0['ra']>0)&(shape0['flags']==0)&(fid_shape0['ra']>0)&(fid_shape0['flags']==0)]
		index = self.index[np.in1d(self.index['ind'],shape['ind'],assume_unique=False)]
	
		u,i,c = np.unique(index['ind'],return_counts=True,return_index=True)
		fid_shape_index = fid_shape[np.repeat(np.arange(len(fid_shape)),c)]
		shape_index = shape[np.repeat(np.arange(len(shape)),c)]


		self.hpind=hp.ang2pix(512,shape['ra'],shape['dec'],nest=True,lonlat=True)
		self.xy_hpind = self.hpind[np.repeat(np.arange(len(self.hpind)),c)]


		sort=self.hpind.argsort()
		self.hpind=self.hpind[sort]
		shape=shape[sort]
		fid_shape=fid_shape[sort]

		self.ind,self.count = np.unique(self.hpind,return_counts=True)
		self.xy_ind,self.xy_count = np.unique(self.xy_hpind,return_counts=True)

		fid_e1 = fid_shape['e1']
		fid_e2 = fid_shape['e2']

		self.ra=shape['ra']
		self.dec=shape['dec']
		e1=shape['e1']
		e2=shape['e2']

		self.delta_e1=e1-fid_e1
		self.delta_e2=e2-fid_e2

		fid_field_e1=fid_shape_index['e1']
		fid_field_e2=fid_shape_index['e2']
		field_e1=shape_index['e1']
		field_e2=shape_index['e2']

		self.delta_field_e1=field_e1-fid_field_e1
		self.delta_field_e2=field_e2-fid_field_e2

		sca_x=index['x']
		sca_y=index['y']
		sca=index['sca']
		field_x=[]
		field_y=[]

		# for i in range(len(sca)):
		# 	if (i%500000==0):
		# 		print(i)
		# 	sca_to_field=field_methods(sca[i],sca_x[i],sca_y[i])
		# 	x, y = sca_to_field.get_field_pos()
		# 	field_x.append(x[0])
		# 	field_y.append(y[0])

		# self.x=np.array(field_x)
		# self.y=np.array(field_y)

	def xy_corr(self):
		cat = treecorr.Catalog(x=self.x, y=self.y, g1=self.delta_field_e1, g2=self.delta_field_e2)
		gg = treecorr.GGCorrelation(min_sep=0.1, max_sep=200, nbins=20)
		gg.process(cat)
		self.jackknife_std('plane')
		self.corr_plot(gg,'plane')

	def sky_corr(self):
		cat = treecorr.Catalog(ra=self.ra, dec=self.dec, g1=self.delta_e1, g2=self.delta_e2,ra_units='deg',dec_units='deg')
		gg = treecorr.GGCorrelation(min_sep=1, max_sep=400, nbins=20, sep_units='arcmin')
		gg.process(cat)
		self.jackknife_std('sky')
		self.corr_plot(gg,'sky')

	def jackknife_std(self,type):
		obj_num=0
		min_ind=0
		subsmp_num=1
		varxip=[]
		varxim=[]
		if type=='plane':
			for i in range(self.xy_ind.shape[0]):
				if obj_num<(len(self.xy_hpind)/1050.):
					obj_num+=self.xy_count[i]
					continue
				# bool=~np.in1d(self.xy_hpind,self.xy_ind[min_ind:i])
				# print('min_ind='+str(min_ind)+',i='+str(i))
				min_ind=i+1
				subsmp_num+=1
				cat = treecorr.Catalog(x=self.x[bool], y=self.y[bool], g1=self.delta_field_e1[bool], g2=self.delta_field_e2[bool])
				gg = treecorr.GGCorrelation(min_sep=0.1, max_sep=200, nbins=20)
				gg.process(cat)
				varxip.append(gg.xip)
				varxim.append(gg.xim)
				min_ind=min_ind+obj_num
				obj_num=0
				subsmp_num+=1

		elif type=='sky':
			for i in range(self.ind.shape[0]):
				if obj_num<(len(self.hpind)/150.):
					obj_num+=self.count[i]
					continue
				# print(i)
				# bool=~np.in1d(self.hpind,self.ind[min_ind:i])
				# print('min_ind='+str(min_ind)+',i='+str(i))
				cat = treecorr.Catalog(ra=self.ra[min_ind:min_ind+obj_num-1], dec=self.dec[min_ind:min_ind+obj_num-1], g1=self.delta_e1[min_ind:min_ind+obj_num-1], g2=self.delta_e2[min_ind:min_ind+obj_num-1],ra_units='deg',dec_units='deg')
				gg = treecorr.GGCorrelation(min_sep=1, max_sep=400, nbins=20, sep_units='arcmin')
				gg.process(cat)
				varxip.append(gg.xip)
				varxim.append(gg.xim)
				min_ind=min_ind+obj_num
				obj_num=0
				subsmp_num+=1


		if type=="plane":
			# bool=~np.in1d(self.xy_hpind,self.xy_ind[min_ind:])
			cat = treecorr.Catalog(x=self.x[bool], y=self.y[bool], g1=self.delta_field_e1[bool], g2=self.delta_field_e2[bool])
			gg = treecorr.GGCorrelation(min_sep=0.1, max_sep=200, nbins=20)
			gg.process(cat)
		elif type=='sky':
			# bool=~np.in1d(self.hpind,self.ind[min_ind:])
			cat = treecorr.Catalog(ra=self.ra[min_ind:], dec=self.dec[min_ind:], g1=self.delta_e1[min_ind:], g2=self.delta_e2[min_ind:],ra_units='deg',dec_units='deg')
			gg = treecorr.GGCorrelation(min_sep=1, max_sep=400, nbins=20, sep_units='arcmin')
			gg.process(cat)
		# boolist.append(bool)
		# ra.append(self.ra[bool])
		# dec.append(self.dec[bool])
		# delta_e1.append(self.delta_e1[bool])
		# delta_e2.append(self.delta_e2[bool])

		# print('done split area')
		# with open('/users/PCON0003/osu10670/wfirst_imsim/corr_figures/corr_variance_'+self.psf_name+'.cPickle','wb') as f:
		# 	pickle.dump(boolist,f)

		# print('done saving data')

		# with open('/users/PCON0003/osu10670/wfirst_imsim/corr_figures/corr_variance_'+self.psf_name+'.cPickle','rb') as f:
		# 	boolist=pickle.load(f)
		# print('done loading data')

		# for i in range(len(boolist)):
		# 	print(i)
		# 	cat = treecorr.Catalog(ra=self.ra[boolist[i]], dec=self.dec[boolist[i]], g1=self.delta_e1[boolist[i]], g2=self.delta_e2[boolist[i]],ra_units='deg',dec_units='deg')
		# 	gg = treecorr.GGCorrelation(min_sep=1, max_sep=400, nbins=20, sep_units='arcmin')
		# 	gg.process(cat)


		varxip.append(gg.xip)
		varxim.append(gg.xim)


		print(len(varxip),len(varxip[0]))
		self.varxip=sum((varxip-np.mean(varxip,axis=0))**2)*(len(varxip)-1)/len(varxip)
		self.varxim=sum((varxim-np.mean(varxim,axis=0))**2)*(len(varxim)-1)/len(varxim)

	def corr_plot(self,gg,type):
		r = np.exp(gg.meanlogr)
		xip = gg.xip
		xim = gg.xim

		sig_p = np.sqrt(gg.varxip+self.varxip)
		sig_m = np.sqrt(gg.varxim+self.varxim)
		# plt.plot(r, xip, color='blue','o')
		# plt.plot(r, -xip, color='blue', 'x')
		plt.errorbar(r[xip>0], xip[xip>0], yerr=sig_p[xip>0], linewidth=2,color='blue', fmt='o')
		plt.errorbar(r[xip<0], -xip[xip<0], yerr=sig_p[xip<0], linewidth=2, color='blue', fmt='x')
		lp = plt.errorbar(-r, xip, yerr=sig_p, color='blue')
		# plt.plot(r, xim, color='green','o')
		# plt.plot(r, -xim, color='green', 'x')
		plt.errorbar(r[xim>0], xim[xim>0], yerr=sig_m[xim>0], linewidth=1, color='red', fmt='o')
		plt.errorbar(r[xim<0], -xim[xim<0], yerr=sig_m[xim<0], linewidth=1, color='red', fmt='x')
		lm = plt.errorbar(-r, xim, yerr=sig_m, color='red')
		plt.xscale('log')
		plt.yscale('log', nonposy='clip')
		if type=='sky':
			plt.xlabel(r'$\theta$(arcmin)')
			plt.title(self.psf_name+'sky delta_e')
			plt.legend([lp, lm], [r'$\xi_+(\theta)$', r'$\xi_-(\theta)$'])
		elif type=='plane':
			plt.xlabel(r'$d$(mm)')
			plt.title(self.psf_name+' focal plane delta_e')
			plt.legend([lp, lm], [r'$\xi_+(d)$', r'$\xi_-(d)$'])
		plt.xlim( [1,200] )
		plt.ylabel(r'$\xi_{+,-}$')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/corr_figures/'+self.psf_name+'_corr_'+type)

	def save_data(self):
		# with open('/users/PCON0003/osu10670/wfirst_imsim/corr_figures/corr_sky_'+self.psf_name+'.cPickle','wb') as f:
		# 	pickle.dump((self.ra,self.dec,self.delta_e1,self.delta_e2),f)

		# with open('/users/PCON0003/osu10670/wfirst_imsim/corr_figures/corr_field_'+self.psf_name+'.cPickle','wb') as f2:
		# 	pickle.dump((self.x,self.y,self.delta_field_e1,self.delta_field_e2),f2)

		with open('/users/PCON0003/osu10670/wfirst_imsim/corr_figures/corr_jackknife_'+self.psf_name+'.cPickle','wb') as f:
			pickle.dump((self.hpind,self.ind,self.count,self.xy_hpind,self.xy_ind,self.xy_count),f)

	def load_data(self):
		with open('/users/PCON0003/osu10670/wfirst_imsim/corr_figures/corr_sky_'+self.psf_name+'.cPickle','rb') as f:
			sky=pickle.load(f)
		self.ra,self.dec,self.delta_e1,self.delta_e2=sky[0],sky[1],sky[2],sky[3]

		# with open('/users/PCON0003/osu10670/wfirst_imsim/corr_figures/corr_field_'+self.psf_name+'.cPickle','rb') as f2:
		# 	plane=pickle.load(f2)
		# self.x,self.y,self.delta_field_e1,self.delta_field_e2=plane[0],plane[1],plane[2],plane[3]

		# with open('/users/PCON0003/osu10670/wfirst_imsim/corr_figures/corr_jackknife_'+self.psf_name+'.cPickle','rb') as f2:
		# 	ind=pickle.load(f2)
		# self.hpind,self.ind,self.count,self.xy_hpind,self.xy_ind,self.xy_count=ind[0],ind[1],ind[2],ind[3],ind[4],ind[5]

# dict=['anismear','tilt','coma','astigmatism','focus','gradz4','gradz6','isosmear','piston','ransmear']

psf=sys.argv[1]
f=corr_func(psf)
f.psf_shape()
f.sky_corr()
print('Done '+psf+' 2pt_corr plot')

# psf=sys.argv[2]
# if sys.argv[1]=='ind':
# 	f=corr_func(psf)
# 	f.psf_shape()
# 	f.save_data()
# elif sys.argv[1]=='corr':
# 	f=corr_func(psf)
# 	f.load_data()
# 	f.sky_corr()
# 	# f.xy_corr()
# 	print('Done '+psf+' 2pt_corr plot')

# for psf in dict:
# 	f.psf_shape(psf)
# 	f.save_data()
# 	f.sky_corr()
# 	f.xy_corr()
# 	print('Done '+psf+' 2pt_corr plot')









