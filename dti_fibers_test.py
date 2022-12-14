import dti_fibers
import matplotlib.pyplot as plt
from scipy.io import loadmat


# test
file = 'BC_DTI_D.mat'
name = file[:-4]
dti = loadmat('BC_DTI_D.mat')
data = dti_fibers.process_dti(name, dti['M'], dti['X'], dti['Y'], dti['FA'])

# show result
plt.imshow(dti['M'], cmap='gray')
plt.plot(data.roi[:,0], data.roi[:,1], '-c')
for i in range(0,len(data.fibers),2):
    plt.plot(data.fibers[i:i+2,0], data.fibers[i:i+2,1], '-r')
plt.show()

