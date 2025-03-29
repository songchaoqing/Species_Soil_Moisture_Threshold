# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 11:40:12 2025

@author: songchaoqing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pyplot import MultipleLocator
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import scipy.stats as st
from scipy import stats

def ConcatData(StatsX):        
    DataX = StatsX[0]
    for xx in range(len(StatsX)):
        if (xx==len(StatsX)-1):
            break
        DataX = pd.concat([DataX,StatsX[xx+1]],axis=0)
    return DataX

#%% site-species information

inpath = 'C:/Users/songchaoqing/Desktop/plant_water_stress/compare/'
site_info = pd.read_excel(inpath+'sapflux_variable_stats.xlsx')
site_info_new = site_info[['site','species','sp','ta','vpd','precip','sw_in','netrad','swc_shallow']]

df1    = pd.read_csv(inpath+'1_extracted_vs_observed_SM.csv')
r1comp = [df1['r_e5h'][0:],df1['r_e5l'][0:],df1['r_gleam'][0:],df1['r_glass'][0:],df1['r_esa'][0:]]
r1comp_result = ConcatData(r1comp); r1comp_result.index = np.arange(0,len(r1comp_result)); r1comp_result = list(r1comp_result)
df1a = pd.DataFrame({'score': r1comp_result,'group': np.repeat(['a','b','c','d','e'], repeats=len(df1))})
df1new = df1a.dropna(axis=0,how='any',subset=['score'])
tukey_r1comp = pairwise_tukeyhsd(endog=df1new['score'],groups=df1new['group'],alpha=0.05)
print(tukey_r1comp)

groups1 = sorted(df1new["group"].unique())
y_data1 = [df1new[df1new["group"]==group]["score"].values for group in groups1]
jitter1 = 0.04
x_data1 = [np.array([i] * len(d)) for i, d in enumerate(y_data1)]
x_jittered1 = [x + st.t(df=6, scale=jitter1).rvs(len(x)) for x in x_data1]

#%%

df2a = pd.read_csv('C:/Users/songchaoqing/Desktop/plant_water_stress/2_linear_regress_grow.csv')
df2b = pd.read_csv(inpath+'2_extracted_variables_Td_simple_regress.csv')
df2  = pd.merge(df2a,df2b,how='left',on=['site','Es_var'])
df2new = df2.copy(); df2new = df2new.drop([73]).reset_index(drop=True)

df_SR = pd.merge(df2new,site_info_new,on=['site','sp'],how='left'); df_SR_new = df_SR[df_SR['sw_in']>=1]
df_SR_del = df_SR[~(df_SR['site'].isin(df_SR_new['site']) & df_SR['sp'].isin(df_SR_new['sp']))]
df_SR_del.index = np.arange(0,len(df_SR_del))

# observed SM-based R
df2new1 = df2new[['site','Es_var','r_swc','r_vpd','r_sw','r_ta']]; df2new1['type'] = 'obs'
# ERA5
df2new2 = df2new[['site','Es_var','r_e5h_swc','r_e5h_vpd','r_e5h_sw','r_e5h_ta']]; df2new2['type'] = 'ERA5'
df2new2.rename(columns={'r_e5h_swc':'r_swc','r_e5h_vpd':'r_vpd','r_e5h_sw':'r_sw','r_e5h_ta':'r_ta'},inplace=True)
# ERA5-land
df2new3 = df2new[['site','Es_var','r_e5l_swc','r_e5l_vpd','r_e5l_sw','r_e5l_ta']]; df2new3['type'] = 'ERA5-Land'
df2new3.rename(columns={'r_e5l_swc':'r_swc','r_e5l_vpd':'r_vpd','r_e5l_sw':'r_sw','r_e5l_ta':'r_ta'},inplace=True)

#########################################################comparison#############################################################

r_swc = [df2new['r_swc'][0:],df2new['r_e5h_swc'][0:],df2new['r_e5l_swc'][0:]]
r_swc_result = ConcatData(r_swc); r_swc_result.index = np.arange(0,len(r_swc_result)); r_swc_result = list(r_swc_result)
r_swc_new = pd.DataFrame({'score': r_swc_result,'group': np.repeat(['a','b','c'], repeats=len(df2new))})
r_swc_new1 = r_swc_new.dropna(axis=0,how='any',subset=['score'])
tukey_r_swc = pairwise_tukeyhsd(endog=r_swc_new1['score'],groups=r_swc_new1['group'],alpha=0.05)
print(tukey_r_swc)

