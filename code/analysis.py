import sys, os
import fitsio as fio
import numpy as np
import treecorr
import matplotlib
from astropy.io import fits
import pickle
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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


class shear_error:

	def __init__(self,path):

		self.path=path
		# self.file_name = file_name

# for file in files:
# 	hdul = fits.open(path+'/'+file)
# 	for i in hdul[1].data:
# 		e1 = i[7]
# 		e2 = i[8]
# 		int_e1 = i[9]
# 		int_e2 = i[10]
# 		g1 = i[17]
# 		g2 =i[18]
# 		shear.append([e1,e2,g1,g2,int_e1,int_e2])




# for i in range(10):
# 	f = fio.FITS(files+str(i)+'.fits')[1].read()
# 	for j in range(len(f)):
# 		if (f['flags'][j]==0 and f['ra'][j]>0):
# 			e1.append(f['e1'][j])
# 			e2.append(f['e2'][j])
# 			snr.append(f['snr'][j])
# 			g1.append(f['g1'][j])
# 			g2.append(f['g2'][j])
# 	print len(e1),len(e2)

	def extract_shear(self):

		files=os.listdir(self.path)
		e1=e2=g1=g2=np.array([],dtype='>f8')
		# e1=[]
		# e2=[]
		# g1=[]
		# g2=[]

		for file in files:
			# f = self.path+'/'+file
			f = fio.FITS(self.path+'/'+file)[1].read()
		# zeros = fitsio.read(f,columns='flags').nonzero()
			# for j in range(len(f)):
			# 	if (f['flags'][j]==0 and f['ra'][j]>0):
			e1=np.append(e1,f['e1'][(f['flags']==0) & (f['ra']>0)])
			e2=np.append(e2,f['e2'][(f['flags']==0) & (f['ra']>0)])
			g1=np.append(g1,f['g1'][(f['flags']==0) & (f['ra']>0)])
			g2=np.append(g2,f['g2'][(f['flags']==0) & (f['ra']>0)])					

		return e1,e2,g1,g2

	def estimate_cfs(self,e1,e2,g1,g2):

		A1 = np.vstack([g1, np.ones(len(g1))]).T
		m1, c1 = np.linalg.lstsq(A1, e1, rcond=None)[0]
		m1 = m1-1
		A2 = np.vstack([g2, np.ones(len(g2))]).T
		m2, c2 = np.linalg.lstsq(A2, e2, rcond=None)[0]
		m2 = m2-1
		print ('m1='+str(m1),'c1='+str(c1), 'm2='+str(m2), 'c2='+str(c2))

		return m1,c1, m2, c2

	def line_plot(self,m1,c1,m2,c2,image_name):

		x = np.zeros(100)
		for i in range(100):
			x[i]=0.01*i

		plt.plot(x,(1+m1)*x+c1,label="m1="+str(m1)+", c1="+str(c1))
		plt.plot(x,(1+m2)*x+c2,label="m2="+str(m2)+", c2="+str(c2))
		plt.plot(x,x,label="$\gamma_{true}=\gamma_{obs}$")
		plt.xlabel('$\gamma_{true}$')
		plt.ylabel('$\gamma_{obs}$')
		plt.legend(loc="upper left")
		plt.savefig(image_name)
		plt.show()

