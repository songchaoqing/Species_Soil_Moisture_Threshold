# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 04:11:39 2025

@author: songchaoqing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from mpl_toolkits.basemap import Basemap

df = pd.read_excel('C:/Users/songchaoqing/Desktop/plant_water_stress/3_site_species_theta_threshold.xlsx')

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

#%% plot

fig = plt.figure(figsize=(13,11.5)); size1=35; size2=50; coll=[170/255,170/255,170/255]; lat_0=0; lon_0=0

ax0 = fig.add_axes([0,0.5,1,0.45])
m = Basemap(projection='cyl', lon_0=lon_0, lat_0=lat_0)
m = Basemap(llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=179.5)
m.fillcontinents(color=[220/255,220/255,220/255], lake_color='none')

m.plot((float(df1['site_long'][0:1]),-80.3574),(float(df1['site_lat'][0:1]),42.7098),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][1:2]),-80.3574),(float(df1['site_lat'][1:2]),42.7098),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][2:3]),-80.3574),(float(df1['site_lat'][2:3]),42.7098),'-',color=coll,zorder=1)
m.scatter(df['site_long'][0:1],df['site_lat'][0:1],s=20,color='black')                   # CAN_TUR_P*

m.plot((float(df1['site_long'][3:4]),16.94638),(float(df1['site_lat'][3:4]),48.68166),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][4:5]),16.94638),(float(df1['site_lat'][4:5]),48.68166),'-',color=coll,zorder=1)
m.scatter(df['site_long'][3:4],df['site_lat'][3:4],s=20,color='black')                   # CZE_LAN

m.plot((float(df1['site_long'][6:7]),17.97),(float(df1['site_lat'][6:7]),49.0358),'-',color=coll,zorder=1)
m.scatter(df['site_long'][6:7],df['site_lat'][6:7],s=20,color='black')                   # CZE_STI

m.plot((float(df1['site_long'][8:9]),-2.3283),(float(df1['site_lat'][8:9]),40.7769),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][9:10]),-2.3283),(float(df1['site_lat'][9:10]),40.7769),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][10:11]),-2.3283),(float(df1['site_lat'][10:11]),40.7769),'-',color=coll,zorder=1)
m.scatter(df['site_long'][8:9],df['site_lat'][8:9],s=20,color='black')                   # ESP_ALT_ARM

m.plot((float(df1['site_long'][11:12]),2.073611),(float(df1['site_lat'][11:12]),41.430989),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][12:13]),2.073611),(float(df1['site_lat'][12:13]),41.430989),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][13:14]),2.073611),(float(df1['site_lat'][13:14]),41.430989),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][14:15]),2.073611),(float(df1['site_lat'][14:15]),41.430989),'-',color=coll,zorder=1)
m.scatter(df['site_long'][11:12],df['site_lat'][11:12],s=20,color='black')               # ESP_CAN

m.plot((float(df1['site_long'][15:16]),1.0144288),(float(df1['site_lat'][15:16]),41.33262995),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][16:17]),1.0144288),(float(df1['site_lat'][16:17]),41.33262995),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][17:18]),1.0144288),(float(df1['site_lat'][17:18]),41.33262995),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][18:19]),1.0144288),(float(df1['site_lat'][18:19]),41.33262995),'-',color=coll,zorder=1)
m.scatter(df['site_long'][15:16],df['site_lat'][15:16],s=20,color='black')               # ESP_TIL_MIX

m.plot((float(df1['site_long'][19:20]),1.81356),(float(df1['site_lat'][19:20]),42.1961),'-',color=coll,zorder=1)
m.scatter(df['site_long'][19:20],df['site_lat'][19:20],s=20,color='black')               # ESP_VAL_SOR

m.plot((float(df1['site_long'][21:22]),-3.8),(float(df1['site_lat'][21:22]),56.616),'-',color=coll,zorder=1)
m.scatter(df['site_long'][21:22],df['site_lat'][21:22],s=20,color='black')               # GBR_ABE_PLO

m.plot((float(df1['site_long'][22:23]),-3.71677),(float(df1['site_lat'][22:23]),56.0333),'-',color=coll,zorder=1)
m.scatter(df['site_long'][22:23],df['site_lat'][22:23],s=20,color='black')               # GBR_DEV_DRO

