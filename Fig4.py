# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 07:05:45 2025

@author: songchaoqing
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import matplotlib.ticker as ticker
from mpl_toolkits.basemap import Basemap

import scicomap as sc
sc_map = sc.ScicoSequential()
sc_map.get_color_map_names()

# load the color map
mpl_cmap_obj = plt.get_cmap("RdBu_r")
div_map = sc.ScicoDiverging(cmap=mpl_cmap_obj)
div_map.unif_sym_cmap(lift=None,bitonic=False,diffuse=True)
cmap1 = div_map.get_mpl_color_map()

#%%

df = pd.read_excel('C:/Users/songchaoqing/Desktop/plant_water_stress/3_site_species_theta_threshold.xlsx')
infile = 'C:/Users/songchaoqing/Desktop/plant_water_stress/2_linear_regress_grow.csv'; dfnew = pd.read_csv(infile)
dfnew['p1'] = dfnew['p_vpd'].apply(lambda x: 1 if x<0.05 else 0)
dfnew['p2'] = dfnew['p_sw'].apply( lambda x: 1 if x<0.05 else 0)
dfnew['p3'] = dfnew['p_ta'].apply( lambda x: 1 if x<0.05 else 0)
dfnew['ps'] = dfnew['p1'] + dfnew['p2'] + dfnew['p3']
dfnew['r_max']    = dfnew[['r_vpd','r_sw','r_ta']].max(axis=1)
dfnew['r_min']    = dfnew[['r_vpd','r_sw','r_ta']].min(axis=1)
dfnew['r_energy'] = dfnew[['r_vpd','r_sw','r_ta']].abs().max(axis=1)
dfnew['r_energy'] = dfnew['r_energy'].where(dfnew['r_energy']!=dfnew['r_min'].abs(), dfnew['r_min'])

df_swc_energy_1 = dfnew[(dfnew['p_swc']<0.05)  & (dfnew['ps']>0)];  df_swc_energy_1['contr'] = 1   # swc+energy impacts signifi
df_swc_energy_2 = dfnew[(dfnew['p_swc']<0.05)  & (dfnew['ps']==0)]; df_swc_energy_2['contr'] = 2   # swc impact signifi
df_swc_energy_3 = dfnew[(dfnew['p_swc']>=0.05) & (dfnew['ps']>0)];  df_swc_energy_3['contr'] = 3   # energy impact signifi
df_swc_energy_4 = dfnew[(dfnew['p_swc']>=0.05) & (dfnew['ps']==0)]; df_swc_energy_4['contr'] = 4   # both no impact
df_swc_energy   = pd.concat([df_swc_energy_1,df_swc_energy_2,df_swc_energy_3,df_swc_energy_4],axis=0,ignore_index=True)
df_swc_energy.index = np.arange(0,len(df_swc_energy))
df_swc_energy['species'] = df_swc_energy['Es_var'].str[0:3]
df4 = df_swc_energy[['site','species','r_swc','r_vpd','r_sw','r_ta','r_energy','contr']]

df5 = pd.merge(df,df4,on=['site','species'],how='left')
df5_energy     = df5[(df5['r_swc']<0) & (df5['r_energy']>0)]  # the second quadrant (energy-controlled)
df5_energy_swc = df5[(df5['r_swc']>0) & (df5['r_energy']>0) & (df5['r_energy']>df5['r_swc'])]  # the upper of first quadrant (energy-dominated)
df5_swc_energy = df5[(df5['r_swc']>0) & (df5['r_energy']>0) & (df5['r_energy']<df5['r_swc'])]  # the lower of first quadrant (swc-dominated)
df5_swc        = df5[(df5['r_swc']>0) & (df5['r_energy']<0)]  # the fourth quadrant (swc-controlled)

df5_E_c = df5_energy[['site','species','site_lat','site_long']];     df5_E_c.rename(columns={'site_lat':'ini_lat','site_long':'ini_lon'},inplace=True)
df5_E_d = df5_energy_swc[['site','species','site_lat','site_long']]; df5_E_d.rename(columns={'site_lat':'ini_lat','site_long':'ini_lon'},inplace=True)
df5_S_d = df5_swc_energy[['site','species','site_lat','site_long']]; df5_S_d.rename(columns={'site_lat':'ini_lat','site_long':'ini_lon'},inplace=True)
df5_S_c = df5_swc[['site','species','site_lat','site_long']];        df5_S_c.rename(columns={'site_lat':'ini_lat','site_long':'ini_lon'},inplace=True)

#%%

# these codes are only used to show multiply speices of one site on a map non overlaping
df0 = df[['site','species','site_lat','site_long','swc_thr']]
lat_val = df0['site_lat'].value_counts(); lat_val = lat_val.to_frame()
lat_val.reset_index(level=0,inplace=True); lat_val.rename(columns={'count':'lat_st'},inplace=True)

df0b = []
for ii in range(len(lat_val)):
    lat0 = lat_val['site_lat'][ii]
    df0a = df0[(df0['site_lat']==lat0)]
    if len(df0a)>1: 
        aa = np.arange(0,len(df0a))
        df0a['site_long'] = df0a['site_long']+aa*4
    df0b = pd.concat([df0b,df0a]) if ii>0 else df0a

df1 = df0b.sort_values(by='site',ascending=True); df1.index = np.arange(0,len(df1))

