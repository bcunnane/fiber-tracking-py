import numpy as np
from scipy.io import loadmat

# %% Get data
# initialize
data = {
        'id':[],
        'force':np.zeros(36),
        'mvc':np.zeros(36),
        'pct':np.zeros(36),
        'loc':np.zeros(36),
        'slice':np.zeros(36),
        'mag':np.zeros((36,256,256,22)),
        'fibers':np.zeros((36,6,2)),
        'xs':np.zeros((36,6,22)),
        'ys':np.zeros((36,6,22)),
        'ma':np.zeros(36)
}

# process fiber-track mat file
mat = loadmat('all_data_with_ma.mat')
for i in range(36):
    data['id'].append(str(mat['data']['ID'][0][i][0]))
    data['force'][i] = np.amax(mat['data']['mean'][0][i][0])
    data['mvc'][i] = mat['data']['MVC'][0][i][0][0]
    data['pct'][i] = mat['data']['pcent'][0][i][0][0]
    data['loc'][i] = mat['data']['loc'][0][i][0][0]
    data['slice'][i] = mat['data']['slice'][0][i][0][0]
    data['mag'][i,:,:,:] = mat['data']['M'][0][i]
    data['fibers'][i,:,:] = mat['data']['fibers'][0][i]
    data['xs'][i,:,:] = mat['data']['xs'][0][i]
    data['ys'][i,:,:] = mat['data']['ys'][0][i]
    data['ma'][i] = mat['data']['ma'][0][i][0][0]

