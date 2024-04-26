import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt


def fiber_cycle_plot(subject, del_angs, del_lens, strains):
    
    # average results for proximal, middle, and distal fibers
    del_lens = np.mean(del_lens, axis=1)
    del_angs = np.mean(del_angs, axis=1)
    strains = np.mean(strains, axis=1)
    
    # convert frames (22) to percent of cycle
    x = np.arange(0,100+(100/21),100/21) 
    
    # plot
    i = 1
    posn = 'D N P'
    posn_code = {'P':'PH', 'N':'PL', 'D':'D'}
    fig = plt.figure(figsize=(9,9))
    for p in [4,2,0]:
        
        # plot delta angle
        ax1 = fig.add_subplot(3,3,i)
        ax1.plot(x, del_angs[p,:], x, del_angs[p+1,:])
        ax1.set_xticks([0, 50, 100])
        ax1.set_xticklabels(['0%', '50%', '100%'])
        ax1.set_xlabel('% Contraction cycle')
        ax1.set_ylabel('\u0394 Fiber angle (\u00b0)')
        ax1.set_ylim((-5, 10))
        ax1.set_yticks([-5,0,5,10])
        ax1.text(.1, 8, posn_code[posn[p]], fontsize=14, weight='bold')
        if posn[p] == 'P':
            ax1.legend(("50% MVC", "25% MVC"))
        ax2 = ax1.twiny()
        ax2.set_xlabel('Time (s)')
        ax2.set_xticks([0, 1.5, 3])
        
        
        # plot delta lengths
        ax3 = fig.add_subplot(3,3,i+1)
        ax3.plot(x, del_lens[p,:], x, del_lens[p+1,:])
        ax3.set_xticks([0, 50, 100])
        ax3.set_xticklabels(['0%', '50%', '100%'])
        ax3.set_xlabel('% Contraction cycle')
        ax3.set_ylabel('\u0394 Fiber length (mm)')
        ax3.set_ylim((-15, 5))
        ax3.text(.1, 2.5, posn_code[posn[p]], fontsize=14, weight='bold')
        ax4 = ax3.twiny()
        ax4.set_xlabel('Time (s)')
        ax4.set_xticks([0, 1.5, 3])
        
        # plot strains
        ax5 = fig.add_subplot(3,3,i+2)
        ax5.plot(x, strains[p,:], x, strains[p+1,:])
        ax5.set_xticks([0, 50, 100])
        ax5.set_xticklabels(['0%', '50%', '100%'])
        ax5.set_xlabel('% Contraction cycle')
        ax5.set_ylabel('Fiber strain')
        ax5.set_ylim((-.4, .2))
        ax5.set_yticks([-0.4,-0.2,0,0.2])
        ax5.text(.1, 0.12, posn_code[posn[p]], fontsize=14, weight='bold')
        if posn[p] == 'N':
            ax5.text(11, 0.13, '*', fontsize=16)
        if posn[p] == 'D':
            ax5.text(8, 0.13, '*', fontsize=16)
        ax6 = ax5.twiny()
        ax6.set_xlabel('Time (s)')
        ax6.set_xticks([0, 1.5, 3])
        
        # start subplot index at next row
        i+=3
    
    # save plot as image
    plt.tight_layout()
    plt.savefig(subject, dpi=300)

# import all data
subject = 'Figure 3.png'
raw = loadmat('fig3.mat')['fig3'][0]

# get delta angles
del_angs = np.zeros((6,3,22))
for n in range(6):
    del_angs[n,:,:] = raw['del_angs'][n]

# get delta lengths
del_lens = np.zeros((6,3,22))
for n in range(6):
    del_lens[n,:,:] = raw['del_lens'][n]

# get strains
strains = np.zeros((6,3,22))
for n in range(6):
    strains[n,:,:] = raw['strains'][n]

# plot
fiber_cycle_plot(subject, del_angs, del_lens, strains)