m.plot((float(df1['site_long'][23:24]),-4.81667),(float(df1['site_lat'][23:24]),57.2667),'-',color=coll,zorder=1)
m.scatter(df['site_long'][23:24],df['site_lat'][23:24],s=20,color='black')               # GBR_GUI_ST1

m.plot((float(df1['site_long'][24:25]),-52.91),(float(df1['site_lat'][24:25]),5.281),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][25:26]),-52.91),(float(df1['site_lat'][25:26]),5.281),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][26:27]),-52.91),(float(df1['site_lat'][26:27]),5.281),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][27:28]),-52.91),(float(df1['site_lat'][27:28]),5.281),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][28:29]),-52.91),(float(df1['site_lat'][28:29]),5.281),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][29:30]),-52.91),(float(df1['site_lat'][29:30]),5.281),'-',color=coll,zorder=1)
m.scatter(df['site_long'][24:25],df['site_lat'][24:25],s=20,color='black',zorder=2)      # GUF_GUY_*

m.plot((float(df1['site_long'][30:31]),120.057),(float(df1['site_lat'][30:31]),-1.494),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][31:32]),120.057),(float(df1['site_lat'][31:32]),-1.494),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][32:33]),120.057),(float(df1['site_lat'][32:33]),-1.494),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][33:34]),120.057),(float(df1['site_lat'][33:34]),-1.494),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][34:35]),120.057),(float(df1['site_lat'][34:35]),-1.494),'-',color=coll,zorder=1)
m.scatter(df['site_long'][30:31],df['site_lat'][30:31],s=20,color='black',zorder=2)      # IND_PON_STE

m.plot((float(df1['site_long'][35:36]),10.69086),(float(df1['site_lat'][35:36]),46.74),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][36:37]),10.69086),(float(df1['site_lat'][36:37]),46.74),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][37:38]),10.69086),(float(df1['site_lat'][37:38]),46.74),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][38:39]),10.69086),(float(df1['site_lat'][38:39]),46.74),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][39:40]),10.69086),(float(df1['site_lat'][39:40]),46.74),'-',color=coll,zorder=1)
m.scatter(df['site_long'][35:36],df['site_lat'][35:36],s=20,color='black')               # ITA_MAT_S21* and ITA_FEI_S17

m.plot((float(df1['site_long'][40:41]),7.56089),(float(df1['site_lat'][40:41]),45.8238),'-',color=coll,zorder=1)
m.scatter(df['site_long'][40:41],df['site_lat'][40:41],s=20,color='black')               # ITA_TOR

m.plot((float(df1['site_long'][42:43]),92.95),(float(df1['site_lat'][42:43]),56.36),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][43:44]),92.95),(float(df1['site_lat'][43:44]),56.36),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][44:45]),92.95),(float(df1['site_lat'][44:45]),56.36),'-',color=coll,zorder=1)
m.scatter(df['site_long'][42:43],df['site_lat'][42:43],s=20,color='black')               # RUS_POG_VAR

m.plot((float(df1['site_long'][45:46]),17.476),(float(df1['site_lat'][45:46]),60.083),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][46:47]),17.476),(float(df1['site_lat'][46:47]),60.083),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][47:48]),17.476),(float(df1['site_lat'][47:48]),60.083),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][48:49]),17.476),(float(df1['site_lat'][48:49]),60.083),'-',color=coll,zorder=1)
m.scatter(df['site_long'][45:46],df['site_lat'][45:46],s=20,color='black')               # SWE_NOR_ST*

m.plot((float(df1['site_long'][50:51]),-79.094),(float(df1['site_lat'][50:51]),36.978),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][51:52]),-79.094),(float(df1['site_lat'][51:52]),36.978),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][52:53]),-79.094),(float(df1['site_lat'][52:53]),36.978),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][53:54]),-79.094),(float(df1['site_lat'][53:54]),36.978),'-',color=coll,zorder=1)
m.scatter(df['site_long'][50:51],df['site_lat'][50:51],s=20,color='black',zorder=2)      # USA_DUK_HAR