df1['site_lat'][0:3]  = df1['site_lat'][0:3]+9         # CAN_TUR_P*
df1['site_long'][0:1] = df1['site_long'][0:1]+8.7      # CAN_TUR_P*
df1['site_long'][1:3] = df1['site_long'][1:3]+0.7      # CAN_TUR_P*

df1['site_lat'][3:5]  = df1['site_lat'][3:5]-3         # CZE_LAN
df1['site_long'][3:4] = df1['site_long'][3:4]+8        # CZE_LAN

df1['site_long'][6:7] = df1['site_long'][6:7]+3        # CZE_STI
df1['site_lat'][6:7]  = df1['site_lat'][6:7]+3         # CZE_STI

df1['site_lat'][8:11]  = df1['site_lat'][8:11]+6       # ESP_ALT_ARM
df1['site_long'][8:11] = df1['site_long'][8:11]-9      # ESP_ALT_ARM

df1['site_lat'][11:15]  = df1['site_lat'][11:15]-6     # ESP_CAN
df1['site_long'][11:14] = df1['site_long'][11:14]+4    # ESP_CAN
df1['site_long'][13:14] = df1['site_long'][13:14]+4

df1['site_lat'][15:19]  = df1['site_lat'][15:19]-10    # ESP_TIL_*
df1['site_long'][17:18] = df1['site_long'][17:18]+8    # ESP_TIL_OAK
df1['site_long'][18:19] = df1['site_long'][18:19]+12   # ESP_TIL_PIN
df1['site_long'][15:19] = df1['site_long'][15:19]-10

df1['site_lat'][19:20]  = df1['site_lat'][19:20]+4     # ESP_VAL_SOR
df1['site_long'][19:20] = df1['site_long'][19:20]-1    # ESP_VAL_SOR

df1['site_long'][21:22] = df1['site_long'][21:22]+2    # GBR_ABE_PLO
df1['site_long'][22:23] = df1['site_long'][22:23]+6    # GBR_DEV_DRO
df1['site_long'][23:24] = df1['site_long'][23:24]-1    # GBR_GUI_ST1
df1['site_lat'][21:24]  = 61

df1['site_lat'][24:30]  = df1['site_lat'][24:30]-6     # GUF_GUY_*
df1['site_long'][24:25] = df1['site_long'][24:25]-4    # GUF_GUY_GUY
df1['site_long'][25:26] = df1['site_long'][25:26]-12
df1['site_long'][24:30] = df1['site_long'][24:30]-6    # GUF_GUY_*

df1['site_long'][30:35] = df1['site_long'][30:35]-6    # IDN_PON_STE
df1['site_lat'][30:35]  = df1['site_lat'][30:35]-6     # IDN_PON_STE

df1['site_lat'][35:40]  = df1['site_lat'][35:40]-6     # ITA_MAT_S21
df1['site_long'][35:36] = df1['site_long'][35:36]-4
df1['site_long'][38:39] = df1['site_long'][38:39]+8
df1['site_long'][35:39] = df1['site_long'][35:39]+5

df1['site_long'][39:40] = df1['site_long'][39:40]+17

df1['site_lat'][40:41]  = df1['site_lat'][40:41]+3     # ITA_TOR
df1['site_long'][40:41] = df1['site_long'][40:41]-3    # ITA_TOR

df1['site_lat'][42:45]  = df1['site_lat'][42:45]-6     # RUS_POG_VAR
df1['site_long'][42:45] = df1['site_long'][42:45]-6

df1['site_lat'][45:49]  = df1['site_lat'][45:49]+5     # SWE_NOR_ST*
df1['site_long'][45:49] = df1['site_long'][45:49]-2
df1['site_long'][45:46] = df1['site_long'][45:46]-4

df1['site_lat'][50:54]  = df1['site_lat'][50:54]-5     # USA_DUK_HAR
df1['site_long'][51:53] = df1['site_long'][51:53]+12
df1['site_long'][50:51] = df1['site_long'][50:51]+16
df1['site_long'][53:54] = df1['site_long'][53:54]+8

df1['site_lat'][54:57]  = df1['site_lat'][54:57]-9.5   # USA_HIL_HF*
df1['site_long'][54:55] = df1['site_long'][54:55]+8
df1['site_long'][54:57] = df1['site_long'][54:57]+7

df1['site_lat'][58:64]  = df1['site_lat'][58:64]+3.5   # USA_INM and USA_MOR_SF
df1['site_long'][63:64] = df1['site_long'][63:64]-4
df1['site_long'][58:64] = df1['site_long'][58:64]-22

df1['site_lat'][64:65]  = df1['site_lat'][64:65]+2     # USA_PAR_FER
df1['site_long'][64:65] = df1['site_long'][64:65]+5    # USA_PAR_FER

df1['site_lat'][65:70]  = df1['site_lat'][65:70]+4     # USA_PJS_P0*_AMB
df1['site_long'][65:70] = df1['site_long'][65:70]-17

df1['site_lat'][70:75]  = df1['site_lat'][70:75]+2.5   # USA_SIL_OAK_*PR
df1['site_long'][70:75] = df1['site_long'][70:75]+8

df1['site_lat'][75:77]  = df1['site_lat'][75:77]+6.5   # USA_SYL_HL2
df1['site_long'][75:77] = df1['site_long'][75:77]-9

