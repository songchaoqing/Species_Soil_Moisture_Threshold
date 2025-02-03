# -*- coding: utf-8 -*-
"""

@author: SY
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

inpath = 'C:/Users/Desktop/'; outpath = 'C:/Users/Desktop/'
infile = inpath + '2_linear_regress_grow.csv'
infile1 = inpath + '2_multi_linear_regress_grow.csv'
df = pd.read_csv(infile); df_multi1 = pd.read_csv(infile1)

#%% univariate regression

df_swc_vpd_1 = df[(df['p_swc']<0.05)  & (df['p_vpd']<0.05)]; df_swc_vpd_2 = df[(df['p_swc']<0.05)  & (df['p_vpd']>=0.05)]
df_swc_vpd_3 = df[(df['p_swc']>=0.05) & (df['p_vpd']<0.05)]
df_swc_sw_1  = df[(df['p_swc']<0.05)  & (df['p_sw']<0.05)];  df_swc_sw_2  = df[(df['p_swc']<0.05)  & (df['p_sw']>=0.05)]
df_swc_sw_3  = df[(df['p_swc']>=0.05) & (df['p_sw']<0.05)]
df_swc_ta_1  = df[(df['p_swc']<0.05)  & (df['p_ta']<0.05)];  df_swc_ta_2  = df[(df['p_swc']<0.05)  & (df['p_ta']>=0.05)]
df_swc_ta_3  = df[(df['p_swc']>=0.05) & (df['p_ta']<0.05)]

df_swc_vpd_1 = df_swc_vpd_1[~((df_swc_vpd_1['r_swc']<0) & (df_swc_vpd_1['r_vpd']<0))]
df_swc_vpd_2 = df_swc_vpd_2[~((df_swc_vpd_2['r_swc']<0) & (df_swc_vpd_2['r_vpd']<0))]
df_swc_vpd_3 = df_swc_vpd_3[~((df_swc_vpd_3['r_swc']<0) & (df_swc_vpd_3['r_vpd']<0))]
data1 = pd.concat([df_swc_vpd_1,df_swc_vpd_2,df_swc_vpd_3],axis=0,ignore_index=True); data1.index = np.arange(0,len(data1))
data1a = data1[(data1['r_swc']<0) & (data1['r_vpd']>0)]  # the second quadrant (energy-controlled)
data1b = data1[(data1['r_swc']>0) & (data1['r_vpd']>0) & (data1['r_vpd']>data1['r_swc'])]  # the upper of first quadrant (energy-dominated)
data1c = data1[(data1['r_swc']>0) & (data1['r_vpd']>0) & (data1['r_vpd']<data1['r_swc'])]  # the lower of first quadrant (swc-dominated)
data1d = data1[(data1['r_swc']>0) & (data1['r_vpd']<0)]  # the fourth quadrant (swc-controlled)
length1 = len(data1a)+len(data1b)+len(data1c)+len(data1d)
ratio1  = [len(data1a)/length1*100,len(data1b)/length1*100,len(data1c)/length1*100,len(data1d)/length1*100]

df_swc_sw_1 = df_swc_sw_1[~((df_swc_sw_1['r_swc']<0) & (df_swc_sw_1['r_sw']<0))]
df_swc_sw_2 = df_swc_sw_2[~((df_swc_sw_2['r_swc']<0) & (df_swc_sw_2['r_sw']<0))]
df_swc_sw_3 = df_swc_sw_3[~((df_swc_sw_3['r_swc']<0) & (df_swc_sw_3['r_sw']<0))]
data2 = pd.concat([df_swc_sw_1,df_swc_sw_2,df_swc_sw_3],axis=0,ignore_index=True); data2.index = np.arange(0,len(data2))
data2a = data2[(data2['r_swc']<0) & (data2['r_sw']>0)]  # the second quadrant (energy-controlled)
data2b = data2[(data2['r_swc']>0) & (data2['r_sw']>0) & (data2['r_sw']>data2['r_swc'])]  # the upper of first quadrant (energy-dominated)
data2c = data2[(data2['r_swc']>0) & (data2['r_sw']>0) & (data2['r_sw']<data2['r_swc'])]  # the lower of first quadrant (swc-dominated)
data2d = data2[(data2['r_swc']>0) & (data2['r_sw']<0)]  # the fourth quadrant (swc-controlled)
length2 = len(data2a)+len(data2b)+len(data2c)+len(data2d)
ratio2  = [len(data2a)/length2*100,len(data2b)/length2*100,len(data2c)/length2*100,len(data2d)/length2*100]

df_swc_ta_1 = df_swc_ta_1[~((df_swc_ta_1['r_swc']<0) & (df_swc_ta_1['r_ta']<0))]
df_swc_ta_2 = df_swc_ta_2[~((df_swc_ta_2['r_swc']<0) & (df_swc_ta_2['r_ta']<0))]
df_swc_ta_3 = df_swc_ta_3[~((df_swc_ta_3['r_swc']<0) & (df_swc_ta_3['r_ta']<0))]
data3 = pd.concat([df_swc_ta_1,df_swc_ta_2,df_swc_ta_3],axis=0,ignore_index=True); data3.index = np.arange(0,len(data3))
data3a = data3[(data3['r_swc']<0) & (data3['r_ta']>0)]  # the second quadrant (energy-controlled)
data3b = data3[(data3['r_swc']>0) & (data3['r_ta']>0) & (data3['r_ta']>data3['r_swc'])]  # the upper of first quadrant (energy-dominated)
data3c = data3[(data3['r_swc']>0) & (data3['r_ta']>0) & (data3['r_ta']<data3['r_swc'])]  # the lower of first quadrant (swc-dominated)
data3d = data3[(data3['r_swc']>0) & (data3['r_ta']<0)]  # the fourth quadrant (swc-controlled)
length3 = len(data3a)+len(data3b)+len(data3c)+len(data3d)
ratio3  = [len(data3a)/length3*100,len(data3b)/length3*100,len(data3c)/length3*100,len(data3d)/length3*100]

#%% consider the one of vpd, sw and ta as energy limitation

dfnew = df.copy()
dfnew['p1'] = dfnew['p_vpd'].apply(lambda x: 1 if x<0.05 else 0)
dfnew['p2'] = dfnew['p_sw'].apply( lambda x: 1 if x<0.05 else 0)
dfnew['p3'] = dfnew['p_ta'].apply( lambda x: 1 if x<0.05 else 0)
dfnew['ps'] = dfnew['p1'] + dfnew['p2'] + dfnew['p3']
dfnew['r_max']    = dfnew[['r_vpd','r_sw','r_ta']].max(axis=1)
dfnew['r_min']    = dfnew[['r_vpd','r_sw','r_ta']].min(axis=1)
dfnew['r_energy'] = dfnew[['r_vpd','r_sw','r_ta']].abs().max(axis=1)
dfnew['r_energy'] = dfnew['r_energy'].where(dfnew['r_energy']!=dfnew['r_min'].abs(), dfnew['r_min'])

df_swc_energy_1 = dfnew[(dfnew['p_swc']<0.05)  & (dfnew['ps']>0)]
df_swc_energy_2 = dfnew[(dfnew['p_swc']<0.05)  & (dfnew['ps']==0)]
df_swc_energy_3 = dfnew[(dfnew['p_swc']>=0.05) & (dfnew['ps']>0)]
df_swc_energy_1 = df_swc_energy_1[~((df_swc_energy_1['r_swc']<0) & (df_swc_energy_1['r_energy']<0))]
df_swc_energy_2 = df_swc_energy_2[~((df_swc_energy_2['r_swc']<0) & (df_swc_energy_2['r_energy']<0))]
df_swc_energy_3 = df_swc_energy_3[~((df_swc_energy_3['r_swc']<0) & (df_swc_energy_3['r_energy']<0))]
data4 = pd.concat([df_swc_energy_1,df_swc_energy_2,df_swc_energy_3],axis=0,ignore_index=True); data4.index = np.arange(0,len(data4))
data4a = data4[(data4['r_swc']<0) & (data4['r_energy']>0)]  # the second quadrant (energy-controlled)
data4b = data4[(data4['r_swc']>0) & (data4['r_energy']>0) & (data4['r_energy']>data4['r_swc'])]  # the upper of first quadrant (energy-dominated)
data4c = data4[(data4['r_swc']>0) & (data4['r_energy']>0) & (data4['r_energy']<data4['r_swc'])]  # the lower of first quadrant (swc-dominated)
data4d = data4[(data4['r_swc']>0) & (data4['r_energy']<0)]  # the fourth quadrant (swc-controlled)
length4 = len(data4a)+len(data4b)+len(data4c)+len(data4d)
ratio4  = [len(data4a)/length4*100,len(data4b)/length4*100,len(data4c)/length4*100,len(data4d)/length4*100]

#%% multiple linear regression

df_m1 = df_multi1[df_multi1['f_pvalue']<0.05]; df_m1.index = np.arange(0,len(df_m1))

df_m1_swc_vpd_1 = df_m1[(df_m1['p_swc']<0.05)  & (df_m1['p_vpd']<0.05)]
df_m1_swc_vpd_2 = df_m1[(df_m1['p_swc']<0.05)  & (df_m1['p_vpd']>=0.05)]
df_m1_swc_vpd_3 = df_m1[(df_m1['p_swc']>=0.05) & (df_m1['p_vpd']<0.05)]
df_m1_swc_vpd_1 = df_m1_swc_vpd_1[~((df_m1_swc_vpd_1['b_swc']<0) & (df_m1_swc_vpd_1['b_vpd']<0))]
df_m1_swc_vpd_2 = df_m1_swc_vpd_2[~((df_m1_swc_vpd_2['b_swc']<0) & (df_m1_swc_vpd_2['b_vpd']<0))]
df_m1_swc_vpd_3 = df_m1_swc_vpd_3[~((df_m1_swc_vpd_3['b_swc']<0) & (df_m1_swc_vpd_3['b_vpd']<0))]
datam1  = pd.concat([df_m1_swc_vpd_1,df_m1_swc_vpd_2,df_m1_swc_vpd_3],axis=0,ignore_index=True); datam1.index = np.arange(0,len(datam1))
datam1a = datam1[(datam1['b_swc']<0) & (datam1['b_vpd']>0)]  # the second quadrant (energy-controlled)
datam1b = datam1[(datam1['b_swc']>0) & (datam1['b_vpd']>0) & (datam1['b_vpd']>datam1['b_swc'])]  # the upper of first quadrant (energy-dominated)
datam1c = datam1[(datam1['b_swc']>0) & (datam1['b_vpd']>0) & (datam1['b_vpd']<datam1['b_swc'])]  # the lower of first quadrant (swc-dominated)
datam1d = datam1[(datam1['b_swc']>0) & (datam1['b_vpd']<0)]  # the fourth quadrant (swc-controlled)
length_m1 = len(datam1a)+len(datam1b)+len(datam1c)+len(datam1d)
ratio1m   = [len(datam1a)/length_m1*100,len(datam1b)/length_m1*100,len(datam1c)/length_m1*100,len(datam1d)/length_m1*100]

df_m1_swc_sw_1 = df_m1[(df_m1['p_swc']<0.05)  & (df_m1['p_sw']<0.05)]
df_m1_swc_sw_2 = df_m1[(df_m1['p_swc']<0.05)  & (df_m1['p_sw']>=0.05)]
df_m1_swc_sw_3 = df_m1[(df_m1['p_swc']>=0.05) & (df_m1['p_sw']<0.05)]
df_m1_swc_sw_1 = df_m1_swc_sw_1[~((df_m1_swc_sw_1['b_swc']<0) & (df_m1_swc_sw_1['b_sw']<0))]
df_m1_swc_sw_2 = df_m1_swc_sw_2[~((df_m1_swc_sw_2['b_swc']<0) & (df_m1_swc_sw_2['b_sw']<0))]
df_m1_swc_sw_3 = df_m1_swc_sw_3[~((df_m1_swc_sw_3['b_swc']<0) & (df_m1_swc_sw_3['b_sw']<0))]
datam2  = pd.concat([df_m1_swc_sw_1,df_m1_swc_sw_2,df_m1_swc_sw_3],axis=0,ignore_index=True); datam2.index = np.arange(0,len(datam2))
datam2a = datam2[(datam2['b_swc']<0) & (datam2['b_sw']>0)]  # the second quadrant (energy-controlled)
datam2b = datam2[(datam2['b_swc']>0) & (datam2['b_sw']>0) & (datam2['b_sw']>datam2['b_swc'])]  # the upper of first quadrant (energy-dominated)
datam2c = datam2[(datam2['b_swc']>0) & (datam2['b_sw']>0) & (datam2['b_sw']<datam2['b_swc'])]  # the lower of first quadrant (swc-dominated)
datam2d = datam2[(datam2['b_swc']>0) & (datam2['b_sw']<0)]  # the fourth quadrant (swc-controlled)
length_m2 = len(datam2a)+len(datam2b)+len(datam2c)+len(datam2d)
ratio2m = [len(datam2a)/length_m2*100,len(datam2b)/length_m2*100,len(datam2c)/length_m2*100,len(datam2d)/length_m2*100]

df_m1_swc_ta_1 = df_m1[(df_m1['p_swc']<0.05)  & (df_m1['p_ta']<0.05)]
df_m1_swc_ta_2 = df_m1[(df_m1['p_swc']<0.05)  & (df_m1['p_ta']>=0.05)]
df_m1_swc_ta_3 = df_m1[(df_m1['p_swc']>=0.05) & (df_m1['p_ta']<0.05)]
df_m1_swc_ta_1 = df_m1_swc_ta_1[~((df_m1_swc_ta_1['b_swc']<0) & (df_m1_swc_ta_1['b_ta']<0))]
df_m1_swc_ta_2 = df_m1_swc_ta_2[~((df_m1_swc_ta_2['b_swc']<0) & (df_m1_swc_ta_2['b_ta']<0))]
df_m1_swc_ta_3 = df_m1_swc_ta_3[~((df_m1_swc_ta_3['b_swc']<0) & (df_m1_swc_ta_3['b_ta']<0))]
datam3  = pd.concat([df_m1_swc_ta_1,df_m1_swc_ta_2,df_m1_swc_ta_3],axis=0,ignore_index=True); datam3.index = np.arange(0,len(datam3))
datam3a = datam3[(datam3['b_swc']<0) & (datam3['b_ta']>0)]  # the second quadrant (energy-controlled)
datam3b = datam3[(datam3['b_swc']>0) & (datam3['b_ta']>0) & (datam3['b_ta']>datam3['b_swc'])]  # the upper of first quadrant (energy-dominated)
datam3c = datam3[(datam3['b_swc']>0) & (datam3['b_ta']>0) & (datam3['b_ta']<datam3['b_swc'])]  # the lower of first quadrant (swc-dominated)
datam3d = datam3[(datam3['b_swc']>0) & (datam3['b_ta']<0)]  # the fourth quadrant (swc-controlled)
length_m3 = len(datam3a)+len(datam3b)+len(datam3c)+len(datam3d)
ratio3m   = [len(datam3a)/length_m3*100,len(datam3b)/length_m3*100,len(datam3c)/length_m3*100,len(datam3d)/length_m3*100]

#%% consider the one of vpd, sw and ta as energy limitation

df_m1_new = df_m1.copy()
df_m1_new['p1'] = df_m1_new['p_vpd'].apply(lambda x: 1 if x<0.05 else 0)
df_m1_new['p2'] = df_m1_new['p_sw'].apply( lambda x: 1 if x<0.05 else 0)
df_m1_new['p3'] = df_m1_new['p_ta'].apply( lambda x: 1 if x<0.05 else 0)
df_m1_new['ps'] = df_m1_new['p1'] + df_m1_new['p2'] + df_m1_new['p3']
df_m1_new['b_max']    = df_m1_new[['b_vpd','b_sw','b_ta']].max(axis=1)
df_m1_new['b_min']    = df_m1_new[['b_vpd','b_sw','b_ta']].min(axis=1)
df_m1_new['b_energy'] = df_m1_new[['b_vpd','b_sw','b_ta']].abs().max(axis=1)
df_m1_new['b_energy'] = df_m1_new['b_energy'].where(df_m1_new['b_energy']!=df_m1_new['b_min'].abs(), df_m1_new['b_min'])

df_m1_swc_energy_1 = df_m1_new[(df_m1_new['p_swc']<0.05)  & (df_m1_new['ps']>0)]
df_m1_swc_energy_2 = df_m1_new[(df_m1_new['p_swc']<0.05)  & (df_m1_new['ps']==0)]
df_m1_swc_energy_3 = df_m1_new[(df_m1_new['p_swc']>=0.05) & (df_m1_new['ps']>0)]
df_m1_swc_energy_1 = df_m1_swc_energy_1[~((df_m1_swc_energy_1['b_swc']<0) & (df_m1_swc_energy_1['b_energy']<0))]
df_m1_swc_energy_2 = df_m1_swc_energy_2[~((df_m1_swc_energy_2['b_swc']<0) & (df_m1_swc_energy_2['b_energy']<0))]
df_m1_swc_energy_3 = df_m1_swc_energy_3[~((df_m1_swc_energy_3['b_swc']<0) & (df_m1_swc_energy_3['b_energy']<0))]
datam4 = pd.concat([df_m1_swc_energy_1,df_m1_swc_energy_2,df_m1_swc_energy_3],axis=0,ignore_index=True); datam4.index = np.arange(0,len(datam4))
datam4a = datam4[(datam4['b_swc']<0) & (datam4['b_energy']>0)]  # the second quadrant (energy-controlled)
datam4b = datam4[(datam4['b_swc']>0) & (datam4['b_energy']>0) & (datam4['b_energy']>datam4['b_swc'])]  # the upper of first quadrant (energy-dominated)
datam4c = datam4[(datam4['b_swc']>0) & (datam4['b_energy']>0) & (datam4['b_energy']<datam4['b_swc'])]  # the lower of first quadrant (swc-dominated)
datam4d = datam4[(datam4['b_swc']>0) & (datam4['b_energy']<0)]  # the fourth quadrant (swc-controlled)
length_m4 = len(datam4a)+len(datam4b)+len(datam4c)+len(datam4d)
ratio4m   = [len(datam4a)/length_m4*100,len(datam4b)/length_m4*100,len(datam4c)/length_m4*100,len(datam4d)/length_m4*100]

#%% plot

x1 = [df_swc_vpd_1['r_swc'],df_swc_sw_1['r_swc'],df_swc_ta_1['r_swc'],df_swc_energy_1['r_swc']]
y1 = [df_swc_vpd_1['r_vpd'],df_swc_sw_1['r_sw'], df_swc_ta_1['r_ta'], df_swc_energy_1['r_energy']]
x2 = [df_swc_vpd_2['r_swc'],df_swc_sw_2['r_swc'],df_swc_ta_2['r_swc'],df_swc_energy_2['r_swc']]
y2 = [df_swc_vpd_2['r_vpd'],df_swc_sw_2['r_sw'], df_swc_ta_2['r_ta'], df_swc_energy_2['r_energy']]
x3 = [df_swc_vpd_3['r_swc'],df_swc_sw_3['r_swc'],df_swc_ta_3['r_swc'],df_swc_energy_3['r_swc']]
y3 = [df_swc_vpd_3['r_vpd'],df_swc_sw_3['r_sw'], df_swc_ta_3['r_ta'], df_swc_energy_3['r_energy']]
x1a = [df_m1_swc_vpd_1['b_swc'],df_m1_swc_sw_1['b_swc'],df_m1_swc_ta_1['b_swc'],df_m1_swc_energy_1['b_swc']]
y1a = [df_m1_swc_vpd_1['b_vpd'],df_m1_swc_sw_1['b_sw'], df_m1_swc_ta_1['b_ta'], df_m1_swc_energy_1['b_energy']]
x2a = [df_m1_swc_vpd_2['b_swc'],df_m1_swc_sw_2['b_swc'],df_m1_swc_ta_2['b_swc'],df_m1_swc_energy_2['b_swc']]
y2a = [df_m1_swc_vpd_2['b_vpd'],df_m1_swc_sw_2['b_sw'], df_m1_swc_ta_2['b_ta'], df_m1_swc_energy_2['b_energy']]
x3a = [df_m1_swc_vpd_3['b_swc'],df_m1_swc_sw_3['b_swc'],df_m1_swc_ta_3['b_swc'],df_m1_swc_energy_3['b_swc']]
y3a = [df_m1_swc_vpd_3['b_vpd'],df_m1_swc_sw_3['b_sw'], df_m1_swc_ta_3['b_ta'], df_m1_swc_energy_3['b_energy']]

ylabel1 = [r'$R_\mathregular{VPD-Td}$',r'$R_\mathregular{SR-Td}$',r'$R_\mathregular{Ta-Td}$',r'$R_\mathregular{Energy-Td}$']
ylabel2 = [r'$\beta_\mathregular{VPD}$',  r'$\beta_\mathregular{SR}$',  r'$\beta_\mathregular{Ta}$', r'$\beta_\mathregular{Energy}$']
size2 = 50; col = ['red',[220/255,80/255,87/255],[80/255,87/255,220/255],'blue']
labels = ['E-c','E-d','S-d','S-c']
col1 = [[170/255,170/255,170/255],[170/255,170/255,170/255],[170/255,170/255,170/255]]; linewidth = 0.8
name1 = ['(a)','(b)','(c)','(d)']; name2 = ['(e)','(f)','(g)','(h)']

fig = plt.figure(figsize=(16,7)); size1 = 35; size2 = 50
plt.subplots_adjust(left=0.047,right=0.99,top=0.97,bottom=0.09,wspace=0.34,hspace=0.3)

for ii in range(len(x1)):
    ax1 = plt.subplot(2,4,ii+1)
    plt.scatter(x1[ii],y1[ii],size2,facecolor='white',edgecolor=col1[0],linewidths=linewidth)
    plt.scatter(x2[ii],y2[ii],size2,facecolor='white',edgecolor=col1[1],linewidths=linewidth)
    plt.scatter(x3[ii],y3[ii],size2,facecolor='white',edgecolor=col1[2],linewidths=linewidth)
    plt.hlines(0,-1,1,colors=[170/255,170/255,170/255],linestyles='--',zorder=0)
    plt.vlines(0,-1,1,colors=[170/255,170/255,170/255],linestyles='--',zorder=0)
    plt.plot((-1,1),(-1,1),'-.',color=[55/255,55/255,55/255],zorder=0)
    plt.xlim(-1,1); plt.ylim(-1,1); plt.xticks(fontsize=11); plt.yticks(fontsize=11)
    x_major_locator = MultipleLocator(0.5); ax1.xaxis.set_major_locator(x_major_locator)
    y_major_locator = MultipleLocator(0.5); ax1.yaxis.set_major_locator(y_major_locator)
    ax1.set_xlabel(r'$R_\mathregular{SM-Td}$',fontdict={'size':11},labelpad=6)
    ax1.set_ylabel(ylabel1[ii],fontdict={'size':11},labelpad=3)
    ax1.text(-1.48,0.91,name1[ii],weight='bold',color='black',fontdict={'size':11})
    
for jj in range(len(x1a)):
    ax1 = plt.subplot(2,4,jj+5)
    plt.scatter(x1a[jj],y1a[jj],size2,facecolor='white',edgecolor=col1[0],linewidths=linewidth)
    plt.scatter(x2a[jj],y2a[jj],size2,facecolor='white',edgecolor=col1[1],linewidths=linewidth)
    plt.scatter(x3a[jj],y3a[jj],size2,facecolor='white',edgecolor=col1[2],linewidths=linewidth)
    plt.hlines(0,-1.5,1.5,colors=[170/255,170/255,170/255],linestyles='--',zorder=0)
    plt.vlines(0,-1.5,1.5,colors=[170/255,170/255,170/255],linestyles='--',zorder=0)
    plt.plot((-1.5,1.5),(-1.5,1.5),'-.',color=[55/255,55/255,55/255],zorder=0)
    plt.xlim(-1.5,1.5); plt.ylim(-1.5,1.5); plt.xticks(fontsize=11); plt.yticks(fontsize=11)
    x_major_locator = MultipleLocator(1.5); ax1.xaxis.set_major_locator(x_major_locator)
    y_major_locator = MultipleLocator(1.5); ax1.yaxis.set_major_locator(y_major_locator)
    ax1.set_xlabel(r'$\beta_\mathregular{SM}$',fontdict={'size':11},labelpad=6)
    ax1.set_ylabel(ylabel2[jj],fontdict={'size':11},labelpad=3)
    ax1.text(-2.21,1.37,name2[jj],weight='bold',color='black',fontdict={'size':11})

ratio_r = [ratio1,ratio2,ratio3,ratio4]; wid = [0.071,0.322,0.574,0.826]; x = np.arange(0,len(ratio1))
for kk in range(len(ratio_r)):
    ax1 = fig.add_axes([wid[kk],0.617,0.055,0.1])
    plt.bar(x,ratio_r[kk],0.75,color=col)
    ax1.spines['top'].set_visible(False); ax1.spines['right'].set_visible(False)
    plt.xticks(fontsize=8); plt.yticks(fontsize=8)
    y_major_locator = MultipleLocator(10) if kk==0 or kk==2 else MultipleLocator(20)
    ax1.yaxis.set_major_locator(y_major_locator)
    x_ticks = np.arange(0,4,1); ax1.set_xticks(x_ticks); ax1.set_xticklabels(labels,rotation=0)
    ax1.set_ylabel('Ratio (%)',fontdict={'size':8},labelpad=0)

ratio_b = [ratio1m,ratio2m,ratio3m,ratio4m]; wid = [0.071,0.322,0.574,0.826]; x = np.arange(0,len(ratio1))
for kk in range(len(ratio_b)):
    ax1 = fig.add_axes([wid[kk],0.12,0.055,0.1])
    plt.bar(x,ratio_b[kk],0.75,color=col)
    ax1.spines['top'].set_visible(False); ax1.spines['right'].set_visible(False)
    plt.xticks(fontsize=8); plt.yticks(fontsize=8)
    y_major_locator = MultipleLocator(20) if kk==0 or kk==3 else MultipleLocator(10)
    ax1.yaxis.set_major_locator(y_major_locator)
    x_ticks = np.arange(0,4,1); ax1.set_xticks(x_ticks); ax1.set_xticklabels(labels,rotation=0)
    ax1.set_ylabel('Ratio (%)',fontdict={'size':8},labelpad=0)

plt.show()
plt.savefig(outpath+'Fig2.png',dpi=500)
