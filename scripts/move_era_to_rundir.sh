#!/bin/csh

set BINDIR = /glade/u/home/wrfhelp/bin

if ( ${#argv} > 0 ) then
  echo 'Calculating initialization time from input date'
  set current_cen   = `echo $1 | cut -c1-2`
  set current_year  = `echo $1 | cut -c3-4`
  set current_month = `echo $1 | cut -c5-6`
  set current_day   = `echo $1 | cut -c7-8`
  set current_hour  = `echo $1 | cut -c9-10`

endif
#
set RUNDIR=$2
cd $RUNDIR
#

set DATA_DIR=/glade/p/univ/umsb0001/era5/2011-2015

#
set last_day_of_month = 31
set num_days = 63

set DataTime = ${current_cen}${current_year}${current_month}${current_day}${current_hour}
#
@ num_days_plus1 = $num_days + 1
set h_interval = 24
set numf = 1
#
# obtain the time-ivariant file: terrain height and land mask
ln -s $DATA_DIR/e5.oper.invariant.128_129_z.regn320sc.2016010100_2016010100.grb $RUNDIR/e5.oper.invariant.128_129_z.regn320sc.2016010100_2016010100.grb
ln -s $DATA_DIR/e5.oper.invariant.128_172_lsm.regn320sc.2016010100_2016010100.grb $RUNDIR/e5.oper.invariant.128_172_lsm.regn320sc.2016010100_2016010100.grb

#
while ( $numf < $num_days_plus1 )
#

set file_time_s = ${current_cen}${current_year}${current_month}${current_day}${current_hour}
set file_time_e = ${current_cen}${current_year}${current_month}${current_day}23
set data_type = e5.oper.an.pl.128
set data_type_uv = regn320uv
set data_type_sc = regn320sc
set data_type_ll = ll025uv
#
ln -sf $DATA_DIR/${data_type}_129_z.${data_type_sc}.${file_time_s}_${file_time_e}.grb $RUNDIR/${data_type}_129_z.${data_type_sc}.${file_time_s}_${file_time_e}.grb
ln -sf $DATA_DIR/${data_type}_130_t.${data_type_sc}.${file_time_s}_${file_time_e}.grb $RUNDIR/${data_type}_130_t.${data_type_sc}.${file_time_s}_${file_time_e}.grb
ln -sf $DATA_DIR/${data_type}_157_r.${data_type_sc}.${file_time_s}_${file_time_e}.grb $RUNDIR/${data_type}_157_r.${data_type_sc}.${file_time_s}_${file_time_e}.grb
ln -sf $DATA_DIR/${data_type}_131_u.${data_type_uv}.${file_time_s}_${file_time_e}.grb $RUNDIR/${data_type}_131_u.${data_type_uv}.${file_time_s}_${file_time_e}.grb
ln -sf $DATA_DIR/${data_type}_132_v.${data_type_uv}.${file_time_s}_${file_time_e}.grb $RUNDIR/${data_type}_132_v.${data_type_uv}.${file_time_s}_${file_time_e}.grb
### This is for the new era5 data (ds633.0)
if (test -f "$DATA_DIR/${data_type}_132_v.${data_type_ll}.${file_time_s}_${file_time_e}.grb") then
    echo 'in one of the If statements'
    ln -sf $DATA_DIR/${data_type}_132_v.${data_type_ll}.${file_time_s}_${file_time_e}.grb $RUNDIR/${data_type}_132_v.${data_type_uv}.${file_time_s}_${file_time_e}.grb
endif
### This is for the new era5 data (ds633.0)
if (test -f "$DATA_DIR/${data_type}_131_u.${data_type_ll}.${file_time_s}_${file_time_e}.grb") then
    echo 'in the second statement'
    ln -sf $DATA_DIR/${data_type}_131_u.${data_type_ll}.${file_time_s}_${file_time_e}.grb $RUNDIR/${data_type}_131_u.${data_type_uv}.${file_time_s}_${file_time_e}.grb
endif
# surface data
#
set file_time_s = ${current_cen}${current_year}${current_month}0100
set file_time_e = ${current_cen}${current_year}${current_month}${last_day_of_month}23
set data_type_sfc = e5.oper.an.sfc.128
#
ln -sf $DATA_DIR/${data_type_sfc}_034_sstk.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_039_swvl1.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_040_swvl2.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_041_swvl3.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_042_swvl4.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_139_stl1.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_170_stl2.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_183_stl3.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_236_stl4.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_165_10u.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_166_10v.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_167_2t.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_168_2d.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_134_sp.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_151_msl.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_235_skt.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_033_rsn.${data_type_sc}.${file_time_s}_* $RUNDIR/.
ln -sf $DATA_DIR/${data_type_sfc}_141_sd.${data_type_sc}.${file_time_s}_* $RUNDIR/.
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
