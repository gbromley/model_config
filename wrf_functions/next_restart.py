###
# Command line script to advance the restart in WRF
# Author: Gabe Bromley
###

from wrf_functions import namelist_functions as nf
import sys
import os


def main():



    namelist_file = sys.argv[0]
    interval = sys.argv[1]
    output_dir = sys.argv[2]

    ### Try and open the namelist to makesure it exists
    try:
        f = open(namelist_file, 'r')
    except OSError:
        print('cannot open', namelist_file)
    else:
        f.close()
    ### Run the advance restart code
    return_code = nf.advance_restart(namelist_file, 8 ,output_dir)
    ### Pass return code from advance_restart to bash
    return return_code


if __name__ == "__main__":
    main()
