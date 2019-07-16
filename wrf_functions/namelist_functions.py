###
# Collection of functions that simply working with the WRF namelist
# Author: Gabriel Bromley
###



import f90nml
import datetime as dt


def advance_restart(prev_namelist, interval):
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


    with open(prev_namelist, 'r') as old_nl:
        namelist = f90nml.read(old_nl)
        start_year = namelist['time_control']['start_year']
        start_month = namelist['time_control']['start_month']
        start_day = namelist['time_control']['start_day']

        current_restart = dt.date(start_year,start_month, start_day)
        new_restart = current_restart + dt.timedelta(weeks=interval)
        namelist.end_comma=True
        namelist['time_control']['start_year'] = new_restart.year
        namelist['time_control']['start_month'] = new_restart.month
        namelist['time_control']['start_day'] = new_restart.day


        try:
            namelist.write(new_restart.isoformat()+'_namelist.input')
        except IOError:
            print('File already exists',new_restart.isoformat()+'_namelist.input')

