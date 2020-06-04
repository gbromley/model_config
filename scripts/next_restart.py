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



    namelist_file = sys.argv[1]
    interval = int(sys.argv[2])
    output_dir = sys.argv[3]

    ### Try and open the namelist to makesure it exists
    try:
        f = open(namelist_file, 'r')
    except OSError:
        print('cannot open', namelist_file)
    else:
        f.close()
    print("Namelist file: "+namelist_file)
    print("Destination: "+output_dir)
    ### Run the advance restart code
    return_code = nf.advance_restart(namelist_file, interval,output_dir)
    ### Pass return code from advance_restart to bash
    return return_code


if __name__ == "__main__":
    main()
