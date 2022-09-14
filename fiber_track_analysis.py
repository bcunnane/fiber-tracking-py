import shelve
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.api import qqplot
import scipy.stats as stats
import pandas as pd


def unshelve_data():
    shelf_file = shelve.open('fiber-track-data-py')
    fiber_track_data = shelf_file['data']
    shelf_file.close()
    return fiber_track_data

# %% calculations
data = unshelve_data()

pix_spacing = 1.1719

rslt = {'force':data['force'], 'id':data['id'], 'mvc':data['mvc']}
dxs = data['xs'][:,1::2,:] - data['xs'][:,0::2,:] 
dys = data['ys'][:,1::2,:] - data['ys'][:,0::2,:]
rslt['lengths'] = ((dxs**2 + dys**2) ** .5) * pix_spacing
del_lens = rslt['lengths'] - rslt['lengths'][:,:,0][:,:,np.newaxis]
rslt['angles'] = np.cos(np.absolute(dys / rslt['lengths']))
rslt['strains'] = del_lens / rslt['lengths'][:,:,0][:,:,np.newaxis]
rslt['angles'] = np.degrees(rslt['angles'])

rslt['peak_strain'] = np.min(rslt['strains'], axis=2)
rslt['ps_idx'] = np.argmin(rslt['strains'], axis=2)

rslt['torque'] = rslt['force'] * data['ma'] * 0.001 # Nm
rslt['mvc_torque'] = rslt['mvc'] * data['ma'] * 0.001 # Nm
rslt['str/force'] = rslt['peak_strain'] / rslt['force'][:, np.newaxis]
rslt['str/torque'] = rslt['peak_strain'] / rslt['torque'][:, np.newaxis]

rslt['init_lens'] = rslt['lengths'][:,:,0]
rslt['init_angs'] = rslt['angles'][:,:,0]

rslt['final_lens'] = np.zeros((36,3))
rslt['final_angs'] = np.zeros((36,3))
for n in range(len(rslt['id'])):
    rslt['final_lens'][n,:] = rslt['lengths'][n,[0,1,2],rslt['ps_idx'][n,:]]
    rslt['final_angs'][n,:] = rslt['angles'][n,[0,1,2],rslt['ps_idx'][n,:]]

# %% normality check
fields = ['peak_strain','str/force','str/torque',
          'init_angs','final_angs','init_lens','final_lens']

p_sw = pd.DataFrame(['D50','N50','P50','D25','N25','P25'], columns=['case'])
p_sw = p_sw.set_index('case')

for field in fields:
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15,10))
    ax= axes.flatten()
    p_sw[field] = np.zeros(6)
    for c in range(6):
        # get case data
        rows = [i for i in range(c,36,6)]
        case_data = rslt[field][rows,:].flatten()
        
        # shaprio-wilks test p-value
        shapiro_rslt = stats.shapiro(case_data)
        p_sw[field][c] = shapiro_rslt.pvalue
        
        # qq plots
        qqplot(case_data, line='s',ax = ax[c])
        ax[c].title.set_text(p_sw.index[c])
    

