# -*- coding: utf-8 -*-
"""
determines the foot angle and moment arm of large FOV DICOM images
"""

import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt


def show_fa(ims, pts, fas):
    # compbine P, N, and D images into single image
    ims = np.concatenate((ims[2,:,:], ims[1,:,:], ims[0,:,:]),axis=1)
    
    # plot images with ankle angle lines and text
    plt.imshow(ims, cmap='gray')
    pts = np.flip(pts,0)
    fas = np.flip(fas)
    for i in range(3):
        plt.plot(pts[i,:,0] + (255*i), pts[i,:,1], '-w', linewidth=0.75)
        plt.text(pts[i,1,0] + 255*i + 8, pts[i,1,1], str(fas[i]) + '\u00b0', color='w', fontsize=8)
        plt.text(255*i + 20, 250, ['PH', 'PL', 'D'][i], color='w', fontsize=8)
    
    # save figure
    plt.axis('off')
    plt.savefig('foot angles.png', dpi=300, bbox_inches='tight', pad_inches=0)




# import original matlab data
og_data = r'C:\Users\Brandon\Google Drive\research\fiber_tracking\foot position\foot position data.mat'
mat = loadmat(og_data)

ft = {
      'name':[],
      'im':np.zeros((18,256,256)),
      'fa_pts':np.zeros((18,3,2)),
      'fa':np.zeros(18, dtype=int)}


for i in range(18):
    ft['name'].append(str(mat['ft']['name'][0][i][0]))
    ft['im'][i,:,:] = mat['ft']['im'][0][i]
    ft['fa_pts'][i,:,:] = mat['ft']['fa_pts'][0][i]
    ft['fa'][i] = mat['ft']['fa'][0][i][0][0]

# change BC-P toe point to keep in frame
ft['fa_pts'][14,2,:] = (133,255)


show_fa(ft['im'][12:15,:,:], ft['fa_pts'][12:15,:,:], ft['fa'][12:15])
