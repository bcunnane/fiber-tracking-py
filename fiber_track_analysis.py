import shelve
import numpy as np
import pandas as pd


def import_data():
    shelf_file = shelve.open('fiber-track-data-py')
    fiber_track_data = shelf_file['data']
    shelf_file.close()
    return fiber_track_data


data = import_data()

pix_spacing = 1.1719

dxs = data['xs'][:,1::2,:] - data['xs'][:,0::2,:] 
dys = data['ys'][:,1::2,:] - data['ys'][:,0::2,:]
data['lengths'] = (dxs**2 + dys**2) ** .5
data['angles'] = np.cos(np.absolute(dys / data['lengths']))
data['angles'] = np.degrees(data['angles'])
data['del_lens'] = data['lengths'] - data['lengths'][:,:,0][:,:,np.newaxis]
data['del_angs'] = data['angles'] - data['angles'][:,:,0][:,:,np.newaxis]
data['strains'] = data['del_lens'] / data['lengths'][:,:,0][:,:,np.newaxis]
