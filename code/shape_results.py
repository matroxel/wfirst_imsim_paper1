import fitsio as fio
import os
import numpy as np
import matplotlib.pyplot as plt


# e1=np.array([],dtype='>f8')
# e2=np.array([],dtype='>f8')
# int_e1=np.array([],dtype='>f8')
# int_e2=np.array([],dtype='>f8')
# psf_e1=np.array([],dtype='>f8')
# psf_e2=np.array([],dtype='>f8')
# psf_T=np.array([],dtype='>f8')
# hlr=np.array([],dtype='>f8')
# snr=np.array([],dtype='>f8')
# g1=np.array([],dtype='>f8')
# g2=np.array([],dtype='>f8')
# nexp_used=np.array([],dtype='>f8')
# fid_e1=np.array([],dtype='>f8')
# fid_e2=np.array([],dtype='>f8')
# fid_int_e1=np.array([],dtype='>f8')
# fid_int_e2=np.array([],dtype='>f8')
# fid_psf_e1=np.array([],dtype='>f8')
# fid_psf_e2=np.array([],dtype='>f8')
# fid_psf_T=np.array([],dtype='>f8')
# fid_hlr=np.array([],dtype='>f8')
# fid_snr=np.array([],dtype='>f8')
# fid_nexp_used=np.array([],dtype='>f8')

# file_names=os.listdir('/fs/scratch/cond0083/wfirst_sim_anismear/ngmix/')

#missing anismear
dict=['oscz4','oscz7','anismear','tilt','coma','astigmatism','focus','gradz4','gradz6','isosmear','piston','ransmear']

