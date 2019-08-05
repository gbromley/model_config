#!/bin/csh
#
# WW: Last modified 7/24/2019
# To run this script: ./get-era5.csh YYYY YYYY
# Before running the script, edit 'last_day_of_month' and 'num_days' for the data needed,
#
set echo
set LOGINNAME   = $USER
set TOPDIR      = /glade/scratch/${LOGINNAME}
# this would be the directory you will download era5 data, create this directory before proceeding
set WPSDIR      = /glade/scratch/$LOGINNAME/era5/test_run/
# do not change this line
set BINDIR      = /glade/u/home/wrfhelp/bin
#
# edit the next two numbers: for September, last_day_of_month = 30, for October, last_day_of_month = 31
#      num_days: number of days for the data
#

set last_day_of_month = 31
set num_days = 365
#
# calculate the start time
#
if ( ${#argv} > 0 ) then
  echo 'Calculating initialization time from input date'
  set current_cen   = `echo $1 | cut -c1-2`
  set current_year  = `echo $1 | cut -c3-4`
  set current_month = `echo $1 | cut -c5-6`
  set current_day   = `echo $1 | cut -c7-8`
  set current_hour  = `echo $1 | cut -c9-10`
else
# date -u gives UTC time
  echo 'Calculating initialization time from current time'
  set current_cen   = `date -u '+%C'`
  set current_year  = `date -u '+%y'`
  set current_month = `date -u '+%m'`
  set current_day   = `date -u '+%d'`
  set current_time  = `date -u '+%H'`
  if ( $current_time < 12 ) then
     set current_hour = 00
  else
     set current_hour = 12
  endif
endif
#
cd $WPSDIR
#
set MSSDIR      = /FS/DECS/DS630.0/e5.oper.an.pl/${current_cen}${current_year}${current_month}
set MSSDIR2     = /FS/DECS/DS630.0/e5.oper.an.sfc/${current_cen}${current_year}${current_month}
set MSSDIR0     = /FS/DECS/DS630.0/e5.oper.invariant/201601
#
set DataTime = ${current_cen}${current_year}${current_month}${current_day}${current_hour}
#
@ num_days_plus1 = $num_days + 1
set h_interval = 24
set numf = 1
#
# obtain the time-ivariant file: terrain height and land mask
hsi cget $MSSDIR0/e5.oper.invariant.128_129_z.regn320sc.2016010100_2016010100.grb
hsi cget $MSSDIR0/e5.oper.invariant.128_172_lsm.regn320sc.2016010100_2016010100.grb
#
while ( $numf < $num_days_plus1 )
#
set file_time_s = ${current_cen}${current_year}${current_month}${current_day}${current_hour}
set file_time_e = ${current_cen}${current_year}${current_month}${current_day}23
set data_type = e5.oper.an.pl.128
set data_type_uv = regn320uv
set data_type_sc = regn320sc
#
hsi cget $MSSDIR/${data_type}_129_z.${data_type_sc}.${file_time_s}_${file_time_e}.grb
hsi cget $MSSDIR/${data_type}_130_t.${data_type_sc}.${file_time_s}_${file_time_e}.grb
hsi cget $MSSDIR/${data_type}_157_r.${data_type_sc}.${file_time_s}_${file_time_e}.grb
hsi cget $MSSDIR/${data_type}_131_u.${data_type_uv}.${file_time_s}_${file_time_e}.grb
hsi cget $MSSDIR/${data_type}_132_v.${data_type_uv}.${file_time_s}_${file_time_e}.grb
#echo 'cget ' $MSSDIR/${data_type}_129_z.${data_type_sc}.${file_time_s}_${file_time_e}.grb
#
# surface data
#
set file_time_s = ${current_cen}${current_year}${current_month}0100
set file_time_e = ${current_cen}${current_year}${current_month}${last_day_of_month}23
set data_type_sfc = e5.oper.an.sfc.128
#
hsi cget $MSSDIR2/${data_type_sfc}_034_sstk.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_039_swvl1.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_040_swvl2.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_041_swvl3.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_042_swvl4.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_139_stl1.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_170_stl2.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_183_stl3.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_236_stl4.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_165_10u.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_166_10v.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_167_2t.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_168_2d.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_134_sp.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_151_msl.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_235_skt.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_033_rsn.${data_type_sc}.${file_time_s}_*.grb
hsi cget $MSSDIR2/${data_type_sfc}_141_sd.${data_type_sc}.${file_time_s}_*.grb
#
# calculate date for next time
#
echo $DataTime
set output2 = `$BINDIR/geth_newdate_cheyenne $DataTime $h_interval`
echo $output2
#
set current_cen    = `echo $output2 | cut -c1-2`
set current_year   = `echo $output2 | cut -c3-4`
set current_month  = `echo $output2 | cut -c5-6`
set current_day    = `echo $output2 | cut -c7-8`
set current_hour   = `echo $output2 | cut -c9-10`
#
# update start date
set DataTime = ${current_cen}${current_year}${current_month}${current_day}$current_hour
#
@ numf ++
#
end