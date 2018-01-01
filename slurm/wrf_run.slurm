#!/bin/bash
#SBATCH -J gbromley.wrf
#SBATCH -n 16
#SBATCH -N 2
#SBATCH --mem 32000
#SBATCH -t 0-6:00:00
#SBATCH -p express
#SBATCH -o gbromley_wrf_output.txt
#SBATCH -e gbromley_wrf_error.txt
#SBATCH --mail-user gabriel.bromley@montana.edu
#SBATCH --mail-type ALL



module load libpng/1.6.24-foss-2016b netCDF-Fortran/4.4.4-foss-2016b zlib/1.2.8-foss-2016b JasPer/1.900.1-foss-2016b


export NETCDF='/cm/shared/hyalite/apps/eb/netCDF-Fortran/4.4.4-foss-2016b'

mpirun -n 16 real.exe > wrf.out