class shape_results:

	def fiducial(self):
		self.fid=fio.FITS('/fs/scratch/cond0083/fiducial_H158_final.fits.gz')[-1].read()
		fid=self.fid[(self.fid['flags']==0)&(self.fid['ra']>0)]
		self.fid_e1=fid['e1']
		self.fid_e2=fid['e2']
		self.fid_g1=fid['g1']
		self.fid_g2=fid['g2']
		self.fid_psf_e1=fid['psf_e1']
		self.fid_psf_e2=fid['psf_e2']
		self.fid_psf_T=fid['psf_T']
		self.fid_hlr=fid['hlr']
		self.fid_snr=fid['snr']

		# mean_fid_e1=np.mean(self.fid_e1)
		# std_fid_e1=np.std(self.fid_e1)/np.sqrt(len(self.fid_e1))
		# mean_fid_e2=np.mean(self.fid_e2)
		# std_fid_e2=np.std(self.fid_e2)/np.sqrt(len(self.fid_e2))
		# mean_fid_psf_e1=np.mean(self.fid_psf_e1)
		# # std_fid_psf_e1=np.std(self.fid_psf_e1)/np.sqrt(len(self.fid_psf_e1))
		# mean_fid_psf_e2=np.mean(self.fid_psf_e2)
		# std_fid_psf_e2=np.std(self.fid_psf_e2)/np.sqrt(len(self.fid_psf_e2))
		# mean_fid_psf_T=np.mean(self.fid_psf_T)
		# std_fid_psf_T=np.std(self.fid_psf_T)/np.sqrt(len(self.fid_psf_T))
		# mean_fid_hlr=np.mean(self.fid_hlr)
		# std_fid_hlr=np.std(self.fid_hlr)/np.sqrt(len(self.fid_hlr))
		# mean_fid_snr=np.mean(self.fid_snr)
		# std_fid_snr=np.std(self.fid_snr)/np.sqrt(len(self.fid_snr))

		self.fid_m1, self.fid_b1, sig_m1, sig_b1, sig_y1 = self.linear_regression(self.fid_g1,self.fid_e1)
		self.fid_m2, self.fid_b2, sig_m2, sig_b2, sig_y2 = self.linear_regression(self.fid_g2,self.fid_e2)

		# print('fid_e1='+str(mean_fid_e1)+'+-'+str(std_fid_e1))
		# print('fid_e2='+str(mean_fid_e2)+'+-'+str(std_fid_e2))
		# # print('fid_psf_e1='+str(mean_fid_psf_e1)+'+-'+str(std_fid_psf_e1))
		# print('fid_psf_e2='+str(mean_fid_psf_e2)+'+-'+str(std_fid_psf_e2))
		# print('fid_psf_T='+str(mean_fid_psf_T)+'+-'+str(std_fid_psf_T))
		# print('fid_hlr='+str(mean_fid_hlr)+'+-'+str(std_fid_hlr))
		# print('fid_snr='+str(mean_fid_snr)+'+-'+str(std_fid_snr))
		print('fid m1='+str(self.fid_m1-1)+'+-'+str(sig_m1)+',m2='+str(self.fid_m2-1)+'+-'+str(sig_m2))
		print('fid c1='+str(self.fid_b1)+'+-'+str(sig_b1)+',c2='+str(self.fid_b2)+'+-'+str(sig_b2))


	def statistics(self,psf_name):
		self.psf_name=psf_name
		f=fio.FITS('/fs/scratch/cond0083/'+psf_name+'_H158_final.fits.gz')[-1].read()
		# bool=(f['flags']==0)&(f['ra']>0)
		# fid=self.fid[bool]
		# bool2= (fid['flags']==0)&(fid['ra']>0)
		# f=f[bool][bool2]
		# fid=fid[bool2]
		bool=(f['flags']==0)&(f['ra']>0)&(self.fid['flags']==0)&(self.fid['ra']>0)
		fid=self.fid[bool]
		f=f[bool]
		

		e1=f['e1']
		e2=f['e2']
		g1=f['g1']
		g2=f['g2']
		# psf_e1=fid[(f['flags']==0)&(f['ra']>0)]['psf_e1']
		# psf_e2=fid[(f['flags']==0)&(f['ra']>0)]['psf_e2']
		# psf_T=f['psf_T']
		# hlr=f['hlr']
		# snr=f['snr']

		# mean_e1=np.mean(e1)
		# std_e1=np.std(e1)/np.sqrt(len(e1))
		# mean_e2=np.mean(e2)
		# std_e2=np.std(e2)/np.sqrt(len(e2))
		# mean_hlr=np.mean(hlr)
		# std_hlr=np.std(hlr)/np.sqrt(len(hlr))
		# mean_snr=np.mean(snr)
		# std_snr=np.std(snr)/np.sqrt(len(snr))

		# print(self.psf_name+'fid_e1 '+str(np.mean(fid['e1'])))
		# print(self.psf_name+'fid_e2 '+str(np.mean(fid['e2'])))
		delta_e1=e1-fid['e1']
		delta_e2=e2-fid['e2']
		mean_de1=np.mean(delta_e1)
		mean_de2=np.mean(delta_e2)
		print(self.psf_name+'delta_de1 '+str(mean_de1))
		print(self.psf_name+'delta_de2 '+str(mean_de2))
		std_de1=np.std(delta_e1)/np.sqrt(len(delta_e1))
		std_de2=np.std(delta_e2)/np.sqrt(len(delta_e2))
		print(self.psf_name+'std_de1 '+str(mean_de1))
		print(self.psf_name+'std_de2 '+str(mean_de2))
		de1_dz=np.mean(delta_e1)/6.465
		de2_dz=np.mean(delta_e2)/6.465
		de1_dz_std=np.std(delta_e1)/6.465/np.sqrt(len(delta_e1))
		de2_dz_std=np.std(delta_e2)/6.465/np.sqrt(len(delta_e2))

		m1, b1, sig_m1, sig_b1, sig_y1 = self.linear_regression(g1,e1)
		m2, b2, sig_m2, sig_b2, sig_y2 = self.linear_regression(g2,e2)

		# print(self.psf_name+'_de1/dz='+str(de1_dz)+'+-'+str(de1_dz_std))
		# print(self.psf_name+'_de2/dz='+str(de2_dz)+'+-'+str(de2_dz_std))
		# print(self.psf_name+'_e1='+str(mean_e1)+'+-'+str(std_e1))
		# print(self.psf_name+'_e2='+str(mean_e2)+'+-'+str(std_e2))
		# print(self.psf_name+'_hlr='+str(mean_hlr)+'+-'+str(std_hlr))
		# print(self.psf_name+'_snr='+str(mean_snr)+'+-'+str(std_snr))
		# print(self.psf_name+'_de1='+str(mean_de1)+'+-'+str(std_de1))
		# print(self.psf_name+'_de2='+str(mean_de2)+'+-'+str(std_de2))
		print(self.psf_name+' m1='+str(m1-1)+'+-'+str(sig_m1)+',m2='+str(m2-1)+'+-'+str(sig_m2))
		print(self.psf_name+' b1='+str(b1)+'+-'+str(sig_b1)+',b2='+str(b2)+'+-'+str(sig_b2))
		print(self.psf_name+' dm1='+str(m1-self.fid_m1)+',dm2='+str(m2-self.fid_m2))
		print(self.psf_name+' db1='+str(b1-self.fid_b1)+',b2='+str(b2)+'+-'+str(sig_b2))
		print(self.psf_name+'de1/dz^2+de2/dz^2='+str((de1_dz**2+de2_dz**2)*6.465**2))

	def linear_regression(self,x, y):
	    mean_x = np.mean(x)
	    mean_y = np.mean(y)

	    rxy = np.mean((x-mean_x)*(y-mean_y))/np.sqrt(np.mean((x-mean_x)**2))/np.sqrt(np.mean((y-mean_y)**2))
	    slope = rxy * np.std(y)/np.std(x) # beta in Wikipedia
	    intercept = mean_y - slope * mean_x  # alpha in Wikipedia
	    ndata = len(x)
	    sum_residual_sqr = sum((y-(slope*x+intercept))**2)/(ndata-2)
	    sig_y = np.sqrt(sum_residual_sqr)
	    sig_slope_sqr = sum_residual_sqr/sum((x-mean_x)**2)
	    sig_slope = np.sqrt(sig_slope_sqr)
	    sig_intercept = sig_slope * np.sqrt(np.mean(x*x))
	    return slope, intercept, sig_slope, sig_intercept, sig_y

