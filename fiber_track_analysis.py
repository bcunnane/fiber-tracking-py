import shelve
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as stats
from statsmodels.formula.api import ols


def import_data():
    # unshelve raw data
    shelf_file = shelve.open('fiber-track-data-py')
    data = shelf_file['data']
    shelf_file.close()
    
    # change in fiber endpoint position
    dxs = data['xs'][:,1::2,:] - data['xs'][:,0::2,:]
    dys = data['ys'][:,1::2,:] - data['ys'][:,0::2,:]
    
    # fiber lengths (lens)
    pix_spacing = 1.1719 #mm/pixel
    data['lens'] = ((dxs**2 + dys**2) ** .5) * pix_spacing
    del_lens = data['lens'] - data['lens'][:,:,0][:,:,None]
    
    # fiber strains and peak strain (ps) index
    data['strains'] = del_lens / data['lens'][:,:,0][:,:,None]
    data['ps_idx'] = np.argmin(data['strains'], axis=2)
    
    # fiber pennation angles (angs, to +y axis in image)
    data['angs'] = np.cos(np.absolute(dys / data['lens']))
    data['angs'] = np.degrees(data['angs'])
    
    # torque (force * moment arm, ma)
    data['torque'] = data['force'] * data['ma'] * 0.001 # Nm
    data['mvc_torque'] = data['mvc'] * data['ma'] * 0.001 # Nm
    
    return data


def interpret_data(data):
    # strain and normalized strain
    peak_str = np.min(data['strains'], axis=2)
    str_force = peak_str / data['force'][:, None]
    str_torque = peak_str / data['torque'][:, None]
    
    # fiber at rest
    init_lens = data['lens'][:,:,0]
    init_angs = data['angs'][:,:,0]
    
    # fiber at peak contraction
    final_lens = np.zeros((36,3))
    final_angs = np.zeros((36,3))
    for n in range(len(data['id'])):
        final_lens[n,:] = data['lens'][n,[0,1,2],data['ps_idx'][n,:]]
        final_angs[n,:] = data['angs'][n,[0,1,2],data['ps_idx'][n,:]]
    
    # collect results into data frame
    rslt = pd.DataFrame({
        'posn' : list('DDDDDDNNNNNNPPPPPP' * 6),
        'pct_mvc':np.tile([50,50,50,25,25,25],(18,)),
        'peak_str':peak_str.flatten(),
        'str_force':str_force.flatten(),
        'str_torque':str_torque.flatten(),
        'init_lens':init_lens.flatten(),
        'final_lens':final_lens.flatten(),
        'init_angs':init_angs.flatten(),
        'final_angs':final_angs.flatten(),
        })
    return rslt


def check_normality(rslt):
    
    p_sw = pd.DataFrame({'case':['D50','N50','P50','D25','N25','P25']})
    
    for field in rslt.columns[2:]:
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15,10))
        ax= axes.flatten()
        p_sw[field] = np.zeros(6)
        c = 0
        for pn in 'DNP':
            for mvc in [50,25]:
            # get c data
                case_idx = (rslt['posn']==pn) & (rslt['pct_mvc']==mvc)
                case_data = rslt[field][case_idx]
                
                # shaprio-wilks test p-value
                shapiro_rslt = stats.shapiro(case_data)
                p_sw.loc[c, field] = shapiro_rslt.pvalue
                
                # qq plots
                sm.qqplot(case_data, line='s',ax = ax[c])
                ax[c].title.set_text(p_sw.loc[c, 'case'])
                c += 1
    return p_sw


def stats_norm(rslt):

    p_norm = pd.DataFrame(index=['C(posn)','C(pct_mvc)',
                                 'C(posn):C(pct_mvc)',
                                 't_dn', 't_np', 't_dp'])
    
    for field in rslt.columns[2:5]:
        # two-way anova p-values
        model = ols(field + '~ C(posn) + C(pct_mvc) + C(posn):C(pct_mvc)',\
                    data=rslt).fit()
        anova = sm.stats.anova_lm(model, type=2)
        p_norm.loc[:p_norm.index[2], field] = \
            anova.loc[:p_norm.index[2],'PR(>F)']
        
        # collect positional data for the field
        D = rslt.loc[rslt['posn']=='D', field]
        N = rslt.loc[rslt['posn']=='N', field]
        P = rslt.loc[rslt['posn']=='P', field]
        
        # get paired t-tests p-values
        p_norm.loc['t_dn',field] = stats.ttest_rel(D, N).pvalue
        p_norm.loc['t_np',field] = stats.ttest_rel(N, P).pvalue
        p_norm.loc['t_dp',field] = stats.ttest_rel(D, P).pvalue
        
    return p_norm
    

def stats_nonorm(rslt):
    
    p_nonorm = pd.DataFrame(index=['ang_dn_mw','ang_np_mw','ang_dp_mw',
                                   'ang_dn_kw','ang_np_kw','ang_dp_kw',
                                   'mvc_mw',])
    
    for field in rslt.columns[5:]:
        
        # collect positional data for the field
        D = rslt.loc[rslt['posn']=='D', field]
        N = rslt.loc[rslt['posn']=='N', field]
        P = rslt.loc[rslt['posn']=='P', field]
        
        # collect exertion level data for the field
        mvc50 = rslt.loc[rslt['pct_mvc']==50, field]
        mvc25 = rslt.loc[rslt['pct_mvc']==25, field]
        
        # Ankle angles using Mann-Whitney
        _, p_nonorm.loc['ang_dn_mw',field] = stats.mannwhitneyu(D, N)
        _, p_nonorm.loc['ang_np_mw',field] = stats.mannwhitneyu(N, P)
        _, p_nonorm.loc['ang_dp_mw',field] = stats.mannwhitneyu(D, P)
        
        # Ankle Angles using Kruskal-Wallis
        p_nonorm.loc['ang_dn_kw',field] = stats.kruskal(D, N).pvalue
        p_nonorm.loc['ang_np_kw',field] = stats.kruskal(N, P).pvalue
        p_nonorm.loc['ang_dp_kw',field] = stats.kruskal(D, P).pvalue
        
        # 25% vs 50% MVC using Mann-Whitney (aka Wilcoxon Rank Sum)
        _, p_nonorm.loc['mvc_mw',field] = stats.mannwhitneyu(mvc50, mvc25)
        
    return p_nonorm


def stats_mvc(mvc):
    
    p_mvc = {}
    
    # remove duplicate MVC values (same MVC for 25% & 50% data)
    mvc = mvc[::2]
    
    # sort MVC data by positions D, N, P
    D = mvc[0::3]
    N = mvc[1::3]
    P = mvc[2::3]
    
    # paired t-tests between MVC data of ankle positions
    p_mvc['DN'] = stats.ttest_rel(D, N).pvalue
    p_mvc['NP'] = stats.ttest_rel(N, P).pvalue
    p_mvc['DP'] = stats.ttest_rel(D, P).pvalue
    
    return p_mvc


#def main():
data = import_data()
rslt = interpret_data(data)
#p_sw = check_normality(rslt)
#p_norm = stats_norm(rslt)
#p_nonorm = stats_nonorm(rslt)
#p_mvc = stats_mvc(data['mvc'])





