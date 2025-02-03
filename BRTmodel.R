# load library
library(readxl); library(dismo); library(gbm); library(pdp); library(dplyr)

# read data
inpath   = 'C:/Users/Desktop/'
outpath  = 'C:/Users/Desktop/'
df = read_xlsx(paste(inpath,'3_site_species_theta_threshold.xlsx',sep='/'))
df = as.data.frame(df)

########################################### all 23 variables ####################################################
swc_thr0 <- gbm.step(
  data=df,
  gbm.x=c("site_mat","site_map","site_elev",'stand_basal_area','stand_height','stand_density',
          'stand_lai',"stand_age","stand_sand_perc","stand_clay_perc","stand_silt_perc",
          "pl_median_dbh","pl_median_sapwarea",'WD',"Ks","P50","Hmax",
          'ta_od','vpd_od','precip1_od','sw_in_od','ws_od','swc_shal_od'),
  gbm.y="swc_thr",
  family="gaussian",
  tree.complexity=5, learning.rate=0.005, bag.fraction=0.5,
  n.folds=10,
  tolerance=0.01, tolerance.method='auto'
)
thr0 = summary(swc_thr0)

dismo::gbm.plot(swc_thr0,smooth=T,rug=F,common.scale=F,
                x.label='1',y.label='Partial effect',
                show.contrib=T,plot.layout=c(2,4),cex.axis=1.2, cex.lab=1.2,las=2,
                mgp=c(3,0.3,0),tck=0.05
)

############################# selected variables based on above running program #################################
swc_thr1 <- gbm.step(
  data=df,
  gbm.x=c('swc_shal_od','stand_basal_area','stand_height','stand_density','site_elev',
          "pl_median_sapwarea",'WD',"vpd_od",'precip1_od'),
  gbm.y="swc_thr",
  family="gaussian",
  tree.complexity=5, learning.rate=0.005, bag.fraction=0.5,
  n.folds=10,
  tolerance=0.01, tolerance.method='auto'
)
thr1 = summary(swc_thr1)
write.csv(thr1,file=paste(outpath,'BRT_result.csv',sep='/'),row.names=FALSE)

dismo::gbm.plot(swc_thr1,smooth=T,rug=F,common.scale=F,
                x.label='1',y.label='Partial effect',
                show.contrib=T,plot.layout=c(2,4),cex.axis=1.2, cex.lab=1.2,las=2,
                mgp=c(3,0.3,0),tck=0.05
)

partial(swc_thr1,pred.var=c('swc_shal_od'),rug=TRUE,train=df,n.trees=1900)
partial(swc_thr1,pred.var=c('stand_height'),rug=TRUE,train=df,n.trees=1900)
partial(swc_thr1,pred.var=c('stand_density'),rug=TRUE,train=df,n.trees=1900)
partial(swc_thr1,pred.var=c('WD'),rug=TRUE,train=df,n.trees=1900)
partial(swc_thr1,pred.var=c('stand_basal_area'),rug=TRUE,train=df,n.trees=1900)
