#%%
import f90nml
import os
import glob
import time
import subprocess
#%%

#path to wrf run directory
run_dir='/Users/gbromley/code/wrf_run_configs/scripts/'
out_dir=''
while True:
    #check to see if previous job completed
    while not os.path.exists(run_dir+'wrf_finished'):
        time.sleep(20)
        
    #move output to folder
    wrf_out_files = glob.glob(run_dir+'wrfout*')
    for out_file in wrf_out_files:
        subprocess.run('mv '+out_file+' '+out_dir+out_file, shell=True)
        
    
    #remove job finshed file
    os.remove(run_dir+'wrf_finished')
    #remove rsl files
    rsl_files = glob.glob(run_dir+'rsl.*')
    for rsl in rsl_files:
        os.remove(f)
    #find most recent restart file
    list_of_restarts = glob.glob(run_dir+'wrfrst*') # * means all if need specific format then *.csv
    latest_restart = max(list_of_restarts, key=os.path.getctime)
    #get start date for next run
    year_start = latest_restart.split('/')[6][11:15]
    month_start = latest_restart.split('/')[6][16:18]
    day_start = latest_restart.split('/')[6][19:21]

    #read data from most recent restart file

    #add start dates to namelist
    with open('/Users/gbromley/code/wrf_run_configs/wrf/4km_NGP/test_namelist.input', 'r') as nl_template:
        file_data = nl_template.read()
        new_namelist = file_data.replace('<year_start>',year_start)
        new_namelist = new_namelist.replace('<month_start>',month_start)
        new_namelist = new_namelist.replace('<day_start>', day_start)
        new_namelist = new_namelist.replace('<rst>', '.true.')
    with open(run_dir+'namelist.input', 'w+') as file:
        file.write(new_namelist)
    #submit new job
    subprocess.run('qsub runwrf.csh', shell=True)