r_vpd = [df2new['r_vpd'][0:],df2new['r_e5h_vpd'][0:],df2new['r_e5l_vpd'][0:]]
r_vpd_result = ConcatData(r_vpd); r_vpd_result.index = np.arange(0,len(r_vpd_result)); r_vpd_result = list(r_vpd_result)
r_vpd_new = pd.DataFrame({'score': r_vpd_result,'group': np.repeat(['a','b','c'], repeats=len(df2new))})
r_vpd_new1 = r_vpd_new.dropna(axis=0,how='any',subset=['score'])
tukey_r_vpd = pairwise_tukeyhsd(endog=r_vpd_new1['score'],groups=r_vpd_new1['group'],alpha=0.05)
print(tukey_r_vpd)

r_sw = [df_SR_new['r_sw'][0:],df_SR_new['r_e5h_sw'][0:],df_SR_new['r_e5l_sw'][0:]]
r_sw_result = ConcatData(r_sw); r_sw_result.index = np.arange(0,len(r_sw_result)); r_sw_result = list(r_sw_result)
r_sw_new = pd.DataFrame({'score': r_sw_result,'group': np.repeat(['a','b','c'], repeats=len(df_SR_new))})
r_sw_new1 = r_sw_new.dropna(axis=0,how='any',subset=['score'])
tukey_r_sw = pairwise_tukeyhsd(endog=r_sw_new1['score'],groups=r_sw_new1['group'],alpha=0.05)
print(tukey_r_sw)

r_ta = [df2new['r_ta'][0:],df2new['r_e5h_ta'][0:],df2new['r_e5l_ta'][0:]]
r_ta_result = ConcatData(r_ta); r_ta_result.index = np.arange(0,len(r_ta_result)); r_ta_result = list(r_ta_result)
r_ta_new = pd.DataFrame({'score': r_ta_result,'group': np.repeat(['a','b','c'], repeats=len(df2new))})
r_ta_new1 = r_ta_new.dropna(axis=0,how='any',subset=['score'])
tukey_r_ta = pairwise_tukeyhsd(endog=r_ta_new1['score'],groups=r_ta_new1['group'],alpha=0.05)
print(tukey_r_ta)

var = ['r_swc','r_vpd','r_sw','r_ta']; dataU0 = []; dataU1 = []; dataU2 = []
for ii in range(len(var)):
    data1 = df2new1[['site','Es_var',var[ii],'type']]; data1['var'] = var[ii]
    data1.rename(columns={var[ii]:'r_val'},inplace=True)
    data2 = df2new2[['site','Es_var',var[ii],'type']]; data2['var'] = var[ii]
    data2.rename(columns={var[ii]:'r_val'},inplace=True)
    data3 = df2new3[['site','Es_var',var[ii],'type']]; data3['var'] = var[ii]
    data3.rename(columns={var[ii]:'r_val'},inplace=True)
    if ii==2:
        data1 = data1[~(data1['site'].isin(df_SR_del['site']) & data1['Es_var'].isin(df_SR_del['Es_var']))]
        data2 = data2[~(data2['site'].isin(df_SR_del['site']) & data2['Es_var'].isin(df_SR_del['Es_var']))]
        data3 = data3[~(data3['site'].isin(df_SR_del['site']) & data3['Es_var'].isin(df_SR_del['Es_var']))]
        
    dataU1.append(data1); dataU1.append(data2)
    dataU2.append(data1); dataU2.append(data3)
    dataU0.append(data1); dataU0.append(data2); dataU0.append(data1); dataU0.append(data3)

datanew0 = ConcatData(dataU0); datanew0.index = np.arange(0,len(datanew0))
datanew1 = ConcatData(dataU1); datanew1.index = np.arange(0,len(datanew1))
datanew2 = ConcatData(dataU2); datanew2.index = np.arange(0,len(datanew2))
datanew3 = datanew2.copy(); datanew4 = datanew1.copy(); datanew5 = datanew1.copy()
datanew3['r_val'][datanew3['type']=='obs']=np.nan
datanew4['r_val'][datanew4['type']=='obs']=np.nan
datanew5['r_val'][datanew5['type']=='ERA5']=np.nan

#%%

theta1 = pd.read_excel(inpath+'3_extracted_vs_observed_theta.xlsx',sheet_name='obs_era5')
theta2 = pd.read_excel(inpath+'3_extracted_vs_observed_theta.xlsx',sheet_name='obs_era5l')
theta3 = pd.read_excel(inpath+'3_extracted_vs_observed_theta.xlsx',sheet_name='obs_gleam')
theta4 = pd.read_excel(inpath+'3_extracted_vs_observed_theta.xlsx',sheet_name='obs_glass')
theta5 = pd.read_excel(inpath+'3_extracted_vs_observed_theta.xlsx',sheet_name='obs_esa')