df1['site_lat'][77:81]  = df1['site_lat'][77:81]+1     # USA_TNB
df1['site_long'][77:81] = df1['site_long'][77:81]-17

df1['site_lat'][81:83]  = df1['site_lat'][81:83]-9.5   # USA_TNO
df1['site_long'][81:83] = df1['site_long'][81:83]-4.5

df1['site_lat'][83:88]  = df1['site_lat'][83:88]-6     # USA_TNP
df1['site_long'][83:88] = df1['site_long'][83:88]-23
df1['site_lat'][88:91]  = df1['site_lat'][88:91]-13    # USA_TNY
df1['site_long'][88:91] = df1['site_long'][88:91]+2.5

df1['site_long'][91:92] = df1['site_long'][91:92]-4    # USA_UMB_CON
df1['site_long'][91:96] = df1['site_long'][91:96]-6    # USA_UMB_GIR
df1['site_lat'][91:96]  = df1['site_lat'][91:96]+12    # USA_UMB_GIR

df1['site_lat'][96:99]  = df1['site_lat'][96:99]+2     # USA_WIL_WC1
df1['site_long'][96:99] = df1['site_long'][96:99]-14

df1['site_lat'][99:103]  = df1['site_lat'][99:103]+10  # USA_WVF
df1['site_long'][99:103] = df1['site_long'][99:103]+11

df1_energy     = pd.merge(df5_E_c,df1,on=['site','species'],how='left')
df1_energy_swc = pd.merge(df5_E_d,df1,on=['site','species'],how='left')
df1_swc_energy = pd.merge(df5_S_d,df1,on=['site','species'],how='left')
df1_swc        = pd.merge(df5_S_c,df1,on=['site','species'],how='left')

df1_energy     = df1_energy.sort_values(by=['site','species'],ascending=True);     df1_energy.index = np.arange(0,len(df1_energy))
df1_energy_swc = df1_energy_swc.sort_values(by=['site','species'],ascending=True); df1_energy_swc.index = np.arange(0,len(df1_energy_swc))
df1_swc_energy = df1_swc_energy.sort_values(by=['site','species'],ascending=True); df1_swc_energy.index = np.arange(0,len(df1_swc_energy))
df1_swc        = df1_swc.sort_values(by=['site','species'],ascending=True);        df1_swc.index = np.arange(0,len(df1_swc))

#%% plot

fig = plt.figure(figsize=(14,10)); lat_0=0; lon_0=0
length=0.42; width=0.3; size1=25; size2=10; coll=[170/255,170/255,170/255]

ax0 = fig.add_axes([0.05,0.722,length,width])
m = Basemap(projection='cyl', lon_0=lon_0, lat_0=lat_0)
m = Basemap(llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=179.5)
m.fillcontinents(color=[220/255,220/255,220/255], lake_color='none')

# these codes are only used to point to multiply speices of one site on a map non overlaping
m.plot((df1_energy['site_long'][0],df1_energy['ini_lon'][0]),(df1_energy['site_lat'][0],df1_energy['ini_lat'][0]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][0],df1_energy['ini_lat'][0],s=size2,color='black')                 # CZE_LAN
m.plot((df1_energy['site_long'][1],df1_energy['ini_lon'][1]),(df1_energy['site_lat'][1],df1_energy['ini_lat'][1]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][1],df1_energy['ini_lat'][1],s=size2,color='black')                 # CZE_STI
m.plot((df1_energy['site_long'][3],df1_energy['ini_lon'][3]),(df1_energy['site_lat'][3],df1_energy['ini_lat'][3]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][3],df1_energy['ini_lat'][3],s=size2,color='black')                 # ESP_ALT_ARM
m.plot((df1_energy['site_long'][4:6],df1_energy['ini_lon'][4:6]),(df1_energy['site_lat'][4:6],df1_energy['ini_lat'][4:6]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][4],df1_energy['ini_lat'][4],s=size2,color='black')                 # IND_PON_STE
m.plot((df1_energy['site_long'][6:8],df1_energy['ini_lon'][6:8]),(df1_energy['site_lat'][6:8],df1_energy['ini_lat'][6:8]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][6],df1_energy['ini_lat'][6],s=size2,color='black')                 # ITA_MAT_S21 and ITA_KAE_S20
m.plot((df1_energy['site_long'][8:9],df1_energy['ini_lon'][8:9]),(df1_energy['site_lat'][8:9],df1_energy['ini_lat'][8:9]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][8],df1_energy['ini_lat'][8],s=size2,color='black')                 # ITA_TOR
m.plot((df1_energy['site_long'][9:12],df1_energy['ini_lon'][9:12]),(df1_energy['site_lat'][9:12],df1_energy['ini_lat'][9:12]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][9],df1_energy['ini_lat'][9],s=size2,color='black')                 # USA_DUK_HAR
m.plot((df1_energy['site_long'][12:14],df1_energy['ini_lon'][12:14]),(df1_energy['site_lat'][12:14],df1_energy['ini_lat'][12:14]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][12],df1_energy['ini_lat'][12],s=size2,color='black')               # USA_INM
m.plot((df1_energy['site_long'][14:15],df1_energy['ini_lon'][14:15]),(df1_energy['site_lat'][14:15],df1_energy['ini_lat'][14:15]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][14],df1_energy['ini_lat'][14],s=size2,color='black')               # USA_PAR_FER
m.plot((df1_energy['site_long'][15:16],df1_energy['ini_lon'][15:16]),(df1_energy['site_lat'][15:16],df1_energy['ini_lat'][15:16]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][15],df1_energy['ini_lat'][15],s=size2,color='black')               # USA_SIL_OAK_*PR
m.plot((df1_energy['site_long'][16:17],df1_energy['ini_lon'][16:17]),(df1_energy['site_lat'][16:17],df1_energy['ini_lat'][16:17]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][16],df1_energy['ini_lat'][16],s=size2,color='black')               # USA_SYL_HL2
m.plot((df1_energy['site_long'][17:19],df1_energy['ini_lon'][17:19]),(df1_energy['site_lat'][17:19],df1_energy['ini_lat'][17:19]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][17],df1_energy['ini_lat'][17],s=size2,color='black')               # USA_TNY
m.plot((df1_energy['site_long'][19:21],df1_energy['ini_lon'][19:21]),(df1_energy['site_lat'][19:21],df1_energy['ini_lat'][19:21]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][19],df1_energy['ini_lat'][19],s=size2,color='black')               # USA_UMB_GIR and USA_UMB_CON
m.plot((df1_energy['site_long'][21:24],df1_energy['ini_lon'][21:24]),(df1_energy['site_lat'][21:24],df1_energy['ini_lat'][21:24]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][21],df1_energy['ini_lat'][21],s=size2,color='black')               # USA_WIL_WC1
m.plot((df1_energy['site_long'][24],df1_energy['ini_lon'][24]),(df1_energy['site_lat'][24],df1_energy['ini_lat'][24]),'-',color=coll,zorder=1)
m.scatter(df1_energy['ini_lon'][24],df1_energy['ini_lat'][24],s=size2,color='black')               # USA_WVF

