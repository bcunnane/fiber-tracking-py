import dti_fibers
import matplotlib.pyplot as plt
from scipy.io import loadmat
import pickle
import pydicom as dcm

# get DTI
dti_file = 'BC_DTI_N.mat'
name = dti_file[:-4]
dti = loadmat(dti_file)

data = dti_fibers.process_dti(name, dti['M'], dti['X'], dti['Y'], dti['FA'])

file = open(name, 'wb')
pickle.dump(data, file)
file.close()

# show result
# plt.imshow(dti['M'], cmap='gray')
# plt.plot(data.roi[:,0], data.roi[:,1], '-c')
# for i in range(0,len(data.fibers),2):
#     plt.plot(data.fibers[i:i+2,0], data.fibers[i:i+2,1], '-r')
# plt.show()

