###
# Collection of functions that simply working with the WRF namelist
# Author: Gabriel Bromley
###



import f90nml
import datetime as dt
import os
import sys


def advance_restart(prev_namelist, interval, output_dir):
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

