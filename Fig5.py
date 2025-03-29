# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 10:08:43 2025

@author: songchaoqing
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import seaborn as sns
from scipy import stats

df = pd.read_excel('C:/Users/songchaoqing/Desktop/plant_water_stress/3_site_species_theta_threshold.xlsx')

# read BRT result
BRT   = pd.read_csv('C:/Users/songchaoqing/Desktop/plant_water_stress/BRT_result/BRT_result.csv')
BRT_p = pd.read_excel('C:/Users/songchaoqing/Desktop/plant_water_stress/BRT_result/BRT_result_yhat.xlsx')

fig = plt.figure(figsize=(12,12))
plt.subplots_adjust(left=0.07,right=0.97,bottom=0.1,top=0.98,hspace=0.25,wspace=0.3)

############################################################################################################################################

name = ['swc_shal_gd','swc_shal_gt','swc_shal_od','swc_shal_ot']
xname = [r'SM$_\mathregular{gd}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',
         r'SM$_\mathregular{gt}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',
         r'SM$_\mathregular{od}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',
         r'SM$_\mathregular{ot}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)']
yname = [r'$\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)']

ax = [0.06,0.306667,0.55333,0.8]; height = [0.68,0.68,0.68,0.68]; axname = ['(a)','(b)','(c)','(d)']; psts = []
for kk in range(len(name)):
    slop,icpt,rval,pval,std_err = stats.linregress(df[name[kk]],df['swc_thr']); psts.append(pval)
    ax1 = fig.add_axes([ax[kk],height[kk],0.19,0.226])
    sns.regplot(x=df[name[kk]],y=df['swc_thr'],scatter_kws={'s':0},color=[50/255,50/255,220/255],
        ci=95,line_kws={'linewidth':1.5})
    plt.scatter(df[name[kk]],df['swc_thr'],32,facecolor='white',edgecolor=[173/255,173/255,173/255],linewidths=1)
    plt.plot((0,0.5),(0,0.5),'-.',color=[55/255,55/255,55/255],zorder=0)
    plt.xlim(0,0.5); plt.ylim(0,0.5)
    x_major_locator = MultipleLocator(0.2); ax1.xaxis.set_major_locator(x_major_locator)
    y_major_locator = MultipleLocator(0.2); ax1.yaxis.set_major_locator(y_major_locator)
    plt.xticks(fontsize=11); plt.yticks(fontsize=11)
    ax1.set_xlabel(xname[kk],fontdict={'size':11},labelpad=7)
    ax1.set_ylabel(yname[0],fontdict={'size':11},labelpad=7) if kk==0 else ax1.set_ylabel('')
    ax1.text(0.01,0.456,'S = '+str(round(slop,2))+', '+'$\it{R^{2}}$ = '+str(round(rval**2,2)),color='black',fontdict={'size':10})
    ax1.text(0.01,0.413,'$\it{p}$ < 0.001')
    ax1.text(-0.08,0.472,axname[kk],color='black',fontdict={'size':11},weight='bold')

############################################################################################################################################

col1=[45/255,138/255,86/255]; col2=[138/255,133/255,193/255]; col3=[200/255,86/255,202/255]; col4='orange'
col = [col1,col2,col2,col3,col2,col4,col1,col1,col1]
yname = [r'SM$_\mathregular{od}$','Stand height','Stand density','WD','Stand basal area','Sapwood area',
         r'VPD$_\mathregular{od}$',r'Precip$_\mathregular{od}$','Site_elev']
ax1 = fig.add_axes([0.13,0.165,0.28,0.42])
x = BRT['var'][:][::-1]; y = BRT['rel.inf'][:][::-1]
plt.barh(x,y,0.7,color=col[::-1])
ax1.set_ylim(-0.6,8.6); ax1.set_yticklabels([]); plt.xticks(fontsize=11); plt.yticks(fontsize=11)
x_major_locator = MultipleLocator(20); ax1.xaxis.set_major_locator(x_major_locator)
ax1.set_yticklabels(yname[::-1],fontdict={'size':11})
ax1.set_xlabel('Relative importance (%)',fontdict={'size':11},labelpad=8)
ax1.text(-15.2,8.36,'(e)',color='black',fontdict={'size':11},weight='bold')
ax1.text(30,0.3,'$\it{R^{2}}$ = '+str(0.92),color='black',fontdict={'size':11})

ax1 = fig.add_axes([0.23,0.25,0.15,0.15])
site  = BRT['rel.inf'][0]+BRT['rel.inf'][6]+BRT['rel.inf'][7]+BRT['rel.inf'][8]
stand = BRT['rel.inf'][1]+BRT['rel.inf'][2]+BRT['rel.inf'][4]
trait = BRT['rel.inf'][3]
plant = BRT['rel.inf'][5]
piedata = [site,stand,trait,plant]; labels=['Site','Stand','Trait','Plant']
plt.pie(piedata,labels=labels,colors=[col1,col2,col3,'orange'])

############################################################################################################################################

ax = [0.512,0.792,0.512,0.792,0.526]; height = [0.42,0.42,0.18,0.18,0.205]; nn = 0
xname = [r'SM$_\mathregular{od}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',
         'Stand height (m)','Stand density (stems $\mathregular{ha^{-1}}$)',
         'WD (g $\mathregular{cm^{-3}}$)','Stand basal area ($\mathregular{m^{2}}$ $\mathregular{ha^{-1}}$)']
         
col = [col1,col2,col2,col3]
for kk in range(0,8,2):
    xx = BRT_p.iloc[:,kk].dropna(); yy = BRT_p.iloc[:,kk+1].dropna()
    ax1 = fig.add_axes([ax[nn],height[nn],0.19,0.155])
    plt.plot(xx,yy,'-',color=col[nn],linewidth=1.8)
    
    plt.ylim(0.165,0.195)
    if nn==0: plt.ylim(0.07,0.35)
    if nn==0: x_major_locator = MultipleLocator(0.2); ax1.xaxis.set_major_locator(x_major_locator)
    if nn==0: ax1.text(-0.125,0.328,'(f)',color='black',fontdict={'size':11},weight='bold')
    if nn==1: ax1.text(-13.5,0.1926,'(g)',color='black',fontdict={'size':11},weight='bold')
    if nn==2: ax1.text(-2700,0.1926,'(h)',color='black',fontdict={'size':11},weight='bold')
    if nn==3: ax1.text(0.089,0.1926,'(i)',color='black',fontdict={'size':11},weight='bold')
    
    plt.xticks(fontsize=11); plt.yticks(fontsize=11)
    ax1.set_xlabel(xname[nn],fontdict={'size':11},labelpad=7,rotation=0)
    if nn==3: ax1.set_xlabel(xname[nn],fontdict={'size':11},labelpad=9,rotation=0)
    ax1.set_ylabel(r'$\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',fontdict={'size':11},labelpad=7)
    if nn==0: ax1.set_ylabel(r'$\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',fontdict={'size':11},labelpad=15)
    nn = nn + 1

plt.show()