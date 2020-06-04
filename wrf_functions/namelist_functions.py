###
# Collection of functions that simply working with the WRF namelist
# Author: Gabriel Bromley
###



import f90nml
import datetime as dt
import os
import sys
import shutil
import glob

def next_restart(prev_namelist_path):
    prev_namelist = prev_namelist_path+'/namelist.input'
    try:
        f = open(prev_namelist, 'r')
    except IOError:
        print("Could not read file:", prev_namelist)
    else:
        f.close()


    ### Get the last restart file by creation time ###
    list_of_restarts = glob.glob(prev_namelist_path +'/wrfrst*')  # * means all if need specific format then *.csv
    latest_file = max(list_of_restarts, key=os.path.getctime)
    print(latest_file)
    restart = latest_file.split('/')[-1]
    ### format of restart file name: wrfrst_d01_2010-11-22_00:00:00 ###
    rst_year = int(restart[11:15])
    rst_month =  int(restart[16:18])
    rst_day = int(restart[19:21])

    current_restart = dt.date(rst_year, rst_month, rst_day)
    with open(prev_namelist, 'r') as old_nl:
        os.rename(prev_namelist, prev_namelist_path + '/backup.namelist.input')
        namelist = f90nml.read(old_nl)
        start_year = namelist['time_control']['start_year']
        start_month = namelist['time_control']['start_month']
        start_day = namelist['time_control']['start_day']


        namelist.end_comma = True
        namelist['time_control']['start_year'] = current_restart.year
        namelist['time_control']['start_month'] = current_restart.month
        namelist['time_control']['start_day'] = current_restart.day

        try:
            namelist.write(prev_namelist_path+'/namelist.input')
            return 0
        except IOError:
            print('Problem with:', new_restart.isoformat() + '_namelist.input')


def advance_modeltime(prev_namelist, interval, output_dir):
    ###
    #Advances the namelist by specified interval in weeks
    #Takes a namelist, finds the start variables adds
    #prev_nameslit should be a path to namelist
    #interval should be in weeks
    ###
    try:
        f = open(prev_namelist, 'r')
    except IOError:
        print("Could not read file:", prev_namelist)
    else:
        f.close()
    if (os.path.exists(output_dir)==False):
        return 1

    with open(prev_namelist, 'r') as old_nl:
        namelist = f90nml.read(old_nl)
        start_year = namelist['time_control']['start_year']
        start_month = namelist['time_control']['start_month']
        start_day = namelist['time_control']['start_day']

        end_year = namelist['time_control']['end_year']
        end_month = namelist['time_control']['end_month']
        end_day = namelist['time_control']['end_day']



        current_restart = dt.date(start_year,start_month, start_day)
        new_restart = current_restart + dt.timedelta(weeks=interval)
        print(end_day)
        print(start_day)
        if (new_restart.year >= end_year and new_restart.month >= end_month and new_restart.day >= end_day):
            print("Simulation has ended")
            sys.exit(2)





        namelist.end_comma=True
        namelist['time_control']['start_year'] = new_restart.year
        namelist['time_control']['start_month'] = new_restart.month
        namelist['time_control']['start_day'] = new_restart.day


        try:
            namelist.write(output_dir+new_restart.isoformat()+'_namelist.input')
            return 0
        except IOError:
            print('File already exists',new_restart.isoformat()+'_namelist.input')

