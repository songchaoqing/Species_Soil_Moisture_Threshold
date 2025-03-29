# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 21:20:46 2023

@author: SY
"""

#!/usr/bin/env/python

# This program is used to identify the dry-down period for each site and species

import os
import pandas as pd
import numpy as np
import datetime

inpath = 'C:/Users/songchaoqing/Desktop/plant_water_stress/example/'; filelist = os.listdir(inpath)
outpath = 'C:/Users/songchaoqing/Desktop/plant_water_stress/example_drydowns/'

site_info = pd.read_excel('C:/Users/songchaoqing/Desktop/plant_water_stress/compare/sapflux_variable_stats.xlsx',sheet_name='site')
site_info = site_info[['site','site_lat','site_long']]
site_info.drop_duplicates(subset=['site'],inplace=True)
site_info = site_info.sort_values(by='site',axis=0); site_info.index = np.arange(0,len(site_info))

#%%

for ii in range(len(filelist)):
    
    site = filelist[ii][:-22]
    df = pd.read_csv(inpath+filelist[ii]); dfname = list(df.columns)
    
    df_pre = df[df['precip']>=0]; df_pre.index = np.arange(0,len(df_pre))
    # time interval/resolution
    date_begin = df_pre['loc_time'][0]; date_inter = df_pre['loc_time'][1]
    time_1 = datetime.datetime.strptime(date_begin,'%Y-%m-%d %H:%M')
    time_2 = datetime.datetime.strptime(date_inter,'%Y-%m-%d %H:%M')
    time_itval = int((time_2-time_1).total_seconds() / 60)
    
    # calculate the number of intervals with precip records in each day
    df_pre_idx = df_pre[['loc_date']].value_counts(); df_pre_idx = df_pre_idx.to_frame()
    df_pre_idx.reset_index(level=0,inplace=True)
    df_pre_idx.sort_values(by='loc_date',inplace=True); df_pre_idx.index = np.arange(0,len(df_pre_idx))
    df_pre_idx.rename(columns={'count':'day_tot_pre_itval'},inplace=True)
    # extract date with precip records less than 95% in a day
    df_pre_ext = df_pre_idx[df_pre_idx['day_tot_pre_itval']<int(60/time_itval*24*0.9)]
    df_pre_new = df_pre[~df_pre['loc_date'].isin(df_pre_ext['loc_date'])] if len(df_pre_ext)>0 else df_pre
    
    # calculate daytime transpiration (radiation>0, the radiation variable prioritizes using 'sw_in', followed by 'netrad')
    if 'sw_in' in dfname:
        sw_var = 'sw_in'
    elif ('sw_in' not in dfname) and ('netrad' in dfname):
        sw_var = 'netrad'
    else:
        sw_var = []
    
    if len(sw_var)>0:
        Es_var = [x for x in dfname if ('ta' in x) or ('vpd' in x) or (sw_var in x) or ('_mean' in x) or ('_mm_day' in x)]
    else:
        Es_var = [x for x in dfname if ('ta' in x) or ('vpd' in x) or ('_mean' in x) or ('_mm_day' in x)]
    
    if len(sw_var)>0:
        df_sw_in = df_pre_new[(df_pre_new[sw_var]>0)]
        df_sw_in = df_sw_in[(df_sw_in['loc_hour']>=6) & (df_sw_in['loc_hour']<18)]
        
        # calculate the number of intervals with sw_var>0 in each daytime
        df_sw_idx = df_sw_in[['loc_date']].value_counts(); df_sw_idx = df_sw_idx.to_frame()
        df_sw_idx.reset_index(level=0,inplace=True)
        df_sw_idx.sort_values(by='loc_date',inplace=True); df_sw_idx.index = np.arange(0,len(df_sw_idx))
        df_sw_idx.rename(columns={'count':'day_tot_sw_itval'},inplace=True)
        # extract date with sw_var records less than 4h in a daytime
        df_sw_ext = df_sw_idx[df_sw_idx['day_tot_sw_itval']<int(60/time_itval*24*0.2)]
        
        # calculate daytime mean transpiration
        df_sw_new = df_sw_in[~df_sw_in['loc_date'].isin(df_sw_ext['loc_date'])] if len(df_sw_ext)>0 else df_sw_in
        df_Es_daytime = df_sw_new.groupby(['loc_date'])[Es_var].mean()
        df_Es_daytime.reset_index(level=0,inplace=True)
        
        df_pre_new = df_pre_new[~df_pre_new['loc_date'].isin(df_sw_ext['loc_date'])] if len(df_sw_ext)>0 else df_pre_new
    
    # calculate daily total precipitation and mean transpiration
    df_pre_daily = df_pre_new.groupby(['loc_date'])['precip'].sum()
    df_pre_daily = pd.DataFrame(df_pre_daily)
    df_pre_daily.reset_index(level=0,inplace=True)
    
    df_Es_daily = df_pre_new.groupby(['loc_date'])[Es_var].mean()
    df_Es_daily.reset_index(level=0,inplace=True)
    
    # merge daily precipitation, daily transpiration and daytime transpiration
    df_pre_Es = pd.merge(df_pre_daily,df_Es_daily,on='loc_date',how='left')
    if len(sw_var)>0:
        df_pre_Es = pd.merge(df_pre_Es,df_Es_daytime,on='loc_date',how='left')
    
    # calculate the number of intervals with swc in each day
    swc_var = [x for x in dfname if 'swc' in x]
    # if len(swc_var)==0: continue      # no swc observation
    df_swc = df_pre_new[df_pre_new[swc_var[0]]>=0]
    
    # calculate daily mean swc and merge with df_pre_Es
    df_swc_daily = df_swc.groupby(['loc_date'])[swc_var].mean()
    df_swc_daily.reset_index(level=0,inplace=True)
    df_pre_Es_swc = pd.merge(df_pre_Es,df_swc_daily,on='loc_date',how='left')
    
    # create a complete time series and merge with df_pre_Es_swc
    date_begin = df_pre_Es_swc['loc_date'][0]; date_end = df_pre_Es_swc['loc_date'][len(df_pre_Es_swc)-1]
    dt = pd.date_range(start=date_begin,end=date_end,freq='D')
    dtnew = dt.strftime('%Y-%m-%d'); dttime = pd.DataFrame(); dttime['loc_date'] = dtnew
    dttime['day'] = np.arange(1,len(dttime)+1)
    df_pre_Es_swc = pd.merge(dttime,df_pre_Es_swc,on='loc_date',how='left')
    
    df_name = list(df_pre_Es_swc.columns)
    if len(swc_var)==1:
        df_name_new = df_name[0:3]+df_name[-1:]+df_name[3:-1]  # adjust variable location
    else:
        df_name_new = df_name[0:3]+df_name[-2:]+df_name[3:-2]
    df_pre_Es_swc = df_pre_Es_swc[df_name_new]
    
    df_pre_Es_swc['year']  = df_pre_Es_swc['loc_date'].str[0:4]; df_pre_Es_swc['year']  = df_pre_Es_swc['year'].astype('int')
    df_pre_Es_swc['month'] = df_pre_Es_swc['loc_date'].str[5:7]; df_pre_Es_swc['month'] = df_pre_Es_swc['month'].astype('int')
    df_pre_Es_swc['Date'] = pd.to_datetime(df_pre_Es_swc['loc_date']).dt.date       # discard hour-minute-second
    df_pre_Es_swc_name = list(df_pre_Es_swc.columns); df_pre_Es_swc_name = df_pre_Es_swc_name[-1:] + df_pre_Es_swc_name[:-1]
    df_pre_Es_swc = df_pre_Es_swc[df_pre_Es_swc_name]
    
    # dry-down period identification
    # outfile  = outpath+filelist[ii][:-4]+'_'+'swc_obs'+'_drydowns.xlsx'; writer = pd.ExcelWriter(outfile)
    df_pre_Es_swc_new = df_pre_Es_swc.copy()
    df_pre_Es_swc_new['iday'] = np.arange(1,len(df_pre_Es_swc_new)+1)
    
    # SMj+1 - SMj
    swc_var_new = [x+'_new' for x in swc_var]
    for kk in range(len(swc_var_new)):
        
        # no record values of swc_var[kk] in all days
        if df_pre_Es_swc_new[swc_var[kk]].isnull().values.all()!=True:
        
            # [1]: calculate SMj+1 - SMj
            df_pre_Es_swc_new[swc_var_new[kk]] = np.nan
            df_pre_Es_swc_new[swc_var_new[kk]][:len(df_pre_Es_swc_new)-1] = df_pre_Es_swc_new[swc_var[kk]][1:]
            df_pre_Es_swc_new[swc_var[kk]+'_diff'] = df_pre_Es_swc_new[swc_var_new[kk]]-df_pre_Es_swc_new[swc_var[kk]]
            
            # [2]: find days with SMj+1 - SMj > 0
            df_diff_ext = df_pre_Es_swc_new[(df_pre_Es_swc_new[swc_var[kk]+'_diff']>0)]
            # determine whether add the first/last day with not nan swc_diff (days with swc_diff>=0 may be intermediate days)
            beg_val = df_pre_Es_swc_new[swc_var[kk]+'_diff'].loc[~df_pre_Es_swc_new[swc_var[kk]+'_diff'].isnull()].iloc[0]
            end_val = df_pre_Es_swc_new[swc_var[kk]+'_diff'].loc[~df_pre_Es_swc_new[swc_var[kk]+'_diff'].isnull()].iloc[-1]
            if beg_val not in list(df_diff_ext[swc_var[kk]+'_diff']):
                aa = df_pre_Es_swc_new.loc[df_pre_Es_swc_new[swc_var[kk]+'_diff']==beg_val]
                # df_diff_ext = df_diff_ext.append(aa)
                df_diff_ext = pd.concat([df_diff_ext,aa],axis=0)
            if end_val not in list(df_diff_ext[swc_var[kk]+'_diff']):
                bb = df_pre_Es_swc_new.loc[df_pre_Es_swc_new[swc_var[kk]+'_diff']==end_val]
                # df_diff_ext = df_diff_ext.append(bb)
                df_diff_ext = pd.concat([df_diff_ext,bb],axis=0)
            df_diff_ext = df_diff_ext.sort_values(by='iday'); df_diff_ext.index = np.arange(0,len(df_diff_ext))
            
            if len(df_diff_ext)==0:
                df_dry_period = df_pre_Es_swc_new
                sheetname = 'ds'+'_'+swc_var[kk][4:8]
                # eval('df_dry_period').to_excel(excel_writer=writer,sheet_name=sheetname,index=False)
            else:
                df_dry_period = pd.DataFrame(); nn=0
                # [3]: determine if the intervals between days in condition [3] >= 10, if >= 10, retain them
                for mm in range(len(df_diff_ext)):
                    if mm==len(df_diff_ext)-1: break
                    iday1 = df_diff_ext['iday'][mm]; iday2 = df_diff_ext['iday'][mm+1]
                    if (iday2-iday1)>=10:
                        df_drydown = df_pre_Es_swc_new[(df_pre_Es_swc_new['iday']>iday1) & (df_pre_Es_swc_new['iday']<=iday2)]
                        if df_drydown[swc_var[kk]].count()<10: continue
                        nn = nn + 1
                        df_dry_period = df_drydown if nn==1 else pd.concat([df_dry_period,df_drydown],axis=0,ignore_index=True)
                
                if len(df_dry_period)>0:
                    sheetname = 'ds'+'_'+swc_var[kk][4:8]
                    # eval('df_dry_period').to_excel(excel_writer=writer,sheet_name=sheetname,index=False)
                else:
                    df_dry_period = pd.DataFrame(); sheetname = 'na'
                    # eval('df_dry_period').to_excel(excel_writer=writer,sheet_name=sheetname,index=False)
        else:
            df_dry_period = pd.DataFrame(); sheetname = 'na'
            # eval('df_dry_period').to_excel(excel_writer=writer,sheet_name=sheetname,index=False)
    # writer.close(); print(ii)
    
    # if sheetname == 'na': continue
    # limit to growing season (5-9 months for northern hemisphere, 11-12 and 1-3 months for southern hemisphere)
    lat = site_info.loc[site_info['site']==site,'site_lat'].item()
    if lat>20:
        data = df_dry_period[(df_dry_period['month']>=5)  & (df_dry_period['month']<=9)]
    elif lat<-20:
        data = df_dry_period[(df_dry_period['month']>=11) & (df_dry_period['month']<=12) | (df_dry_period['month']>=1) & (df_dry_period['month']<=3)]
    else:
        data = df_dry_period
    data.index = np.arange(0,len(data))
    
    # limit to peaking growing season (summer)
    if lat>20:
        data1 = df_dry_period[(df_dry_period['month']>=6)  & (df_dry_period['month']<=8)]
    elif lat<-20:
        data1 = df_dry_period[(df_dry_period['month']==12) | (df_dry_period['month']==1) | (df_dry_period['month']==2)]
    else:
        data1 = df_dry_period
    
    outfile = outpath + filelist[ii][0:-4]+'_'+swc_var[0]+'_drydowns'+'.xlsx'
    writer  = pd.ExcelWriter(outfile)
    eval('data').to_excel(excel_writer=writer,sheet_name='growing_season',index=False)
    eval('data1').to_excel(excel_writer=writer,sheet_name='growing_peak',index=False)
    writer.close()
