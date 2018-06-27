#!/bin/csh

### Project name
#PBS -A xxxxxxxx

### Job name
#PBS -N real

### Wallclock time
#PBS -l walltime=00:30:00

### Queue
#PBS -q regular

### Merge output and error files
#PBS -j oe                    

### Select 2 nodes with 36 CPUs, for 72 MPI processes 
#PBS -l select=2:ncpus=36:mpiprocs=36  

mpiexec_mpt ./real.exe