m.plot((float(df1['site_long'][54:55]),-78.8642),(float(df1['site_lat'][54:55]),36.2173),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][55:56]),-78.8642),(float(df1['site_lat'][55:56]),36.2173),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][56:57]),-78.8642),(float(df1['site_lat'][56:57]),36.2173),'-',color=coll,zorder=1)
m.scatter(df['site_long'][54:55],df['site_lat'][54:55],s=20,color='black',zorder=2)      # USA_HIL_HF*

m.plot((float(df1['site_long'][58:59]),-86.4132),(float(df1['site_lat'][58:59]),39.3232),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][59:60]),-86.4132),(float(df1['site_lat'][59:60]),39.3232),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][60:61]),-86.4132),(float(df1['site_lat'][60:61]),39.3232),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][61:62]),-86.4132),(float(df1['site_lat'][61:62]),39.3232),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][62:63]),-86.4132),(float(df1['site_lat'][62:63]),39.3232),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][63:64]),-86.4132),(float(df1['site_lat'][63:64]),39.3232),'-',color=coll,zorder=1)
m.scatter(df['site_long'][58:59],df['site_lat'][58:59],s=20,color='black',zorder=2)      # USA_INM and USA_MOR_SF

m.plot((float(df1['site_long'][64:65]),-76.6679),(float(df1['site_lat'][64:65]),35.8031),'-',color=coll,zorder=1)
m.scatter(df['site_long'][64:65],df['site_lat'][64:65],s=20,color='black',zorder=2)      # USA_PAR_FER

m.plot((float(df1['site_long'][65:66]),-106.529),(float(df1['site_lat'][65:66]),34.3864),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][66:67]),-106.529),(float(df1['site_lat'][66:67]),34.3864),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][67:68]),-106.529),(float(df1['site_lat'][67:68]),34.3864),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][68:69]),-106.529),(float(df1['site_lat'][68:69]),34.3864),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][69:70]),-106.529),(float(df1['site_lat'][69:70]),34.3864),'-',color=coll,zorder=1)
m.scatter(df['site_long'][65:66],df['site_lat'][65:66],s=20,color='black',zorder=2)      # USA_PJS_P0*_AMB

m.plot((float(df1['site_long'][70:71]),-74.5956),(float(df1['site_lat'][70:71]),39.9156),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][71:72]),-74.5956),(float(df1['site_lat'][71:72]),39.9156),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][72:73]),-74.5956),(float(df1['site_lat'][72:73]),39.9156),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][73:74]),-74.5956),(float(df1['site_lat'][73:74]),39.9156),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][74:75]),-74.5956),(float(df1['site_lat'][74:75]),39.9156),'-',color=coll,zorder=1)
m.scatter(df['site_long'][70:71],df['site_lat'][70:71],s=20,color='black')               # USA_SIL_OAK_*PR

m.plot((float(df1['site_long'][75:76]),-89.3477),(float(df1['site_lat'][75:76]),46.242),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][76:77]),-89.3477),(float(df1['site_lat'][76:77]),46.242),'-',color=coll,zorder=1)
m.scatter(df['site_long'][75:76],df['site_lat'][75:76],s=20,color='black')               # USA_SYL_HL2

m.plot((float(df1['site_long'][77:78]),-84.7041),(float(df1['site_lat'][77:78]),36.4712),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][78:79]),-84.7041),(float(df1['site_lat'][78:79]),36.4712),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][79:80]),-84.7041),(float(df1['site_lat'][79:80]),36.4712),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][80:81]),-84.7041),(float(df1['site_lat'][80:81]),36.4712),'-',color=coll,zorder=1)
m.scatter(df['site_long'][77:78],df['site_lat'][77:78],s=20,color='black')               # USA_TNB

m.plot((float(df1['site_long'][81:82]),-84.2819),(float(df1['site_lat'][81:82]),35.966),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][82:83]),-84.2819),(float(df1['site_lat'][82:83]),35.966),'-',color=coll,zorder=1)
m.scatter(df['site_long'][81:82],df['site_lat'][81:82],s=20,color='black')               # USA_TNO