m.scatter(df1_energy['site_long'][1:],df1_energy['site_lat'][1:],s=size1,edgecolor=[130/255,130/255,130/255],
          c=df1_energy['swc_thr'][1:],cmap='RdYlBu',vmin=df1['swc_thr'].min(),vmax=df1['swc_thr'].max(),linewidths=1)
m.scatter(df1_energy['site_long'][0],df1_energy['site_lat'][0],s=size1,edgecolor=[0/255,0/255,0/255],
          c=df1_energy['swc_thr'][0],cmap='RdYlBu',vmin=df1['swc_thr'].min(),vmax=df1['swc_thr'].max(),linewidths=1)
position = fig.add_axes([0.205,0.774,0.15,0.011])
cbar = plt.colorbar(cax=position,orientation='horizontal',shrink=0.5,ticks=[0,0.1,0.2,0.3,0.4,0.5])
plt.text(0.5,-0.01,r'$\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',color='black',fontdict={'size':9})
ax0.text(-176.2,78,'(a)',weight='bold',color='black',fontdict={'size':11})

#############################################################################################################################################

ax1 = fig.add_axes([0.56,0.722,length,width])
m = Basemap(projection='cyl', lon_0=lon_0, lat_0=lat_0)
m = Basemap(llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=179.5)
m.fillcontinents(color=[220/255,220/255,220/255], lake_color='none')