slop_e5h,icpt_e5h,rval_e5h,pval_e5h,std_err_e5h           = stats.linregress(theta1['swc_thr_obs'],theta1['swc_thr_era5'])
slop_e5l,icpt_e5l,rval_e5l,pval_e5l,std_err_e5l           = stats.linregress(theta2['swc_thr_obs'],theta2['swc_thr_era5l'])
slop_gleam,icpt_gleam,rval_gleam,pval_gleam,std_err_gleam = stats.linregress(theta3['swc_thr_obs'],theta3['swc_thr_gleam'])
slop_glass,icpt_glass,rval_glass,pval_glass,std_err_glass = stats.linregress(theta4['swc_thr_obs'],theta4['swc_thr_glass'])
slop_esa,icpt_esa,rval_esa,pval_esa,std_err_esa           = stats.linregress(theta5['swc_thr_obs'],theta5['swc_thr_esa'])
R2   = [rval_e5h**2,rval_e5l**2,rval_gleam**2,rval_glass**2,rval_esa**2]
pval = [pval_e5h,pval_e5l,pval_gleam,pval_glass,pval_esa]
slop = [slop_e5h,slop_e5l,slop_gleam,slop_glass,slop_esa]

RMSE_e5h    = np.sqrt(((theta1['swc_thr_obs']-theta1['swc_thr_era5'])**2).mean())
RMSE_e5l    = np.sqrt(((theta2['swc_thr_obs']-theta2['swc_thr_era5l'])**2).mean())
RMSE_gleam  = np.sqrt(((theta3['swc_thr_obs']-theta3['swc_thr_gleam'])**2).mean())
RMSE_glass  = np.sqrt(((theta4['swc_thr_obs']-theta4['swc_thr_glass'])**2).mean())
RMSE_esa    = np.sqrt(((theta5['swc_thr_obs']-theta5['swc_thr_esa'])**2).mean())
RMSE = [RMSE_e5h,RMSE_e5l,RMSE_gleam,RMSE_glass,RMSE_esa]

RPE_e5h   = (theta1['swc_thr_era5'].mean()-theta1['swc_thr_obs'].mean())/theta1['swc_thr_obs'].mean()*100
RPE_e5l   = (theta2['swc_thr_era5l'].mean()-theta2['swc_thr_obs'].mean())/theta2['swc_thr_obs'].mean()*100
RPE_gleam = (theta3['swc_thr_gleam'].mean()-theta3['swc_thr_obs'].mean())/theta3['swc_thr_obs'].mean()*100
RPE_glass = (theta4['swc_thr_glass'].mean()-theta4['swc_thr_obs'].mean())/theta4['swc_thr_obs'].mean()*100
RPE_esa   = (theta5['swc_thr_esa'].mean()-theta5['swc_thr_obs'].mean())/theta5['swc_thr_obs'].mean()*100
RPE = [RPE_e5h,RPE_e5l,RPE_gleam,RPE_glass,RPE_esa]

#%% Plot

x_ticks1=['ERA5','ERA5-Land','GLEAM4','GLASS','ESA-CCI']
x_ticks2=['SM-Td','VPD-Td','SR-Td','Ta-Td']
color1 = [205/255,120/255,144/255]
medianprops1 = dict(linewidth=2.7,color=color1,solid_capstyle="butt")
boxprops1    = dict(linewidth=1.2,color=color1)
aa = 0.003; size=40; col1 = [167/255,167/255,167/255]
col2 = [[235/255,46/255,46/255],[65/255,65/255,237/255],[20/255,168/255,20/255],[237/255,169/255,44/255],[170/255,23/255,170/255]]

fig = plt.figure(figsize=(12,6))

ax1 = fig.add_axes([0.07-aa,0.56,0.42,0.33])
sns.violinplot(r1comp,bw_adjust=.8,cut=0,linewidth=1,palette=col2,
               fill=False,inner='box',inner_kws=dict(box_width=7, whis_width=2))