m.plot((float(df1['site_long'][83:84]),-84.2879),(float(df1['site_lat'][83:84]),35.9604),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][84:85]),-84.2879),(float(df1['site_lat'][84:85]),35.9604),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][85:86]),-84.2879),(float(df1['site_lat'][85:86]),35.9604),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][86:87]),-84.2879),(float(df1['site_lat'][86:87]),35.9604),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][87:88]),-84.2879),(float(df1['site_lat'][87:88]),35.9604),'-',color=coll,zorder=1)
m.scatter(df['site_long'][83:84],df['site_lat'][83:84],s=20,color='black')               # USA_TNP

m.plot((float(df1['site_long'][88:89]),-83.5012),(float(df1['site_lat'][88:89]),35.6876),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][89:90]),-83.5012),(float(df1['site_lat'][89:90]),35.6876),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][90:91]),-83.5012),(float(df1['site_lat'][90:91]),35.6876),'-',color=coll,zorder=1)
m.scatter(df['site_long'][88:89],df['site_lat'][88:89],s=20,color='black')               # USA_TNY

m.plot((float(df1['site_long'][91:92]),-84.6975),(float(df1['site_lat'][91:92]),45.5625),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][92:93]),-84.6975),(float(df1['site_lat'][92:93]),45.5625),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][93:94]),-84.6975),(float(df1['site_lat'][93:94]),45.5625),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][94:95]),-84.6975),(float(df1['site_lat'][94:95]),45.5625),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][95:96]),-84.6975),(float(df1['site_lat'][95:96]),45.5625),'-',color=coll,zorder=1)
m.scatter(df['site_long'][91:92],df['site_lat'][91:92],s=20,color='black')               # USA_UMB_GIR and USA_UMB_CON

m.plot((float(df1['site_long'][96:97]),-90.0867),(float(df1['site_lat'][96:97]),45.8131),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][97:98]),-90.0867),(float(df1['site_lat'][97:98]),45.8131),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][98:99]),-90.0867),(float(df1['site_lat'][98:99]),45.8131),'-',color=coll,zorder=1)
m.scatter(df['site_long'][96:97],df['site_lat'][96:97],s=20,color='black')               # USA_WIL_WC1

m.plot((float(df1['site_long'][99:100]),-79.6907),(float(df1['site_lat'][99:100]),39.0589),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][100:101]),-79.6907),(float(df1['site_lat'][100:101]),39.0589),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][101:102]),-79.6907),(float(df1['site_lat'][101:102]),39.0589),'-',color=coll,zorder=1)
m.plot((float(df1['site_long'][102:103]),-79.6907),(float(df1['site_lat'][102:103]),39.0589),'-',color=coll,zorder=1)
m.scatter(df['site_long'][99:100],df['site_lat'][99:100],s=20,color='black')               # USA_WVF

m.scatter(df1['site_long'],df1['site_lat'],s=40,edgecolor=[130/255,130/255,130/255],c=df1['swc_thr'],cmap='RdYlBu',linewidths=1)
position = fig.add_axes([0.435,0.53,0.29,0.016])
cbar = plt.colorbar(cax=position,orientation='horizontal',shrink=0.5,ticks=[0,0.1,0.2,0.3,0.4,0.5])
cbar.ax.tick_params(labelsize=11)
plt.text(0.50,0.1,r'$\mathregular{\theta_{crit}}$ ($\mathregular{m^{3}}$ $\mathregular{m^{-3}}$)',color='black',fontdict={'size':11})

swc_thr = df1['swc_thr']
ax1 = fig.add_axes([0.115,0.528,0.19,0.15])
hist2, bin2 = np.histogram(swc_thr,bins=5,range=(0,0.5),density=True)
ax1.hist(bin2[:-1], bin2, weights=hist2, facecolor='white',alpha=1, edgecolor=[30/255,30/255,30/255])
mu = swc_thr.mean()
sigma = swc_thr.std()
x = np.linspace(swc_thr.min(),swc_thr.max(),100)
ndf = np.exp(-(x-mu)**2/(2*sigma**2))/(sigma * np.sqrt(2 * np.pi))
ax1.plot(x, ndf, 'r-')
plt.ylabel('PDF',fontdict={'size':11},labelpad=4)
plt.xticks(fontsize=11); plt.yticks(fontsize=11)
y_major_locator = MultipleLocator(2); ax1.yaxis.set_major_locator(y_major_locator)
ax1.spines['top'].set_visible(False); ax1.spines['right'].set_visible(False)

plt.show()