m.plot((df1_energy_swc['site_long'][0:2],df1_energy_swc['ini_lon'][0:2]),(df1_energy_swc['site_lat'][0:2],df1_energy_swc['ini_lat'][0:2]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][0],df1_energy_swc['ini_lat'][0],s=size2,color='black')                 # CAN_TUR_P*
m.plot((df1_energy_swc['site_long'][2:3],df1_energy_swc['ini_lon'][2:3]),(df1_energy_swc['site_lat'][2:3],df1_energy_swc['ini_lat'][2:3]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][2],df1_energy_swc['ini_lat'][2],s=size2,color='black')                 # CZE_LAN
m.plot((df1_energy_swc['site_long'][4:6],df1_energy_swc['ini_lon'][4:6]),(df1_energy_swc['site_lat'][4:6],df1_energy_swc['ini_lat'][4:6]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][4],df1_energy_swc['ini_lat'][4],s=size2,color='black')                 # ESP_ALT_ARM
m.plot((df1_energy_swc['site_long'][6:7],df1_energy_swc['ini_lon'][6:7]),(df1_energy_swc['site_lat'][6:7],df1_energy_swc['ini_lat'][6:7]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][6],df1_energy_swc['ini_lat'][6],s=size2,color='black')                 # ESP_CAN
m.plot((df1_energy_swc['site_long'][7:8],df1_energy_swc['ini_lon'][7:8]),(df1_energy_swc['site_lat'][7:8],df1_energy_swc['ini_lat'][7:8]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][7],df1_energy_swc['ini_lat'][7],s=size2,color='black')                 # ESP_TIL_MIX
m.plot((df1_energy_swc['site_long'][8:9],df1_energy_swc['ini_lon'][8:9]),(df1_energy_swc['site_lat'][8:9],df1_energy_swc['ini_lat'][8:9]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][8],df1_energy_swc['ini_lat'][8],s=size2,color='black')                 # ESP_VAL_SOR
m.plot((df1_energy_swc['site_long'][10:11],df1_energy_swc['ini_lon'][10:11]),(df1_energy_swc['site_lat'][10:11],df1_energy_swc['ini_lat'][10:11]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][10],df1_energy_swc['ini_lat'][10],s=size2,color='black')               # GBR_DEV_DRO
m.plot((df1_energy_swc['site_long'][11:12],df1_energy_swc['ini_lon'][11:12]),(df1_energy_swc['site_lat'][11:12],df1_energy_swc['ini_lat'][11:12]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][11],df1_energy_swc['ini_lat'][11],s=size2,color='black')               # GBR_GUI_ST1
m.plot((df1_energy_swc['site_long'][12:13],df1_energy_swc['ini_lon'][12:13]),(df1_energy_swc['site_lat'][12:13],df1_energy_swc['ini_lat'][12:13]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][12],df1_energy_swc['ini_lat'][12],s=size2,color='black')               # GUF_GUY_*
m.plot((df1_energy_swc['site_long'][13:15],df1_energy_swc['ini_lon'][13:15]),(df1_energy_swc['site_lat'][13:15],df1_energy_swc['ini_lat'][13:15]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][13],df1_energy_swc['ini_lat'][13],s=size2,color='black')               # IND_PON_STE
m.plot((df1_energy_swc['site_long'][16:19],df1_energy_swc['ini_lon'][16:19]),(df1_energy_swc['site_lat'][16:19],df1_energy_swc['ini_lat'][16:19]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][16],df1_energy_swc['ini_lat'][16],s=size2,color='black')               # RUS_POG_VAR
m.plot((df1_energy_swc['site_long'][19:23],df1_energy_swc['ini_lon'][19:23]),(df1_energy_swc['site_lat'][19:23],df1_energy_swc['ini_lat'][19:23]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][19],df1_energy_swc['ini_lat'][19],s=size2,color='black')               # SWE_NOR_ST*
m.plot((df1_energy_swc['site_long'][23:25],df1_energy_swc['ini_lon'][23:25]),(df1_energy_swc['site_lat'][23:25],df1_energy_swc['ini_lat'][23:25]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][23],df1_energy_swc['ini_lat'][23],s=size2,color='black')               # USA_HIL_HF*
m.plot((df1_energy_swc['site_long'][26:29],df1_energy_swc['ini_lon'][26:29]),(df1_energy_swc['site_lat'][26:29],df1_energy_swc['ini_lat'][26:29]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][26],df1_energy_swc['ini_lat'][26],s=size2,color='black')               # USA_INM
m.plot((df1_energy_swc['site_long'][29:30],df1_energy_swc['ini_lon'][29:30]),(df1_energy_swc['site_lat'][29:30],df1_energy_swc['ini_lat'][29:30]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][29],df1_energy_swc['ini_lat'][29],s=size2,color='black')               # USA_SYL_HL2
m.plot((df1_energy_swc['site_long'][30:32],df1_energy_swc['ini_lon'][30:32]),(df1_energy_swc['site_lat'][30:32],df1_energy_swc['ini_lat'][30:32]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][30],df1_energy_swc['ini_lat'][30],s=size2,color='black')               # USA_TNB
m.plot((df1_energy_swc['site_long'][32:33],df1_energy_swc['ini_lon'][32:33]),(df1_energy_swc['site_lat'][32:33],df1_energy_swc['ini_lat'][32:33]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][32],df1_energy_swc['ini_lat'][32],s=size2,color='black')               # USA_TNY
m.plot((df1_energy_swc['site_long'][33:36],df1_energy_swc['ini_lon'][33:36]),(df1_energy_swc['site_lat'][33:36],df1_energy_swc['ini_lat'][33:36]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][33],df1_energy_swc['ini_lat'][33],s=size2,color='black')               # USA_UMB_GIR and USA_UMB_CON
m.plot((df1_energy_swc['site_long'][36:38],df1_energy_swc['ini_lon'][36:38]),(df1_energy_swc['site_lat'][36:38],df1_energy_swc['ini_lat'][36:38]),'-',color=coll,zorder=1)
m.scatter(df1_energy_swc['ini_lon'][36],df1_energy_swc['ini_lat'][36],s=size2,color='black')               # USA_WVF

m.scatter(df1_energy_swc['site_long'],df1_energy_swc['site_lat'],s=size1,edgecolor=[130/255,130/255,130/255],
          c=df1_energy_swc['swc_thr'],cmap='RdYlBu',vmin=df1['swc_thr'].min(),vmax=df1['swc_thr'].max(),linewidths=1)
m.scatter(df1_energy_swc['site_long'][16],df1_energy_swc['site_lat'][16],s=size1,edgecolor=[0/255,0/255,0/255],
          c=df1_energy_swc['swc_thr'][16],cmap='RdYlBu',vmin=df1['swc_thr'].min(),vmax=df1['swc_thr'].max(),linewidths=1)
position = fig.add_axes([0.715,0.774,0.15,0.011])
cbar = plt.colorbar(cax=position,orientation='horizontal',shrink=0.5,ticks=[0,0.1,0.2,0.3,0.4,0.5])
plt.text(0.5,-0.01,r'$\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',color='black',fontdict={'size':9})
ax1.text(-176.2,78,'(b)',weight='bold',color='black',fontdict={'size':11})

#############################################################################################################################################

ax2 = fig.add_axes([0.05,0.213,length,width])
m = Basemap(projection='cyl', lon_0=lon_0, lat_0=lat_0)
m = Basemap(llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=179.5)
m.fillcontinents(color=[220/255,220/255,220/255], lake_color='none')