plt.xticks(fontsize=11); plt.yticks(fontsize=11); plt.ylim(-1,1.25)
y_major_locator = MultipleLocator(0.5); ax1.yaxis.set_major_locator(y_major_locator)
ax1.set_xticklabels(x_ticks1)
ax1.set_ylabel(r'$R$',fontdict={'size':11},labelpad=5)
ax1.text(-0.1,1.07,'ab',color='black',fontdict={'size':11})
ax1.text(0.95,1.07,'b',color='black',fontdict={'size':11})
ax1.text(1.95,1.07,'a',color='black',fontdict={'size':11})
ax1.text(2.91,1.07,'ac',color='black',fontdict={'size':11})
ax1.text(3.96,1.07,'c',color='black',fontdict={'size':11})
ax1.text(-1.24,1.11,'(a)',weight='bold',color='black',fontdict={'size':11})

c1 = [235/255,46/255,46/255]; c2 = [65/255,65/255,237/255]; c3 = [167/255,167/255,167/255]
ax2 = fig.add_axes([0.582-aa,0.56,0.413,0.33])
sns.violinplot(data=datanew5,x='var',y='r_val',hue='type',split=True,fill=False,gap=0.1,inner='box',
               inner_kws=dict(box_width=5,whis_width=1),
               palette={'obs':c3,'ERA5':c1},bw_adjust=.8,cut=0,width=0.9,legend=False)
sns.violinplot(data=datanew4,x='var',y='r_val',hue='type',split=True,fill=False,gap=0.1,inner='quart',
               palette={'obs':c3,'ERA5':c1},bw_adjust=.8,cut=0,width=0.9,legend=False)
sns.violinplot(data=datanew3,x='var',y='r_val',hue='type',split=True,fill=False,gap=0.1,inner='quart',
               palette={'obs':c3,'ERA5-Land':c2},bw_adjust=.8,cut=0,width=0.9,legend=False) 
plt.xticks(fontsize=11); plt.yticks(fontsize=11); plt.ylim(-1,1.2)
y_major_locator = MultipleLocator(0.5); ax2.yaxis.set_major_locator(y_major_locator)
ax2.set_xticklabels(x_ticks2)
ax2.set_xlabel(' '); ax2.set_ylabel(r'$R$',fontdict={'size':11},labelpad=5)
ax2.text(-0.09,1.02,'a', color=c3,fontdict={'size':11})
ax2.text(0.01, 1.02,'b', color=c1,fontdict={'size':11})
ax2.text(0.10, 1.02,'b', color=c2,fontdict={'size':11})
ax2.text(0.91, 1.02,'a', color=c3,fontdict={'size':11})
ax2.text(1.01, 1.02,'a', color=c1,fontdict={'size':11})
ax2.text(1.11, 1.02,'a', color=c2,fontdict={'size':11})
ax2.text(1.91, 1.02,'a', color=c3,fontdict={'size':11})
ax2.text(2.01, 1.02,'b', color=c1,fontdict={'size':11})
ax2.text(2.11, 1.02,'ab',color=c2,fontdict={'size':11})
ax2.text(2.91, 1.02,'a', color=c3,fontdict={'size':11})
ax2.text(3.01, 1.02,'a', color=c1,fontdict={'size':11})
ax2.text(3.11, 1.02,'a', color=c2,fontdict={'size':11})
ax2.text(-1.1,1.05,'(b)',weight='bold',color='black',fontdict={'size':11})

ax2 = fig.add_axes([0.946,0.61,0,0])
sns.violinplot(data=datanew0,x='var',y='r_val',hue='type',split=False,fill=False,gap=0.2,
               inner_kws=dict(box_width=5,whis_width=1),palette={'obs':c3,'ERA5':c1,'ERA5-Land':c2})
ax2.set_xlabel(' '); ax2.set_ylabel(' '); plt.xticks(()); plt.yticks(())
ax2.legend(bbox_to_anchor=(1.6,1),loc='upper right',ncol=3,fontsize=10,frameon=False,
           handletextpad=0.2,handlelength=2,handleheight=0.8,columnspacing=0.9)

ax3 = fig.add_axes([0.07-aa,0.14,0.145,0.29])
plt.scatter(theta1['swc_thr_era5'],theta1['swc_thr_obs'],size,facecolor='white',edgecolor=col1,linewidths=1)
plt.plot((0,0.5),(0,0.5),'-.',color=[55/255,55/255,55/255],zorder=0)
plt.xlim(0,0.5); plt.ylim(0,0.5); plt.xticks(fontsize=11); plt.yticks(fontsize=11)
x_major_locator = MultipleLocator(0.2); ax3.xaxis.set_major_locator(x_major_locator)
y_major_locator = MultipleLocator(0.2); ax3.yaxis.set_major_locator(y_major_locator)
ax3.set_xlabel(r'ERA5 $\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',fontdict={'size':11},labelpad=9)
ax3.set_ylabel(r'$\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',fontdict={'size':11},labelpad=14)
ax3.text(-0.213,0.465,'(c)',weight='bold',color='black',fontdict={'size':11})
ax3.text(0.009,0.52,'$\it{R^{2}}$ = '+str(round(R2[0],2))+', '+'RMSE = '+str(round(RMSE[0],2)),color='black',fontdict={'size':10})

