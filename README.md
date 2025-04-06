# Species_Soil_Moisture_Threshold
Python 3.12.4 and R 4.4.1 were used to perform the results.

For installation of Python and R, please see https://www.python.org/ and https://cran.r-project.org/bin/windows/base/, and/or Anaconda3 (spyder editor) and RStudio.

For used packages in .py and .R file, the installation can be finished with 'pip install + package name' in Python and 'install.packages('package name')' in R.

'.rar' can be decompressed by WinRAR or other software.

******************************************************************************************************************************************************************

a. 1_studied_site_and_species_info.csv and Fig1.py-----basic information of studied sites, measured period and species number (present in Figure 1).

b. drydown_identify.py-----the Python program used to identify soil drying period at each site (example data in 'example.rar' and 'example_drydowns.rar').

c. drydown_swc_obs_shallow_fitting.R-----the R program used to estimate species-level critical soil moisture threshold (theta) with a piecewise linear regression between species transpiration (Td) and soil moisture (SM) during soil dry-downs (example data in 'example_drydowns.rar').

d. 2_linear_regress_grow.csv and 2_multi_linear_regress_grow.csv and Fig2.py-----quantification of linear relationships between Td and SM, VPD, SR and Ta during soil dry-downs in growing season (present in Figure 2).

e. 3_site_species_theta_threshold.xlsx and Fig3.py-----estimated theta and its spatial distribution (present in Figure 3).

f. Fig4.py-----Evaluation of species-level transpiration (Td)-soil moisture (SM) relationship.

g. BRTmodel.R and Fig5.py-----a boosted regression tree (BRT) model used to explore the drivers of spatial variation in species-level theta ('BRT_result.rar' is the output and present in Figure 5).

h. Fig6.py-----comparison of Td-SM relationship and theta between observation and reanalysis-based and satellite-based SM products ('compare.rar' is the output and present in Figure 6).

***Note: before run .py or .R file, change the read file path ('C:/Users/songchaoqing/Desktop/plant_water_stress/') to local path.