m.plot((df1_swc_energy['site_long'][0:1],df1_swc_energy['ini_lon'][0:1]),(df1_swc_energy['site_lat'][0:1],df1_swc_energy['ini_lat'][0:1]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][0],df1_swc_energy['ini_lat'][0],s=size2,color='black')               # CAN_TUR_P*
m.plot((df1_swc_energy['site_long'][1:4],df1_swc_energy['ini_lon'][1:4]),(df1_swc_energy['site_lat'][1:4],df1_swc_energy['ini_lat'][1:4]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][1],df1_swc_energy['ini_lat'][1],s=size2,color='black')               # ESP_CAN
m.plot((df1_swc_energy['site_long'][4:7],df1_swc_energy['ini_lon'][4:7]),(df1_swc_energy['site_lat'][4:7],df1_swc_energy['ini_lat'][4:7]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][4],df1_swc_energy['ini_lat'][4],s=size2,color='black')               # ESP_TIL_MIX
m.plot((df1_swc_energy['site_long'][7:8],df1_swc_energy['ini_lon'][7:8]),(df1_swc_energy['site_lat'][7:8],df1_swc_energy['ini_lat'][7:8]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][7],df1_swc_energy['ini_lat'][7],s=size2,color='black')               # IND_PON_STE
m.plot((df1_swc_energy['site_long'][8:10],df1_swc_energy['ini_lon'][8:10]),(df1_swc_energy['site_lat'][8:10],df1_swc_energy['ini_lat'][8:10]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][8],df1_swc_energy['ini_lat'][8],s=size2,color='black')               # ITA_MAT_S21* and ITA_FEI_S17
m.plot((df1_swc_energy['site_long'][10:11],df1_swc_energy['ini_lon'][10:11]),(df1_swc_energy['site_lat'][10:11],df1_swc_energy['ini_lat'][10:11]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][10],df1_swc_energy['ini_lat'][10],s=size2,color='black')             # ITA_MUN
m.plot((df1_swc_energy['site_long'][11:12],df1_swc_energy['ini_lon'][11:12]),(df1_swc_energy['site_lat'][11:12],df1_swc_energy['ini_lat'][11:12]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][11],df1_swc_energy['ini_lat'][11],s=size2,color='black')             # USA_DUK_HAR
m.plot((df1_swc_energy['site_long'][12:14],df1_swc_energy['ini_lon'][12:14]),(df1_swc_energy['site_lat'][12:14],df1_swc_energy['ini_lat'][12:14]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][12],df1_swc_energy['ini_lat'][12],s=size2,color='black')             # USA_SIL_OAK_*PR
m.plot((df1_swc_energy['site_long'][14:15],df1_swc_energy['ini_lon'][14:15]),(df1_swc_energy['site_lat'][14:15],df1_swc_energy['ini_lat'][14:15]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][14],df1_swc_energy['ini_lat'][14],s=size2,color='black')             # USA_TNB
m.plot((df1_swc_energy['site_long'][15:17],df1_swc_energy['ini_lon'][15:17]),(df1_swc_energy['site_lat'][15:17],df1_swc_energy['ini_lat'][15:17]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][15],df1_swc_energy['ini_lat'][15],s=size2,color='black')             # USA_TNO
m.plot((df1_swc_energy['site_long'][17:21],df1_swc_energy['ini_lon'][17:21]),(df1_swc_energy['site_lat'][17:21],df1_swc_energy['ini_lat'][17:21]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][17],df1_swc_energy['ini_lat'][17],s=size2,color='black')             # USA_TNP
m.plot((df1_swc_energy['site_long'][21],df1_swc_energy['ini_lon'][21]),(df1_swc_energy['site_lat'][21],df1_swc_energy['ini_lat'][21]),'-',color=coll,zorder=1)
m.scatter(df1_swc_energy['ini_lon'][21],df1_swc_energy['ini_lat'][21],s=size2,color='black')             # USA_WVF

m.scatter(df1_swc_energy['site_long'],df1_swc_energy['site_lat'],s=size1,edgecolor=[130/255,130/255,130/255],
          c=df1_swc_energy['swc_thr'],cmap='RdYlBu',vmin=df1['swc_thr'].min(),vmax=df1['swc_thr'].max(),linewidths=1)
m.scatter(df1_swc_energy['site_long'][5],df1_swc_energy['site_lat'][5],s=30,edgecolor=[0/255,0/255,0/255],
          c=df1_swc_energy['swc_thr'][5],cmap='RdYlBu',vmin=df1['swc_thr'].min(),vmax=df1['swc_thr'].max(),linewidths=1)
position = fig.add_axes([0.205,0.265,0.15,0.011])
cbar = plt.colorbar(cax=position,orientation='horizontal',shrink=0.5,ticks=[0,0.1,0.2,0.3,0.4,0.5])
plt.text(0.5,-0.01,r'$\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',color='black',fontdict={'size':9})
ax2.text(-176.2,78,'(c)',weight='bold',color='black',fontdict={'size':11})

#############################################################################################################################################

ax3 = fig.add_axes([0.56,0.213,length,width])
m = Basemap(projection='cyl', lon_0=lon_0, lat_0=lat_0)
m = Basemap(llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=179.5)
m.fillcontinents(color=[220/255,220/255,220/255], lake_color='none')

