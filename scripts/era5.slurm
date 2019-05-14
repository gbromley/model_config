#!/bin/bash -l
#SBATCH --job-name=era5_download_gbromley
#SBATCH --account=UMSB0001
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=1
#SBATCH --time=00:60:00
#SBATCH --partition=dav
#SBATCH --output=dep_job1.out.%j



module load python/3.6.8

ncar_pylib


python3 /glade/u/home/gbromley/code/Python-Utilities/era_5_download.py 2011 2012