class corr_func:
	def __init__(self,path,file_name,psf_name):

		self.path=path
		self.file_name=file_name
		self.psf_name=psf_name
		ra=dec=e1=e2=fid_e1=fid_e2=x=y=sca_x=sca_y=sca=np.array([],dtype='>f8')

	def extract_info(self):

		file=self.path+'/'+self.file_name
		file2=self.path.rstrip('ngmix')+'meds/'+self.file_name.rstrip('0.fits').rstrip('_')+'.fits.gz'
		fid = fio.FITS('/fs/scratch/cond0083/wfirst_sim_fiducial/ngmix/fiducial'+self.file_name.lstrip(self.psf_name))[1].read()
		
		f=fio.FITS(file)[1].read()
		f2=fits.open(file2)[1].data
		# f = fio.FITS('/fs/scratch/cond0083/wfirst_sim_fiducial/ngmix/'+file)[1].read()

		# for j in range(len(f2)):
		# 	if (f['flags'][j]==0 and f['ra'][j]>0):
		# 		e1=np.append(e1,f['e1'][j]) #e1,f2['e1'][(f2['flags']==0)&(f2['ra']>0)])
		# 		e2=np.append(e2,f['e2'][j]) #e2,f2['e2'][(f2['flags']==0)&(f2['ra']>0)])
		# 		ra=np.append(ra,f['ra'][j])
		# 		dec=np.append(dec,f['dec'][j])
		# 		fid_e1=np.append(fid_e1,fid['e1'][j]) #,f['e1'][(f2['flags']==0)&(f2['ra']>0)])
		# 		fid_e2=np.append(fid_e2,fid['e2'][j]) #fid_e2,f['e2'][(f2['flags']==0)&(f2['ra']>0)])
		# 		sca_x=np.append(sca_X,f2['orig_col'][j])
		# 		sca_y=np.append(sca_y,f2['orig_row'][j])
		# 		sca=np.append(sca,f2['sca'][j])

		ra=f['ra'][(f['flags']==0) & (f['ra']>0)]
		dec=f['dec'][(f['flags']==0) & (f['ra']>0)]
		fid_e1=fid['e1'][(f['flags']==0) & (f['ra']>0)]
		fid_e2=fid['e2'][(f['flags']==0) & (f['ra']>0)]
		e1=f['e1'][(f['flags']==0) & (f['ra']>0)]
		e2=f['e2'][(f['flags']==0) & (f['ra']>0)]
		sca_x=f2['orig_col'][(f['flags']==0) & (f['ra']>0)]
		sca_y=f2['orig_row'][(f['flags']==0) & (f['ra']>0)]
		sca=f2['sca'][(f['flags']==0) & (f['ra']>0)]
		delta_e1=e1-fid_e1
		delta_e2=e2-fid_e2

		focal_plane_x = []
		focal_plane_y =[]
		for i in range(len(sca)):
			for j in range(len(sca[i])):
				sca_to_plane=field_methods(sca[i][j],sca_x[i][j],sca_y[i][j])
				x, y=sca_to_plane.get_field_pos()
				focal_plane_x.append(x)
				focal_plane_y.append(y)

		return ra,dec,delta_e1,delta_e2,delta_e1.repeat(len(sca[0])),delta_e2.repeat(len(sca[0])),np.array(focal_plane_x),np.array(focal_plane_y)

	def xy_corr(self,x,y,g1,g2):
		cat = treecorr.Catalog(x=x, y=y, g1=g1, g2=g2)
		gg = treecorr.GGCorrelation(min_sep=0.1, max_sep=200, nbins=20)
		gg.process(cat)

		return gg

	def sky_corr(self,ra,dec,g1,g2):
		cat = treecorr.Catalog(ra=ra, dec=dec, g1=g1, g2=g2,ra_units='deg',dec_units='deg')
		gg = treecorr.GGCorrelation(min_sep=1, max_sep=400, nbins=20, sep_units='arcmin')
		gg.process(cat)

		return gg

	def corr_plot(self,gg,file_name,type):
		r = np.exp(gg.meanlogr)
		xip = gg.xip
		xim = gg.xim
		sig = np.sqrt(gg.varxip)

		# plt.plot(r, xip, color='blue','o')
		# plt.plot(r, -xip, color='blue', 'x')
		plt.errorbar(r[xip>0], xip[xip>0], yerr=sig[xip>0], color='blue', fmt='o')
		plt.errorbar(r[xip<0], -xip[xip<0], yerr=sig[xip<0], color='blue', fmt='x')
		lp = plt.errorbar(-r, xip, yerr=sig, color='blue')

		# plt.plot(r, xim, color='green','o')
		# plt.plot(r, -xim, color='green', 'x')
		plt.errorbar(r[xim>0], xim[xim>0], yerr=sig[xim>0], color='red', fmt='o')
		plt.errorbar(r[xim<0], -xim[xim<0], yerr=sig[xim<0], color='red', fmt='x')
		lm = plt.errorbar(-r, xim, yerr=sig, color='red')

		plt.xscale('log')
		plt.yscale('log', nonposy='clip')

		if type=='sky':
			plt.xlabel(r'$\theta$(arcmin)')
		elif type=='plane':
			plt.xlabel(r'$d$(mm)')


		plt.legend([lp, lm], [r'$\xi_+(d)$', r'$\xi_-(d)$'])
		plt.xlim( [1,200] )
		plt.ylabel(r'$\xi_{+,-}$')
		plt.savefig(file_name)
		# plt.show()