m.plot((df1_swc['site_long'][0:1],df1_swc['ini_lon'][0:1]),(df1_swc['site_lat'][0:1],df1_swc['ini_lat'][0:1]),'-',color=coll,zorder=1)
m.scatter(df1_swc['ini_lon'][0],df1_swc['ini_lat'][0],s=size2,color='black')             # GBR_ABE_PLO
m.plot((df1_swc['site_long'][1:6],df1_swc['ini_lon'][1:6]),(df1_swc['site_lat'][1:6],df1_swc['ini_lat'][1:6]),'-',color=coll,zorder=1)
m.scatter(df1_swc['ini_lon'][1],df1_swc['ini_lat'][1],s=size2,color='black')             # GUF_GUY_*
m.plot((df1_swc['site_long'][8:9],df1_swc['ini_lon'][8:9]),(df1_swc['site_lat'][8:9],df1_swc['ini_lat'][8:9]),'-',color=coll,zorder=1)
m.scatter(df1_swc['ini_lon'][8],df1_swc['ini_lat'][8],s=size2,color='black')             # USA_MOR_SF
m.plot((df1_swc['site_long'][9:14],df1_swc['ini_lon'][9:14]),(df1_swc['site_lat'][9:14],df1_swc['ini_lat'][9:14]),'-',color=coll,zorder=1)
m.scatter(df1_swc['ini_lon'][9],df1_swc['ini_lat'][9],s=size2,color='black')             # USA_PJS_P0*_AMB
m.plot((df1_swc['site_long'][14:16],df1_swc['ini_lon'][14:16]),(df1_swc['site_lat'][14:16],df1_swc['ini_lat'][14:16]),'-',color=coll,zorder=1)
m.scatter(df1_swc['ini_lon'][14],df1_swc['ini_lat'][14],s=size2,color='black')           # USA_SIL_OAK_*PR
m.plot((df1_swc['site_long'][16:17],df1_swc['ini_lon'][16:17]),(df1_swc['site_lat'][16:17],df1_swc['ini_lat'][16:17]),'-',color=coll,zorder=1)
m.scatter(df1_swc['ini_lon'][16],df1_swc['ini_lat'][16],s=size2,color='black')           # USA_TNB
m.plot((df1_swc['site_long'][17],df1_swc['ini_lon'][17]),(df1_swc['site_lat'][17],df1_swc['ini_lat'][17]),'-',color=coll,zorder=1)
m.scatter(df1_swc['ini_lon'][17],df1_swc['ini_lat'][17],s=size2,color='black')           # USA_TNP

m.scatter(df1_swc['site_long'],df1_swc['site_lat'],s=size1,edgecolor=[130/255,130/255,130/255],
          c=df1_swc['swc_thr'],cmap='RdYlBu',vmin=df1['swc_thr'].min(),vmax=df1['swc_thr'].max(),linewidths=1)
m.scatter(df1_swc['site_long'][10],df1_swc['site_lat'][10],s=30,edgecolor=[0/255,0/255,0/255],
          c=df1_swc['swc_thr'][10],cmap='RdYlBu',vmin=df1['swc_thr'].min(),vmax=df1['swc_thr'].max(),linewidths=1)
position = fig.add_axes([0.715,0.265,0.15,0.011])
cbar = plt.colorbar(cax=position,orientation='horizontal',shrink=0.5,ticks=[0,0.1,0.2,0.3,0.4,0.5])
plt.text(0.5,-0.01,r'$\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',color='black',fontdict={'size':9})
ax3.text(-176.2,78,'(d)',weight='bold',color='black',fontdict={'size':11})

#############################################################################################################################################

inpath  = 'C:/Users/songchaoqing/Desktop/plant_water_stress/example_drydowns/'
filelist = os.listdir(inpath); filelist = [x for x in filelist if ('deep' not in x)]

# example for energy-controlled, energy-dominated, swc-dominated and swc-controlled
filenames = [filelist[0],filelist[2],filelist[1],filelist[3]]
Es = ['Qro_Es_mm_day_y','Lgm_mean_y','Qil_Es_mm_day_y','Ped_Es_mm_day_y']
sp = ['Qro','Lgm','Qil','Ped']; cmap = ['ta_y','sw_in_y','sw_in_y','vpd_y']
ax = [0.26,0.77,0.26,0.77]; height = [0.56,0.56,0.052,0.052]
ydis = [0.2,2,1,0.1]; size=30; col1 = [150/255,150/255,150/255]; size1 = 35; length = 0.2
b0l = [-5.1833,-6.53,-4.268,-0.04311]; b1l = [20.38711,85.3518,40.976,1.5296]
c0l = [1.7047,6.5317,4.93,0.256]; c1l = [-2.45188,-16.5233,-11.837,-0.896]


