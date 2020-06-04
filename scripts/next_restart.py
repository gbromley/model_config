###
# Command line script to advance the restart in WRF
# Author: Gabe Bromley
###
import sys
import os
HOME=os.environ['HOME']
sys.path.append(HOME+'/config_files/model_config/wrf_functions/')
import namelist_functions as nf
import sys



def main():



    namelist_file_path = sys.argv[1]
    namelist_file = namelist_file_path + '/namelist.input'
    ### Try and open the namelist to makesure it exists
    try:
        f = open(namelist_file, 'r')
    except OSError:
        print('cannot open', namelist_file)
    else:
        f.close()
    print("Namelist file: "+namelist_file)
    ### Run the advance restart code
    return_code = nf.next_restart(namelist_file_path)
    ### Pass return code from advance_restart to bash
    return return_code


if __name__ == "__main__":
    main()
