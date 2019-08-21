#!/bin/csh

### Project name
#PBS -A UMSB0001

### Job name
#PBS -N metgrid_gbromley 

### Wallclock time
#PBS -l walltime=04:00:00

### Queue
#PBS -q regular

### Merge output and error files
#PBS -j oe                    

### Select 2 nodes with 36 CPUs, for 72 MPI processes 
#PBS -l select=2:ncpus=36:mpiprocs=36  




mpiexec_mpt ./metgrid.exe
