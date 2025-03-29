# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 03:39:16 2025

@author: songchaoqing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

infile  = 'C:/Users/songchaoqing/Desktop/plant_water_stress/1_studied_site_and_species_info.csv'
df = pd.read_csv(infile)
df.sort_values(by='species_number',ascending=False,inplace=True); df.index = np.arange(0,len(df))
# divide measured period
df['per'] = df['measure_time_begin'].apply(lambda x: 1 if x<2000 else 2 if x<2010 else 3)
data1 = df[df['per']==1]; data2 = df[df['per']==2]; data3 = df[df['per']==3]
data2.index = np.arange(0,len(data2)); data3.index = np.arange(0,len(data3))

#%% plot

col = [[239/255,35/255,0/255],[200/255,86/255,202/255],[65/255,118/255,178/255]]; lat_0 = 0; lon_0 = 0
fig = plt.figure(figsize=(12,9))

# subfig1
ax1 = fig.add_axes([0.03,0.63,0.27,0.3])
ax1.plot((0,0.598),(0.6,0.6),linestyle='-',linewidth=2.7,color=col[2])
ax1.plot((0.603,1),(0.598,0),linestyle='-',linewidth=2.7,color=col[0])
ax1.plot((0.6,0.6),(-0.1,1.2),'--',linewidth=2.2,dashes=(3,2),color=[170/255,170/255,170/255])
ax1.set_xlim(-0.1,1.1); ax1.set_ylim(-0.1,0.8)
ax1.spines['top'].set_visible(False); ax1.spines['right'].set_visible(False)
ax1.set_xticks([]); ax1.set_yticks([]); ax1.set_xticklabels([]); ax1.set_yticklabels([])
plt.annotate('',xy=(1.06, 0), xycoords='axes fraction',xytext=(-0.06, 0), textcoords='axes fraction',
              arrowprops=dict(facecolor='black', shrink=0.03,headwidth=5,headlength=7,width=0.2),zorder=5)
plt.annotate('',xy=(0, 1.06), xycoords='axes fraction',xytext=(0, -0.06), textcoords='axes fraction',
              arrowprops=dict(facecolor='black', shrink=0.03,headwidth=5,headlength=7,width=0.2),zorder=5)
ax1.set_xlabel('Decreasing SM',color='black',fontdict={'size':10},labelpad=8)
ax1.set_ylabel('Increasing ET',color='black',fontdict={'size':10},labelpad=6.8)
ax1.text(0.1,0.77,'Energy-limited',color='black',fontdict={'size':11})
ax1.text(0.7,0.77,'Water-limited',color='black',fontdict={'size':11})
ax1.text(0.62,-0.07,r'$\regular{\theta_{crit}}$',color='black',fontdict={'size':11})
ax1.text(0.22,0.63,r'ET$_{max}$',color='black',fontdict={'size':11})
ax1.text(-0.068,0.82,'(a)',weight='bold',color='black',fontdict={'size':11})

# subfig2
ax0 = fig.add_axes([0.315,0.6,0.7,0.36])
m = Basemap(projection='cyl',lon_0=lon_0,lat_0=lat_0)
m = Basemap(llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=179.5)
m.drawcoastlines(color=[190/255,190/255,190/255],linewidth=0.7,zorder=0)
m.shadedrelief(scale=0.5,alpha=1)
m.scatter(data1['site_long'],data1['site_lat'],s=data1['species_number']*40,edgecolor=col[0],facecolor='none',linewidths=1.2,label='1990s')
m.scatter(data2['site_long'],data2['site_lat'],s=data2['species_number']*40,edgecolor=col[1],facecolor='none',linewidths=1.2,label='2000s')
m.scatter(data3['site_long'],data3['site_lat'],s=data3['species_number']*40,edgecolor=col[2],facecolor='none',linewidths=1.2,label='2010s')

# these two ax2 only for obtaining legend
ax2 = fig.add_axes([0.48,0.61,0,0]); ax = 5
m1 = Basemap(projection='cyl',lon_0=lon_0,lat_0=lat_0)
m1 = Basemap(llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=179.5)
m1.drawcoastlines(color=[180/255,180/255,180/255],linewidth=0.7)
m1.scatter(data2['site_long'][ax],data2['site_lat'][ax],s=data2['species_number'][ax]*40,edgecolor=col[0],facecolor='none',linewidths=1.2,label='1990s')
m1.scatter(data2['site_long'][ax],data2['site_lat'][ax],s=data2['species_number'][ax]*40,edgecolor=col[1],facecolor='none',linewidths=1.2,label='2000s')
m1.scatter(data2['site_long'][ax],data2['site_lat'][ax],s=data2['species_number'][ax]*40,edgecolor=col[2],facecolor='none',linewidths=1.2,label='2010s')
plt.legend(loc='lower right',bbox_to_anchor=(0.2,0.1),frameon=False,ncol=1,handletextpad=0.2,labelspacing=1,title='Period')

ax2 = fig.add_axes([0.412,0.61,0,0])
m = Basemap(projection='cyl',lon_0=lon_0,lat_0=lat_0)
m = Basemap(llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=179.5)
m.drawcoastlines(color=[180/255,180/255,180/255],linewidth=0.7)
m.scatter(data2['site_long'][28],data2['site_lat'][28],s=data2['species_number'][28]*40,edgecolor='black',facecolor='none',linewidths=1.2,label='1')
m.scatter(data2['site_long'][5], data2['site_lat'][5], s=data2['species_number'][5]*40, edgecolor='black',facecolor='none',linewidths=1.2,label='4')
m.scatter(data2['site_long'][0], data2['site_lat'][0], s=data2['species_number'][0]*40, edgecolor='black',facecolor='none',linewidths=1.2,label='8')
plt.legend(loc='lower right',bbox_to_anchor=(0.2,0.1),frameon=False,ncol=1,handletextpad=0.2,labelspacing=1,title='Species')
ax0.text(-176.2,80,'(b)',weight='bold',color='black',fontdict={'size':11})

plt.show()
# plt.savefig('Fig1.png',dpi=500)