class shape_results:
	def __init__(self,path,psf_name):
		self.path=path
		self.psf_name=psf_name

	def results(self):
		e1=e2=int_e1=int_e2=psf_e1=psf_e2=psf_T=hlr=snr=g1=g2=nexp_used=fid_e1=fid_e2=fid_int_e1=fid_int_e2=fid_psf_e1=fid_psf_e2=fid_psf_T=fid_hlr=fid_snr=fid_nexp_used=np.array([],dtype='>f8')

		file_names=os.listdir(self.path)
		
		for file in file_names:
			print(file)
			# f = fio.FITS('/fs/scratch/cond0083/wfirst_sim_fiducial/ngmix/'+file)[1].read()
			f = fio.FITS('/fs/scratch/cond0083/wfirst_sim_fiducial/ngmix/'+'fiducial'+file.lstrip(self.psf_name))[1].read()
			f2 = fio.FITS('/fs/scratch/cond0083/wfirst_sim_'+self.psf_name+'/ngmix/'+file)[1].read()
			for j in range(len(f2)):
				if (f2['flags'][j]==0 and f2['ra'][j]>0):
					fid_e1=np.append(fid_e1,f['e1'][j]) #,f['e1'][(f2['flags']==0)&(f2['ra']>0)])
					fid_e2=np.append(fid_e2,f['e2'][j]) #fid_e2,f['e2'][(f2['flags']==0)&(f2['ra']>0)])
					fid_int_e1=np.append(fid_int_e1,f['int_e1'][j]) #fid_int_e1,f['int_e1'][(f2['flags']==0)&(f2['ra']>0)])
					fid_int_e2=np.append(fid_int_e2,f['int_e2'][j]) #fid_int_e2,f['int_e2'][(f2['flags']==0)&(f2['ra']>0)])
					fid_psf_e1=np.append(fid_psf_e1,f['psf_e1'][j]) #fid_psf_e1,f['psf_e1'][(f2['flags']==0)&(f2['ra']>0)])
					fid_psf_e2=np.append(fid_psf_e2,f['psf_e2'][j]) #fid_psf_e2,f['psf_e2'][(f2['flags']==0)&(f2['ra']>0)])
					fid_psf_T=np.append(fid_psf_T,f['psf_T']) #fid_psf_T,f['psf_T'][(f2['flags']==0)&(f2['ra']>0)])
					fid_nexp_used=np.append(fid_nexp_used,f['nexp_used'][j]) #fid_nexp_used,f['nexp_used'][(f2['flags']==0)&(f2['ra']>0)])
					fid_hlr=np.append(fid_hlr,f['hlr'][j]) #fid_hlr,f['hlr'][(f2['flags']==0)&(f2['ra']>0)])
					fid_snr=np.append(fid_snr,f['snr'][j]) #fid_snr,f['snr'][(f2['flags']==0)&(f2['ra']>0)])
					e1=np.append(e1,f2['e1'][j]) #e1,f2['e1'][(f2['flags']==0)&(f2['ra']>0)])
					e2=np.append(e2,f2['e2'][j]) #e2,f2['e2'][(f2['flags']==0)&(f2['ra']>0)])
					int_e1=np.append(int_e1,f2['int_e1'][j]) #int_e1,f2['int_e1'][(f2['flags']==0)&(f2['ra']>0)])
					int_e2=np.append(int_e2,f2['int_e2'][j]) #int_e2,f2['int_e2'][(f2['flags']==0)&(f2['ra']>0)])
					psf_e1=np.append(psf_e1,f2['psf_e1'][j]) #psf_e1,f2['psf_e1'][(f2['flags']==0)&(f2['ra']>0)])
					psf_e2=np.append(psf_e2,f2['psf_e2'][j]) #psf_e2,f2['psf_e2'][(f2['flags']==0)&(f2['ra']>0)])
					psf_T=np.append(psf_T,f2['psf_T'][j]) #psf_T,f2['psf_T'][(f2['flags']==0)&(f2['ra']>0)])
					hlr=np.append(hlr,f2['hlr'][j]) #hlr,f2['hlr'][(f2['flags']==0)&(f2['ra']>0)])
					snr=np.append(snr,f2['snr'][j]) #snr,f2['snr'][(f2['flags']==0)&(f2['ra']>0)])
					g1=np.append(g1,f2['g1'][j]) #g1,f2['g1'][(f2['flags']==0)&(f2['ra']>0)])
					g2=np.append(g2,f2['g2'][j]) #g2,f2['g2'][(f2['flags']==0)&(f2['ra']>0)])
					nexp_used=np.append(nexp_used,f2['nexp_used'][j]) #nexp_used,f2['nexp_used'][(f2['flags']==0)&(f2['ra']>0)])

		mean_fid_e1=np.mean(fid_e1)
		std_fid_e1=np.std(fid_e1)
		mean_fid_e2=np.mean(fid_e2)
		std_fid_e2=np.std(fid_e2)
		mean_fid_psf_e1=np.mean(fid_psf_e1)
		std_fid_psf_e1=np.std(fid_psf_e1)
		mean_fid_psf_e2=np.mean(fid_psf_e2)
		std_fid_psf_e2=np.std(fid_psf_e2)
		mean_fid_psf_T=np.mean(fid_psf_T)
		std_fid_psf_T=np.std(fid_psf_T)
		mean_fid_hlr=np.mean(fid_hlr)
		std_fid_hlr=np.std(fid_hlr)
		mean_fid_snr=np.mean(fid_snr)
		std_fid_snr=np.std(fid_snr)

		delta_e1=e1-fid_e1
		delta_e2=e2-fid_e2
		mean_de1=np.mean(delta_e1)
		mean_de2=np.mean(delta_e2)
		std_de1=np.std(delta_e1)
		std_de2=np.std(delta_e2)
		de1_dpsf=np.mean(delta_e1)/6.465
		de2_dpsf=np.mean(delta_e2)/6.465
		de1_dpsf_std=np.std(delta_e1)/6.465
		de2_dpsf_std=np.std(delta_e2)/6.465

		mean_e1=np.mean(e1)
		std_e1=np.std(e1)
		mean_e2=np.mean(e2)
		std_e2=np.std(e2)
		mean_hlr=np.mean(hlr)
		std_hlr=np.std(hlr)
		mean_snr=np.mean(snr)
		std_snr=np.std(snr)


		# mod1 = sm.OLS(e1,g1)
		# mod2 = sm.OLS(e2,g2)
		# res1 = mod1.fit()
		# res2 = mod2.fit()

		print('de1/d'+self.psf_name+'='+str(de1_dpsf)+'+-'+str(de1_dpsf_std))
		print('de2/d'+self.psf_name+'='+str(de2_dpsf)+'+-'+str(de2_dpsf_std))
		print('fid_e1='+str(mean_fid_e1)+'+-'+str(std_fid_e1))
		print('fid_e2='+str(mean_fid_e2)+'+-'+str(std_fid_e2))
		print('fid_psf_e1='+str(mean_fid_psf_e1)+'+-'+str(std_fid_psf_e1))
		print('fid_psf_e2='+str(mean_fid_psf_e2)+'+-'+str(std_fid_psf_e2))
		print('fid_psf_T='+str(mean_fid_psf_T)+'+-'+str(std_fid_psf_T))
		print('fid_hlr='+str(mean_fid_hlr)+'+-'+str(std_fid_hlr))
		print('fid_snr='+str(mean_fid_snr)+'+-'+str(std_fid_snr))
		print(self.psf_name+'_delta_e1='+str(mean_de1)+'+-'+str(std_de1))
		print(self.psf_name+'_delta_e2='+str(mean_de2)+'+-'+str(std_de2))
		print(self.psf_name+'_e1='+str(mean_e1)+'+-'+str(std_e1))
		print(self.psf_name+'_e2='+str(mean_e2)+'+-'+str(std_e2))
		print(self.psf_name+'_hlr='+str(mean_hlr)+'+-'+str(std_hlr))
		print(self.psf_name+'_snr='+str(mean_snr)+'+-'+str(std_snr))
		print(self.psf_name+'_de1='+str(mean_de1)+'+-'+str(std_de1))
		print(self.psf_name+'_de2='+str(mean_de2)+'+-'+str(std_de2))

		plt.hist(e1,bins=50)
		plt.ylabel('N')
		plt.xlabel('e1')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.psf_name+'_e1')

		plt.hist(e2,bins=50)
		plt.ylabel('N')
		plt.xlabel('e2')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.psf_name+'_e2')

		plt.hist(psf_e1,bins=200)
		plt.ylabel('N')
		plt.xlabel('PSF e1')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.psf_name+'_psf_e1')

		plt.hist(psf_e2,bins=200)
		plt.ylabel('N')
		plt.xlabel('PSF e2')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.psf_name+'_psf_e2')

		plt.hist(psf_T,bins=200)
		plt.ylabel('N')
		plt.xlabel('PSF FWHM(pix)')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.psf_name+'_psf_fwhm')

		plt.hist(nexp_used,bins=np.arange(-1,14))
		plt.ylabel('N')
		plt.xlabel('Number of exposures')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.psf_name+'_nexp')

		plt.hist(hlr,bins=np.arange(0,4,0.1))
		plt.ylabel('N')
		plt.xlabel('radius')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.psf_name+'_hlr')

		snr=np.log10(np.array(snr)[np.array(snr).nonzero()[0]])
		plt.hist(snr,bins=200)
		plt.ylabel('N')
		plt.xlabel('log10(snr)')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.psf_name+'_snr')

	def focal_plane_hist(self):

		delta_e1=np.array([])
		delta_e2=np.array([])
		x=np.array([])
		y=np.array([])

		files=os.listdir('/fs/scratch/cond0083/wfirst_sim_'+self.psf_name+'/ngmix')
		for file in files:
			delta_e10, delta_e20, x0, y0 = self.delta_e(file)
			delta_e1=np.append(delta_e1,delta_e10)
			delta_e2=np.append(delta_e2,delta_e20)
			x=np.append(x,x0)
			y=np.append(y,y0)
			print (file,len(x))
		f=open('hist_2d_'+self.psf_name+'.pickle','wb')
		pickle.dump(np.vstack((x,y,delta_e1,delta_e2)),f)
		f.close()

		plt.hexbin(x,y,C=delta_e1,mincnt=5,gridsize=10,cmap=plt.cm.jet)
		plt.title('<'+self.psf_name+'_e1-fid_e1>')
		plt.xlabel('x(mm)')
		plt.ylabel('y(mm)')
		plt.colorbar()
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_2d_'+self.psf_name+'_e1')

		plt.hexbin(x,y,C=delta_e2,mincnt=5,gridsize=10,cmap=plt.cm.jet)
		plt.title('<'+self.psf_name+'_e2-fid_e2>')
		plt.xlabel('x(mm)')
		plt.ylabel('y(mm)')
		plt.colorbar()
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_2d_'+self.psf_name+'_e2')

