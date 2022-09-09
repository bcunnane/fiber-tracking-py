import get_dti_fibers
import matplotlib.pyplot as plt 

# test
import scipy.io
file = 'BC_DTI_D.mat'
name = file[:-4]
dti = scipy.io.loadmat('BC_DTI_D.mat')
data = get_dti_fibers.main(name, dti['M'], dti['X'], dti['Y'], dti['FA'])

# show result
plt.imshow(dti['M'], cmap='gray')
plt.plot(data.roi[:,0], data.roi[:,1], '-c')
for i in range(0,len(data.fibers),2):
    plt.plot(data.fibers[i:i+2,0], data.fibers[i:i+2,1], '-r')
plt.show()


# clean up
# write test function
# try to understand how row comparison works