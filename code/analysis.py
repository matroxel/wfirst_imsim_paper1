import sys, os
from astropy.io import fits
import fitsio
import numpy as np
import treecorr
import matplotlib
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

	def __init__(self,path,file_name):

		self.path=path
		self.file_name=file_name

	def extract_shear(self):

		file=fits.open(self.path+'/'+self.file_name)
		shear=[]

		for i in file[1].data:
			e1=i[7]
			e2=i[8]
			g1=i[17]
			g2=i[18]
			shear.append([g1,g2,e1,e2])

		return shear

	def estimate_cfs(self,shear):

		A1 = np.vstack([shear[:,0], np.ones(len(shear[:,0]))]).T
		m1, c1 = np.linalg.lstsq(A1, shear[:,3], rcond=None)[0]
		m1 = m1-1
		A2 = np.vstack([shear[:,2], np.ones(len(shear[:,2]))]).T
		m2, c2 = np.linalg.lstsq(A2, e2, rcond=None)[0]
		m2 = m2-1

		return (m1,c1, m2, c2)

	def line_plot(self,m1,c1,m2,c2):

		x = np.zeros(100)
		for i in range(100):
			x[i]=0.01*i

		plt.plot(x,(1+m1)*x+c1,label="m1="+str(m1)+", c1="+str(c1))
		plt.plot(x,(1+m2)*x+c2,label="m2="+str(m2)+", c2="+str(c2))
		plt.plot(x,x,label="e=g")
		plt.legend(loc="upper left")
		plt.show()

class corr_func:
	def __init__(self,path,file_name):

		self.path=path
		self.file_name=file_name

	def extract_info(self):

		file=self.path+'/'+self.file_name
		file2=self.path.rstrip('ngmix')+'meds/'+self.file_name
		
		ra=fitsio.read(file,columns='ra')
		dec=fitsio.read(file,columns='dec')
		e1=fitsio.read(file,columns='e1')
		e2=fitsio.read(file,columns='e2')
		sca_x=fitsio.read(file2,columns='orig_col')
		sca_y=fitsio.read(file2,columns='orig_row')
		sca=fitsio.read(file2,columns='sca')

		focal_plane_x = []
		focal_plane_y =[]
		for i in range(len(sca)):
			for j in range(len(sca[i])):
				sca_to_plane=field_methods(sca[i][j],sca_x[i][j],sca_y[i][j])
				x, y=sca_to_plane.get_field_pos()
				focal_plane_x.append(x)
				focal_plane_y.append(y)

		return ra,dec,e1,e2,e1.repeat(len(sca[0])),e2.repeat(len(sca[0])),np.array(focal_plane_x),np.array(focal_plane_y)

	def xy_corr(self,x,y,g1,g2):
		cat = treecorr.Catalog(x=x, y=y, g1=g1, g2=g2)
		gg = treecorr.GGCorrelation(min_sep=0.1, max_sep=200, nbins=20)
		gg.process(cat)

		return gg

	def sky_corr(self,ra,dec,g1,g2):
		cat = treecorr.Catalog(ra=ra, dec=dec, g1=g1, g2=g2,ra_units='deg',dec_units='deg')
		gg = treecorr.GGCorrelation(min_sep=1, max_sep=400, nbins=20, sep_units='arcmin')
		gg.process(cat)

	def corr_plot(self,gg,file_name):
		r = np.exp(gg.meanlogr)
		xip = gg.xip
		xim = gg.xim
		sig = np.sqrt(gg.varxip)

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
		plt.xlabel(r'$d$(mm)')


		plt.legend([lp, lm], [r'$\xi_+(d)$', r'$\xi_-(d)$'])
		plt.xlim( [1,200] )
		plt.ylabel(r'$\xi_{+,-}$')
		plt.savefig(file_name)
		plt.show()

path = sys.argv[1]
files = os.listdir(path)
ra=dec=sky_e1=sky_e2=e1=e2=x=y=np.array([],dtype='>f8')

for file in files:
	print (file)
	corr=corr_func(path,file)
	ra_tmp,dec_tmp,e1_tmp,e2_tmp,e1_xy_tmp,e2_xy_tmp,x_tmp,y_tmp=corr.extract_info()
	ra = np.append(ra,ra_tmp)
	dec = np.append(dec,dec_tmp)
	sky_e1 = np.append(e1,e1_tmp)
	sky_e2 = np.append(e2,e2_tmp)
	e1 = np.append(e1,e1_xy_tmp)
	e2 = np.append(e2,e2_xy_tmp)
	x = np.append(x,x_tmp)
	y = np.append(y,y_tmp)
	


gg = corr.xy_corr(x,y,e1,e2)
corr.corr_plot(gg,'xy_corr'),

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






# ra_min = np.min(cat.ra)
# ra_max = np.max(cat.ra)
# dec_min = np.min(cat.dec)
# dec_max = numpy.max(cat.dec)
# print('ra range = %f .. %f' % (ra_min, ra_max))
# print('dec range = %f .. %f' % (dec_min, dec_max))




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






