# with open('hist_2d_coma.pickle','rb') as f:
# 	a=pickle.load(f)

# plt.hexbin(a[0],a[1],C=a[3],mincnt=10,gridsize=10,cmap=plt.cm.jet)
# plt.title('<coma_e2-fid_e2>')
# plt.xlabel('x(mm)')
# plt.ylabel('y(mm)')
# plt.colorbar()
# plt.show()


	def delta_e(self,file_name):

		e1=e2=fid_e1=fid_e2=sca_x=sca_y=sca=np.array([],dtype='>f8')

		file = fio.FITS('/fs/scratch/cond0083/wfirst_sim_'+self.psf_name+'/ngmix/'+file_name)[1].read()
		file2= fits.open('/fs/scratch/cond0083/wfirst_sim_'+self.psf_name+'/meds/'+file_name.rstrip('0.fits').rstrip('_')+'.fits.gz')[1].data
		fid_file=fio.FITS('/fs/scratch/cond0083/wfirst_sim_fiducial/ngmix/fiducial'+file_name.lstrip(self.psf_name))[1].read()
			# fid_file2='/fs/scratch/cond0083/wfirst_sim_fiducial/meds/fiducial'+file_name.lstrip(psf_name).rstrip(0_fits)+'.fits.gz'
		# for j in range(len(file)):
		# 	if (file['flags'][j]==0 and file['ra'][j]>0):
		e1=np.append(e1,file['e1'][(file['flags']==0) & (file['ra']>0)])
		e2=np.append(e2,file['e2'][(file['flags']==0) & (file['ra']>0)])
		fid_e1=np.append(fid_e1,file['e1'][(file['flags']==0) & (file['ra']>0)])
		fid_e2=np.append(fid_e2,file['e2'][(file['flags']==0) & (file['ra']>0)])		
		sca_x=np.append(sca_x,file2['orig_col'][(file['flags']==0) & (file['ra']>0)])
		sca_y=np.append(sca_y,file2['orig_row'][(file['flags']==0) & (file['ra']>0)])
		sca=np.append(sca,file2['sca'][(file['flags']==0) & (file['ra']>0)])	

		focal_plane_x = []
		focal_plane_y =[]
		for i in range(len(sca)):
			for j in range(len(sca[i])):
				sca_to_plane=field_methods(sca[i][j],sca_x[i][j],sca_y[i][j])
				x, y=sca_to_plane.get_field_pos()
				focal_plane_x.append(x)
				focal_plane_y.append(y)

		delta_e1=e1-fid_e1
		delta_e2=e2-fid_e2

		return delta_e1.repeat(len(sca[0])),delta_e2.repeat(len(sca[0])),np.array(focal_plane_x),np.array(focal_plane_y)