ax3 = fig.add_axes([0.265-aa,0.14,0.145,0.29])
plt.scatter(theta2['swc_thr_era5l'],theta2['swc_thr_obs'],size,facecolor='white',edgecolor=col1,linewidths=1)
plt.plot((0,0.5),(0,0.5),'-.',color=[55/255,55/255,55/255],zorder=0)
plt.xlim(0,0.5); plt.ylim(0,0.5); plt.xticks(fontsize=11); plt.yticks(fontsize=11)
x_major_locator = MultipleLocator(0.2); ax3.xaxis.set_major_locator(x_major_locator)
y_major_locator = MultipleLocator(0.2); ax3.yaxis.set_major_locator(y_major_locator)
ax3.set_xlabel(r'ERA5-Land $\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',fontdict={'size':11},labelpad=9)
ax3.text(0.009,0.52,'$\it{R^{2}}$ = '+str(round(R2[1],2))+', '+'RMSE = '+str(round(RMSE[1],2)),color='black',fontdict={'size':10})

ax3 = fig.add_axes([0.46-aa,0.14,0.145,0.29])
plt.scatter(theta3['swc_thr_gleam'],theta3['swc_thr_obs'],size,facecolor='white',edgecolor=col1,linewidths=1)
plt.plot((0,0.5),(0,0.5),'-.',color=[55/255,55/255,55/255],zorder=0)
plt.xlim(0,0.5); plt.ylim(0,0.5); plt.xticks(fontsize=11); plt.yticks(fontsize=11)
x_major_locator = MultipleLocator(0.2); ax3.xaxis.set_major_locator(x_major_locator)
y_major_locator = MultipleLocator(0.2); ax3.yaxis.set_major_locator(y_major_locator)
ax3.set_xlabel(r'GLEAM4 $\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',fontdict={'size':11},labelpad=9)
ax3.text(0.009,0.52,'$\it{R^{2}}$ = '+str(round(R2[2],2))+', '+'RMSE = '+str(round(RMSE[2],2)),color='black',fontdict={'size':10})

ax3 = fig.add_axes([0.655-aa,0.14,0.145,0.29])
plt.scatter(theta4['swc_thr_glass'],theta4['swc_thr_obs'],size,facecolor='white',edgecolor=col1,linewidths=1)
plt.plot((0,0.5),(0,0.5),'-.',color=[55/255,55/255,55/255],zorder=0)
plt.xlim(0,0.5); plt.ylim(0,0.5); plt.xticks(fontsize=11); plt.yticks(fontsize=11)
x_major_locator = MultipleLocator(0.2); ax3.xaxis.set_major_locator(x_major_locator)
y_major_locator = MultipleLocator(0.2); ax3.yaxis.set_major_locator(y_major_locator)
ax3.set_xlabel(r'GLASS $\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',fontdict={'size':11},labelpad=9)
ax3.text(0.021,0.52,'$\it{R^{2}}$ = '+str(round(R2[3],2))+', '+'RMSE = '+str(round(RMSE[3],2)),color='black',fontdict={'size':10})

ax3 = fig.add_axes([0.85-aa,0.14,0.145,0.29])
plt.scatter(theta5['swc_thr_esa'],theta5['swc_thr_obs'],size,facecolor='white',edgecolor=col1,linewidths=1)
plt.plot((0,0.5),(0,0.5),'-.',color=[55/255,55/255,55/255],zorder=0)
plt.xlim(0,0.5); plt.ylim(0,0.5); plt.xticks(fontsize=11); plt.yticks(fontsize=11)
x_major_locator = MultipleLocator(0.2); ax3.xaxis.set_major_locator(x_major_locator)
y_major_locator = MultipleLocator(0.2); ax3.yaxis.set_major_locator(y_major_locator)
ax3.set_xlabel(r'ESA-CCI $\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',fontdict={'size':11},labelpad=9)
ax3.text(0.009,0.52,'$\it{R^{2}}$ = '+str(round(R2[4],2))+', '+'RMSE = '+str(round(RMSE[4],2)),color='black',fontdict={'size':10})

plt.show()
