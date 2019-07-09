import fitsio as fio
import os
import numpy as np
import matplotlib.pyplot as plt

class shape_results:
	def __init__(self,path,dir_name):
		self.path=path
		self.dir_name=dir_name

	def results(self):
		e1=[]
		e2=[]
		int_e1=[]
		int_e2=[]
		psf_e1=[]
		psf_e2=[]
		psf_T=[]
		hlr=[]
		snr=[]
		g1=[]
		g2=[]
		nexp_used=[]
		fid_e1=[]
		fid_e2=[]
		fid_int_e1=[]
		fid_int_e2=[]
		fid_psf_e1=[]
		fid_psf_e2=[]
		fid_psf_T=[]
		fid_hlr=[]
		fid_snr=[]
		fid_nexp_used=[]

		file_names=os.listdir(self.path)
		
		for file in file_names:
			# f = fio.FITS('/fs/scratch/cond0083/wfirst_sim_fiducial/ngmix/'+file)[1].read()
			f = fio.FITS('/fs/scratch/cond0083/wfirst_sim_fiducial/ngmix/'+'fiducial'+file.lstrip(self.dir_name))[1].read()
			f2 = fio.FITS('/fs/scratch/cond0083/wfirst_sim_'+self.dir_name+'/ngmix/'+file)[1].read()
			for j in range(len(f)):
				if (f['flags'][j]==0 and f['ra'][j]>0):
				# if True:
					fid_e1.append(f['e1'][j])
					fid_e2.append(f['e2'][j])
					fid_int_e1.append(f['int_e1'][j])
					fid_int_e2.append(f['int_e2'][j])
					fid_psf_e1.append(f['psf_e1'][j])
					fid_psf_e2.append(f['psf_e2'][j])
					fid_psf_T.append(f['psf_T'][j])
					fid_nexp_used.append(f['nexp_used'][j])
					fid_hlr.append(f['hlr'][j])
					fid_snr.append(f['snr'][j])
					e1.append(f2['e1'][j])
					e2.append(f2['e2'][j])
					int_e1.append(f2['int_e1'][j])
					int_e2.append(f2['int_e2'][j])
					psf_e1.append(f2['psf_e1'][j])
					psf_e2.append(f2['psf_e2'][j])
					psf_T.append(f2['psf_T'][j])
					hlr.append(f2['hlr'][j])
					snr.append(f2['snr'][j])
					g1.append(f2['g1'][j])
					g2.append(f2['g2'][j])
					nexp_used.append(f2['nexp_used'][j])

		mean_fid_e1=np.mean(np.array(fid_e1))
		std_fid_e1=np.std(np.array(fid_e1))
		mean_fid_e2=np.mean(np.array(fid_e2))
		std_fid_e2=np.std(np.array(fid_e2))
		mean_fid_psf_e1=np.mean(np.array(fid_psf_e1))
		std_fid_psf_e1=np.std(np.array(fid_psf_e1))
		mean_fid_psf_e2=np.mean(np.array(fid_psf_e2))
		std_fid_psf_e2=np.std(np.array(fid_psf_e2))
		mean_fid_psf_T=np.mean(np.array(fid_psf_T))
		std_fid_psf_T=np.std(np.array(fid_psf_T))
		mean_fid_hlr=np.mean(np.array(fid_hlr))
		std_fid_hlr=np.std(np.array(fid_hlr))
		mean_fid_snr=np.mean(np.array(fid_snr))
		std_fid_snr=np.std(np.array(fid_snr))

		delta_e1=np.array(e1)-np.array(fid_e1)
		delta_e2=np.array(e2)-np.array(fid_e2)
		mean_de1=np.mean(delta_e1)
		mean_de2=np.mean(delta_e2)
		std_de1=np.std(delta_e1)
		std_de2=np.std(delta_e2)
		de1_dz4=np.mean(delta_e1)/6.465
		de2_dz4=np.mean(delta_e2)/6.465
		de1_dz4_std=np.std(delta_e1)/6.465
		de2_dz4_std=np.std(delta_e2)/6.465

		mean_e1=np.mean(np.array(e1))
		std_e1=np.std(np.array(e1))
		mean_e2=np.mean(np.array(e2))
		std_e2=np.std(np.array(e2))
		mean_hlr=np.mean(np.array(hlr))
		std_hlr=np.std(np.array(hlr))
		mean_snr=np.mean(np.array(snr))
		std_snr=np.std(np.array(snr))


		# mod1 = sm.OLS(e1,g1)
		# mod2 = sm.OLS(e2,g2)
		# res1 = mod1.fit()
		# res2 = mod2.fit()

		print('fid_e1='+str(mean_fid_e1)+'+-'+str(std_fid_e1))
		print('fid_e2='+str(mean_fid_e2)+'+-'+str(std_fid_e2))
		print('fid_psf_e1='+str(mean_fid_psf_e1)+'+-'+str(std_fid_psf_e1))
		print('fid_psf_e2='+str(mean_fid_psf_e2)+'+-'+str(std_fid_psf_e2))
		print('fid_psf_T='+str(mean_fid_psf_T)+'+-'+str(std_fid_psf_T))
		print('fid_hlr='+str(mean_fid_hlr)+'+-'+str(std_fid_hlr))
		print('fid_snr='+str(mean_fid_snr)+'+-'+str(std_fid_snr))
		print(self.dir_name+'_e1='+str(mean_e1)+'+-'+str(std_e1))
		print(self.dir_name+'_e2='+str(mean_e2)+'+-'+str(std_e2))
		print(self.dir_name+'_hlr='+str(mean_hlr)+'+-'+str(std_hlr))
		print(self.dir_name+'_snr='+str(mean_snr)+'+-'+str(std_snr))
		print(self.dir_name+'_de1='+str(mean_de1)+'+-'+str(std_de1))
		print(self.dir_name+'_de2='+str(mean_de2)+'+-'+str(std_de2))

		plt.hist(e1,bins=50)
		plt.ylabel('N')
		plt.xlabel('e1')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_e1')

		plt.hist(e2,bins=50)
		plt.ylabel('N')
		plt.xlabel('e2')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_e2')

		plt.hist(psf_e1,bins=200)
		plt.ylabel('N')
		plt.xlabel('PSF e1')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_psf_e1')

		plt.hist(psf_e2,bins=200)
		plt.ylabel('N')
		plt.xlabel('PSF e2')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_psf_e2')

		plt.hist(psf_T,bins=200)
		plt.ylabel('N')
		plt.xlabel('PSF FWHM(pix)')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_psf_fwhm')

		plt.hist(nexp_used,bins=np.arange(-1,14))
		plt.ylabel('N')
		plt.xlabel('Number of exposures')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_nexp')

		plt.hist(hlr,bins=np.arange(0,4,0.1))
		plt.ylabel('N')
		plt.xlabel('radius')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_hlr')

		snr=np.log10(np.array(snr)[np.array(snr).nonzero()[0]])
		plt.hist(snr,bins=200)
		plt.ylabel('N')
		plt.xlabel('log10(snr)')
		plt.savefig('/users/PCON0003/osu10670/wfirst_imsim/figures/hist_'+self.dir_name+'_snr')

path = sys.argv[1]
dir_name=sys.argv[2]
f = shape_results(path,dir_name)
f.results()