path = sys.argv[2]
if sys.argv[1] == 'shear_error':
	f = shear_error(path)
	e1,e2,g1,g2 = f.extract_shear()
	m1,c1,m2,c2 = f.estimate_cfs(e1,e2,g1,g2)
	image_name = sys.argv[3]
	f.line_plot(m1,c1,m2,c2,image_name)

elif sys.argv[1] == 'shape_results':
	psf_name=sys.argv[3]
	f = shape_results(path,psf_name)
	f.results()
	f.focal_plane_hist()

ra=dec=sky_e1=sky_e2=e1=e2=x=y=np.array([],dtype='>f8')
if sys.argv[1] == '2pt_corr':
	# psf_name=sys.argv[3]
	# files = os.listdir(path)
	# for file in files:
	# 	print(file)
	# 	corr = corr_func(path,file,psf_name)
	# 	ra_tmp,dec_tmp,e1_tmp,e2_tmp,e1_xy_tmp,e2_xy_tmp,x_tmp,y_tmp=corr.extract_info()
	# 	ra = np.append(ra,ra_tmp)
	# 	dec = np.append(dec,dec_tmp)
	# 	sky_e1 = np.append(sky_e1,e1_tmp)
	# 	sky_e2 = np.append(sky_e2,e2_tmp)
	# 	e1 = np.append(e1,e1_xy_tmp)
	# 	e2 = np.append(e2,e2_xy_tmp)
	# 	x = np.append(x,x_tmp)
	# 	y = np.append(y,y_tmp)
	# 	print((file,len(sky_e1),len(sky_e2),len(ra),len(dec),len(e1),len(e2),len(x),len(y)))

	sky_im_name = sys.argv[4]
	xy_im_name = sys.argv[5]

	# with open('focus_sky_corr.pickle','wb') as f:
	# 	pickle.dump(np.vstack((ra,dec,sky_e1,sky_e2)),f)

	# with open('focus_plane_corr.pickle','wb') as f2:
	# 	pickle.dump(np.vstack((e1,e2,x,y)),f2)

	# cat = treecorr.Catalog(ra=a[0], dec=a[1], g1=a[2], g2=a[3],ra_units='deg',dec_units='deg')
	# gg = treecorr.GGCorrelation(min_sep=1, max_sep=400, nbins=20, sep_units='arcmin')
	# gg.process(cat)
	# gg = corr.sky_corr(ra,dec,sky_e1,sky_e2)
	# corr.corr_plot(gg,sky_im_name,sky)

	# # with open('anismear_plane_corr.pickle','rb') as f:
	# # 	a=pickle.load(f)

	# gg_xy = corr.xy_corr(x,y,e1,e2)
	# corr.corr_plot(gg_xy,xy_im_name,plane)

	# with open('anismear_sky_corr.pickle','rb') as f:
	#  	a=pickle.load(f)


	# cat = treecorr.Catalog(ra=a[0], dec=a[1], g1=a[2], g2=a[3],ra_units='deg',dec_units='deg')
	# gg = treecorr.GGCorrelation(min_sep=1, max_sep=400, nbins=20, sep_units='arcmin')
	# gg.process(cat)
	# corr=corr_func(path,'anismear_sky_corr')
	# corr.corr_plot(gg,'anismear_sky_corr')

	# with open('focus_plane_corr.pickle','rb') as f:
	#  	a=pickle.load(f)

	# corr=corr_func(path,'focus_plane_corr','focus')
	# gg_xy = corr.xy_corr(a[0],a[1],a[2],a[3])
	# corr.corr_plot(gg_xy,xy_im_name,'plane')
	# corr.corr_plot(gg,'focus_plane_corr')

	with open('focus_sky_corr.pickle','rb') as f:
	 	a=pickle.load(f)

	corr=corr_func(path,'focus_plane_corr','focus')
	gg_sky = corr.sky_corr(a[0],a[1],a[2],a[3])
	corr.corr_plot(gg_sky,sky_im_name,'sky')


