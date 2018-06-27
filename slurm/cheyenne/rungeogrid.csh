#!/bin/csh

### Project name
#PBS -A P66770001

### Job name
#PBS -N geogrid_gbromley 

### Wallclock time
#PBS -l walltime=00:30:00

### Queue
#PBS -q regular

### Merge output and error files
#PBS -j oe                    

### Select 2 nodes with 36 CPUs, for 72 MPI processes 
#PBS -l select=2:ncpus=36:mpiprocs=36  

mpiexec_mpt ./geogrid.exe
