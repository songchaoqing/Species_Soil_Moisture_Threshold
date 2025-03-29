# load library
library(ggplot2); library(segmented); library(readxl); library(stringr)

# read data
inpath  = 'C:/Users/songchaoqing/Desktop/plant_water_stress/example_drydowns/'
outpath = 'C:/Users/songchaoqing/Desktop/plant_water_stress/example_drydowns/'
dryf <- list.files(inpath,pattern='shallow_drydowns',full.names=TRUE)

# read site variables info
site_info = read_xlsx('C:/Users/songchaoqing/Desktop/plant_water_stress/compare/sapflux_variable_stats.xlsx')
col_name = c("site",'lat','lon','species','period','Es',"date_begin","date_end",'swc_thr','swc_thr_err','b0','b1','c0','c1',
             'p_swc_shal','p_icpt','R2','R2adj','std_err')
ds = data.frame(matrix(vector(),0,19,dimnames=list(c(),col_name)),stringsAsFactors=F)

for (ii in 1:length(dryf)){
  
  site = str_sub(dryf[ii],67,-45) # change 67 and -45 to capture the corresponding site char or run the below
  # ii = 2; site = 'ESP_TIL_OAK'; if (ii!=2) {next}    # as an example
  nums = excel_sheets(dryf[ii]); if (nums[1]=='Sheet1'){next}
  
  for (jj in 1:length(nums)){
    
    # read dry down data
    df = read_xlsx(dryf[ii],sheet=nums[jj]); if (nrow(df)<7) {next}
    day_begin = df$day[1]; day_end = df$day[nrow(df)]
    
    # find the species's daytime Es variables (one site may include multiple species)
    col_name = colnames(df)
    Es_stand_name = col_name[str_detect(col_name,'mm_day_y')]
    Es_mean_name  = col_name[str_detect(col_name,'mean_y')]
    
    # ******************************* species loop **********************************
    for (kk in 1:length(Es_stand_name)){
      
      sp_name = substring(Es_stand_name[kk],1,3)
      sp_basal_perc = as.numeric(site_info[site_info$site==site & site_info$sp==sp_name,'sp_basal_area_perc'])
      st_basal_area = as.numeric(site_info[site_info$site==site & site_info$sp==sp_name,'st_basal_area'])
      lat = as.numeric(site_info[site_info$site==site & site_info$sp==sp_name,'site_lat'])
      lon = as.numeric(site_info[site_info$site==site & site_info$sp==sp_name,'site_long'])
      
      # revise the name of Es of a species to conduct linear and segmented regression
      if (is.na(sp_basal_perc)==FALSE && is.na(st_basal_area)==FALSE){
        colnames(df)[which(names(df)==Es_stand_name[kk])] <- "Es_mm_d"    # stand level Td
        Es_name = Es_stand_name[kk]; Es = 'stand'
      }else{
        colnames(df)[which(names(df)==Es_mean_name[kk])] <- "Es_mm_d"     # basal area weighted Td
        Es_name = Es_mean_name[kk]; Es = 'mean'
      }
      
      dfnew <- df[!is.na(df$swc_shallow) & !is.na(df$Es_mm_d), ]
      dfnew = dfnew[dfnew$precip==0 & dfnew$Es_mm_d>0,]
      
      # create the linear regression model and plot
      lm1 = try(model.lm <- lm(Es_mm_d ~ swc_shallow,data=dfnew),silent=TRUE)
      
      if (class(lm1)=='try-error'){
        next
      }else{
        # create the segmented linear regression model and plot
        seg1 = try(model.segmented <- segmented(model.lm,seg.Z=~swc_shallow),silent=TRUE)
        if (class(seg1)[1]=='try-error' || class(seg1)[1]=='lm'){    # for no segmented || for no break point
          ds = rbind(ds, data.frame("site"=site,'lat'=lat,'lon'=lon,'species'=sp_name,'period'=nums[jj],
                                    'Es'=Es,"day_begin"=day_begin,"day_end"=day_end,
                                    "swc_thr"=999,"swc_thr_err"=999,'b0'=999,'b1'=999,'c0'=999,'c1'=999,
                                    "p_swc_shal"=999,"p_icpt"=999,"R2"=999,"R2adj"=999,"std_err"=999))
          next
        }else{
          bb=summary(model.segmented)
          
          # obtain variable and output
          swc_thr     = round(bb[["psi"]][1,2],3)            # SWC threshold
          swc_thr_err = round(bb[["psi"]][1,3],3)            # SWC threshold error
          b0          = coef(model.segmented)[[1]]           # intercept
          b1          = coef(model.segmented)[[2]]           # slop
          c1          = coef(model.segmented)[[2]] + coef(model.segmented)[[3]]     # slop
          c0          = b0 + b1*bb[["psi"]][1,2] - c1*bb[["psi"]][1,2]              # intercept
          p_itcept    = round(bb[['coefficients']][1,4],3)   # significance
          p_swc_shal  = round(bb[['coefficients']][2,4],3)   # significance
          R2          = round(bb[["r.squared"]],3)
          R2adj       = round(bb[["adj.r.squared"]],3)
          std_err     = round(bb[["sigma"]],3)
          
          ds = rbind(ds, data.frame("site"=site,'lat'=lat,'lon'=lon,'species'=sp_name,'period'=nums[jj],
                                    'Es'=Es,"day_begin"=day_begin,"day_end"=day_end,
                                    "swc_thr"=swc_thr,"swc_thr_err"=swc_thr_err,'b0'=b0,'b1'=b1,'c0'=c0,'c1'=c1,
                                    "p_swc_shal"=p_swc_shal,"p_icpt"=p_itcept,"R2"=R2,"R2adj"=R2adj,"std_err"=std_err))
          
          # save the plot when segmented linear regression meets requires
          pngname = paste(site,sp_name,nums[jj],Es,'Es_swc_shallow_thr.png',sep='_')
          png(filename=paste(outpath,pngname,sep='/'),width=1000, height=1000, units="px",res=200)

          if (is.na(p_itcept)==FALSE && is.na(p_swc_shal)==FALSE){
            if (p_swc_shal<0.05){
              plot(model.segmented,xlab='swc_shallow',ylab=Es_name,col='blue',ylim=c(min(dfnew$Es_mm_d,na.rm=TRUE),max(dfnew$Es_mm_d,na.rm=TRUE)))
            }else{
              plot(model.segmented,xlab='swc_shallow',ylab=Es_name,col='orange',ylim=c(min(dfnew$Es_mm_d,na.rm=TRUE),max(dfnew$Es_mm_d,na.rm=TRUE)))
            }
          }else{
            plot(dfnew$swc_shallow,dfnew$Es_mm_d,col='black',xlab='swc_shallow',ylab=Es_name)
          }
          points(Es_mm_d~swc_shallow,data=dfnew)
          dev.off()
          
        }
      }
      
      # change back to the initial name
      if (is.na(sp_basal_perc)==FALSE && is.na(st_basal_area)==FALSE){
        colnames(df)[which(names(df)=="Es_mm_d")] <- Es_stand_name[kk]    # stand level Td
      }else{
        colnames(df)[which(names(df)=="Es_mm_d")] <- Es_mean_name[kk]     # basal area weighted Td
      }
      
    }
    
  }
  print(ii)
}

write.csv(ds,file=paste(outpath,'swc_threshold_with_obs_shallow.csv',sep='/'),row.names=FALSE)