# if sys.argv[2] = 'sky_corr'

# path = sys.argv[1]
# files = os.listdir(path)
# ra=dec=sky_e1=sky_e2=e1=e2=x=y=np.array([],dtype='>f8')

# for file in files:
# 	print (file)
# 	corr=corr_func(path,file)
# 	ra_tmp,dec_tmp,e1_tmp,e2_tmp,e1_xy_tmp,e2_xy_tmp,x_tmp,y_tmp=corr.extract_info()
# 	ra = np.append(ra,ra_tmp)
# 	dec = np.append(dec,dec_tmp)
# 	sky_e1 = np.append(e1,e1_tmp)
# 	sky_e2 = np.append(e2,e2_tmp)
# 	e1 = np.append(e1,e1_xy_tmp)
# 	e2 = np.append(e2,e2_xy_tmp)
# 	x = np.append(x,x_tmp)
# 	y = np.append(y,y_tmp)
	


# gg = corr.xy_corr(x,y,e1,e2)
# corr.corr_plot(gg,'xy_corr'),

		# ra=np.array([],dtype='>f8')
		# dec=np.array([],dtype='>f8')
		# e1=np.array([],dtype='>f8')
		# e2=np.array([],dtype='>f8')
		# x=np.array([],dtype='>f8')
		# y=np.array([],dtype='>f8')

		# for file in files:
		# 	# ra_tmp = fitsio.read(path+'/'+file,columns='ra')
		# 	# dec_tmp = fitsio.read(path+'/'+file,columns='dec')
		# 	e1_tmp = fitsio.read(path+'/'+file,columns='e1')
		# 	e2_tmp = fitsio.read(path+'/'+file,columns='e2')
		# 	x_tmp = fitsio.read(path.rstrip('ngmix')+'meds/'+file,columns='orig_col')
		# 	y_tmp = fitsio.read(path.rstrip('ngmix')+'meds/'+file,columns='orig_row')
		# 	# ra=np.append(ra,ra_tmp)
		# 	# dec=np.append(dec,dec_tmp)
		# 	e1=np.append(e1,e1_tmp)
		# 	e2=np.append(e2,e2_tmp)