for ii in range(len(filenames)):
    data    = pd.read_excel(inpath+filenames[ii]); site = filenames[ii][:-44]
    df_cmap = data[(data['precip']==0) & (data[Es[ii]]>0) & (data['swc_shallow']>0)]
    df_segment = df[(df['site']==site) & (df['species']==sp[ii])]; df_segment.index = np.arange(0,len(df_segment))
    swc_thr = df_segment['swc_thr'][0]
    b0 = b0l[ii]; b1 = b1l[ii]; c0 = c0l[ii]; c1 = c1l[ii]
    swc1 = np.arange(df_cmap['swc_shallow'].min(),swc_thr+0.000001,0.000001); y1 = b0 + b1*swc1
    swc2 = np.arange(swc_thr,df_cmap['swc_shallow'].max()+0.000001,0.000001); y2 = c0 + c1*swc2
    
    ax1 = fig.add_axes([ax[ii],height[ii],length,0.17])
    plt.scatter(df_cmap['swc_shallow'],df_cmap[Es[ii]],size,c=df_cmap[cmap[ii]],cmap=cmap1)
    plt.plot(swc1,y1,'--',color=col1); plt.plot(swc2,y2,'--',color=col1)
    plt.xticks(fontsize=11); plt.yticks(fontsize=11)
    x_major_locator = MultipleLocator(0.05); ax1.xaxis.set_major_locator(x_major_locator)
    y_major_locator = MultipleLocator(ydis[ii]); ax1.yaxis.set_major_locator(y_major_locator)
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    ax1.set_xlabel('SM ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',fontdict={'size':11},labelpad=6)
    if ii==1:
        ax1.set_ylabel('T$_{c}$ (cm $\mathregular{h^{-1}}$)',fontdict={'size':11},labelpad=4)
    else:
        ax1.set_ylabel('T$_{s}$ (mm $\mathregular{d^{-1}}$)',fontdict={'size':11},labelpad=4)
    cbar = plt.colorbar()
    if ii==3:
        cbar.set_label('VPD (kPa)',fontdict={'size':10},labelpad=7)
    elif ii==0: 
        cbar.set_label('Ta (C)',fontdict={'size':10},labelpad=7)
    elif ii==2:
        cbar.set_ticks([300,400,500,600])
        cbar.set_label('SR (W $\mathregular{m^{-2}}$)',fontdict={'size':10},labelpad=4)
    else:
        cbar.set_label('SR (W $\mathregular{m^{-2}}$)',fontdict={'size':10},labelpad=4)

#############################################################################################################################################

x_ticks = ['SM','VPD','SR','Ta','Energy']
col = [[0/255,0/255,0/255],[0/255,0/255,0/255],[0/255,0/255,0/255],[0/255,0/255,0/255],[200/25,200/255,200/255]]
medianprops1 = dict(linewidth=2.2,color=col,solid_capstyle="butt")
boxprops1    = dict(linewidth=1.2,color=col)

ax1 = fig.add_axes([0.05,0.56,0.15,0.17])
plt.hlines(0,0.5,5.5,colors=[170/255,170/255,170/255],linestyles='--',zorder=0)
plt.boxplot(df5_energy[['r_swc','r_vpd','r_sw','r_ta','r_energy']],showfliers=False,showcaps=False,
            medianprops={'color':'orange','linewidth':1.2})
plt.xticks(fontsize=11); plt.yticks(fontsize=11); plt.ylim(-0.6,1)
y_major_locator = MultipleLocator(0.5);  ax1.yaxis.set_major_locator(y_major_locator)
ax1.set_xticklabels(x_ticks)
ax1.set_ylabel('$\mathregular{R}$',fontdict={'size':11},labelpad=-5)

ax1 = fig.add_axes([0.56,0.56,0.15,0.17])
plt.hlines(0,0.5,5.5,colors=[170/255,170/255,170/255],linestyles='--',zorder=0)
plt.boxplot(df5_energy_swc[['r_swc','r_vpd','r_sw','r_ta','r_energy']],showfliers=False,showcaps=False,
            medianprops={'color':'orange','linewidth':1.2})
plt.xticks(fontsize=11); plt.yticks(fontsize=11); plt.ylim(-0.6,1)
y_major_locator = MultipleLocator(0.5);  ax1.yaxis.set_major_locator(y_major_locator)
ax1.set_xticklabels(x_ticks)
ax1.set_ylabel('$\mathregular{R}$',fontdict={'size':11},labelpad=-5)

ax1 = fig.add_axes([0.05,0.052,0.15,0.17])
plt.hlines(0,0.5,5.5,colors=[170/255,170/255,170/255],linestyles='--',zorder=0)
plt.boxplot(df5_swc_energy[['r_swc','r_vpd','r_sw','r_ta','r_energy']],showfliers=False,showcaps=False,
            medianprops={'color':'orange','linewidth':1.2})
plt.xticks(fontsize=11); plt.yticks(fontsize=11); plt.ylim(-0.6,1)
y_major_locator = MultipleLocator(0.5);  ax1.yaxis.set_major_locator(y_major_locator)
ax1.set_xticklabels(x_ticks)
ax1.set_ylabel('$\mathregular{R}$',fontdict={'size':11},labelpad=-5)

ax1 = fig.add_axes([0.56,0.052,0.15,0.17])
plt.hlines(0,0.5,5.5,colors=[170/255,170/255,170/255],linestyles='--',zorder=0)
plt.boxplot(df5_swc[['r_swc','r_vpd','r_sw','r_ta','r_energy']],showfliers=False,showcaps=False,
            medianprops={'color':'orange','linewidth':1.2})
plt.xticks(fontsize=11); plt.yticks(fontsize=11); plt.ylim(-0.6,1)
y_major_locator = MultipleLocator(0.5);  ax1.yaxis.set_major_locator(y_major_locator)
ax1.set_xticklabels(x_ticks)
ax1.set_ylabel('$\mathregular{R}$',fontdict={'size':11},labelpad=-5)

plt.show()
