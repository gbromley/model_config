#!/bin/bash

### Project name
#PBS -A UMSB0001

### Job name
#PBS -N era5_download_gbromley

### Wallclock time
#PBS -l walltime=04:00:00

### Queue
#PBS -q economy

### Merge output and error files
#PBS -j oe

### Select 2 nodes with 36 CPUs, for 72 MPI processes
#PBS -l select=1:ncpus=4:mpiprocs=36

module load python/3.6.8

ncar_pylib

START=2012
END=2013
SCRATCH_DIRECTORY=/glade/scratch/gbromley/era5_${START}-${END}
mkdir -p ${SCRATCH_DIRECTORY}
cd ${SCRATCH_DIRECTORY}

python ~gbromley/config_files/model_config/scripts/era_5_download.py