# path = '/fs/scratch/PCON0003/osu10670/wfirst_sim_out/ngmix'
# files = os.listdir(path)
# shear = []

# for file in files:
# 	hdul = fits.open(path+'/'+file)
# 	for i in hdul[1].data:
# 		e1 = i[7]
# 		e2 = i[8]
# 		int_e1 = i[9]
# 		int_e2 = i[10]
# 		g1 = i[17]
# 		g2 =i[18]
# 		shear.append([e1,e2,g1,g2,int_e1,int_e2])

# header = ['e1','e2','g1','g2','int_e1','int_e2']
# with open('/fs/scratch/PCON0003/osu10670/wfirst_sim_out/error/error.csv','w') as f:
# 	writer = csv.writer(f, delimiter=',')
# 	writer.writerow(header)

# 	for l in shear:
# 		writer.writerow(l)

# test
# points = np.zeros((18,20,2))

# for i in range(18):
# 	sca_points=[]
# 	sca_points=np.random.rand(20,2)*4096-2048
# 	plt.scatter(sca_points[:,0],sca_points[:,1],s=2)
# 	plt.xlim(-2048,2048)
# 	plt.ylim(-2048,2048)
# 	plt.gca().set_aspect('equal', adjustable='box')
# 	plt.savefig("sca"+str(i+1))
# 	plt.clf()
# 	points[i]=sca_points

# focal_plane_x = []
# focal_plane_y = []

# for i in range(18):
# 	for m, l in zip(points[i,:,0],points[i,:,1]):
# 		a=field_methods(i+1,m,l)
# 		x, y = a.get_field_pos()
# 		focal_plane_x=np.append(focal_plane_x,x)
# 		focal_plane_y=np.append(focal_plane_y,y)
# 		plt.plot(a.sca_corners()[i,:,0],a.sca_corners()[i,:,1])

# plt.scatter(focal_plane_x,focal_plane_y,s=0.5)
# plt.savefig("focal_plane")






