f=shape_results()
f.fiducial()
for psf in dict:
	f.statistics(psf)

# for file in file_names:
# 	# f = fio.FITS('/fs/scratch/cond0083/wfirst_sim_fiducial/ngmix/'+file)[1].read()
# 	print(file)
# 	f = fio.FITS('/fs/scratch/cond0083/wfirst_sim_anismear/ngmix/'+file)[1].read()
# 	# f2 = fio.FITS('/fs/scratch/cond0083/wfirst_sim_'+self.dir_name+'/ngmix/'+file)[1].read()
# 	# for j in range(len(f)):
# 		# if (f['flags'][j]==0 and f['ra'][j]>0):
# 		# if True:
# 	fid_e1=np.append(fid_e1,f['e1'][(f['flags']==0) & (f['ra']>0)])
# 	fid_e2=np.append(fid_e2,f['e2'][(f['flags']==0) & (f['ra']>0)])
		# fid_int_e1.append(f['int_e1'][j])
		# fid_int_e2.append(f['int_e2'][j])
		# fid_psf_e1.append(f['psf_e1'][j])
		# fid_psf_e2.append(f['psf_e2'][j])
		# fid_psf_T.append(f['psf_T'][j])
		# fid_nexp_used.append(f['nexp_used'][j])
		# fid_hlr.append(f['hlr'][j])
		# fid_snr.append(f['snr'][j])
		# e1.append(f2['e1'][j])
		# e2.append(f2['e2'][j])
		# int_e1.append(f2['int_e1'][j])
		# int_e2.append(f2['int_e2'][j])
		# psf_e1.append(f2['psf_e1'][j])
		# psf_e2.append(f2['psf_e2'][j])
		# psf_T.append(f2['psf_T'][j])
		# hlr.append(f2['hlr'][j])
		# snr.append(f2['snr'][j])
		# g1.append(f2['g1'][j])
		# g2.append(f2['g2'][j])
		# nexp_used.append(f2['nexp_used'][j])

		# mean_fid_e1=np.mean(np.array(fid_e1))
		# std_fid_e1=np.std(np.array(fid_e1))
		# mean_fid_e2=np.mean(np.array(fid_e2))
		# std_fid_e2=np.std(np.array(fid_e2))
		# mean_fid_psf_e1=np.mean(np.array(fid_psf_e1))
		# std_fid_psf_e1=np.std(np.array(fid_psf_e1))
		# mean_fid_psf_e2=np.mean(np.array(fid_psf_e2))
		# std_fid_psf_e2=np.std(np.array(fid_psf_e2))
		# mean_fid_psf_T=np.mean(np.array(fid_psf_T))
		# std_fid_psf_T=np.std(np.array(fid_psf_T))
		# mean_fid_hlr=np.mean(np.array(fid_hlr))
		# std_fid_hlr=np.std(np.array(fid_hlr))
		# mean_fid_snr=np.mean(np.array(fid_snr))
		# std_fid_snr=np.std(np.array(fid_snr))

		# delta_e1=np.array(e1)-np.array(fid_e1)
		# delta_e2=np.array(e2)-np.array(fid_e2)
		# mean_de1=np.mean(delta_e1)
		# mean_de2=np.mean(delta_e2)
		# std_de1=np.std(delta_e1)
		# std_de2=np.std(delta_e2)
		# de1_dz4=np.mean(delta_e1)/6.465
		# de2_dz4=np.mean(delta_e2)/6.465
		# de1_dz4_std=np.std(delta_e1)/6.465
		# de2_dz4_std=np.std(delta_e2)/6.465

		# mean_e1=np.mean(np.array(e1))
		# std_e1=np.std(np.array(e1))
		# mean_e2=np.mean(np.array(e2))
		# std_e2=np.std(np.array(e2))
		# mean_hlr=np.mean(np.array(hlr))
		# std_hlr=np.std(np.array(hlr))
		# mean_snr=np.mean(np.array(snr))
		# std_snr=np.std(np.array(snr))


		# mod1 = sm.OLS(e1,g1)
		# mod2 = sm.OLS(e2,g2)
		# res1 = mod1.fit()
		# res2 = mod2.fit()

		# print('fid_e1='+str(mean_fid_e1)+'+-'+str(std_fid_e1))
		# print('fid_e2='+str(mean_fid_e2)+'+-'+str(std_fid_e2))
		# print('fid_psf_e1='+str(mean_fid_psf_e1)+'+-'+str(std_fid_psf_e1))
		# print('fid_psf_e2='+str(mean_fid_psf_e2)+'+-'+str(std_fid_psf_e2))
		# print('fid_psf_T='+str(mean_fid_psf_T)+'+-'+str(std_fid_psf_T))
		# print('fid_hlr='+str(mean_fid_hlr)+'+-'+str(std_fid_hlr))
		# print('fid_snr='+str(mean_fid_snr)+'+-'+str(std_fid_snr))
		# print(self.dir_name+'_e1='+str(mean_e1)+'+-'+str(std_e1))
		# print(self.dir_name+'_e2='+str(mean_e2)+'+-'+str(std_e2))
		# print(self.dir_name+'_hlr='+str(mean_hlr)+'+-'+str(std_hlr))
		# print(self.dir_name+'_snr='+str(mean_snr)+'+-'+str(std_snr))
		# print(self.dir_name+'_de1='+str(mean_de1)+'+-'+str(std_de1))
		# print(self.dir_name+'_de2='+str(mean_de2)+'+-'+str(std_de2))

		# plt.hist(e1,bins=50)
		# plt.ylabel('N')
		# plt.xlabel('e1')
		# plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_e1')

		# plt.hist(e2,bins=50)
		# plt.ylabel('N')
		# plt.xlabel('e2')
		# plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_e2')

		# plt.hist(psf_e1,bins=200)
		# plt.ylabel('N')
		# plt.xlabel('PSF e1')
		# plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_psf_e1')

		# plt.hist(psf_e2,bins=200)
		# plt.ylabel('N')
		# plt.xlabel('PSF e2')
		# plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_psf_e2')

		# plt.hist(psf_T,bins=200)
		# plt.ylabel('N')
		# plt.xlabel('PSF FWHM(pix)')
		# plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_psf_fwhm')

		# plt.hist(nexp_used,bins=np.arange(-1,14))
		# plt.ylabel('N')
		# plt.xlabel('Number of exposures')
		# plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_nexp')

		# plt.hist(hlr,bins=np.arange(0,4,0.1))
		# plt.ylabel('N')
		# plt.xlabel('radius')
		# plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_hlr')

		# snr=np.log10(np.array(snr)[np.array(snr).nonzero()[0]])
		# plt.hist(snr,bins=200)
		# plt.ylabel('N')
		# plt.xlabel('log10(snr)')
		# plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_snr')
