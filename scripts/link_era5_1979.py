import subprocess
import sys
import glob
import shutil
import os


atm_data = '/glade/collections/rda/data/ds633.0/e5.oper.an.pl/'
sfc_data = '/glade/collections/rda/data/ds633.0/e5.oper.an.sfc/'

scratch_dir = '/glade/scratch/gbromley/'

start_year = int(sys.argv[1])
end_year = int(sys.argv[2])


if (end_year <= start_year):
    print("invalid years")
    sys.exit()

if (start_year < 1979 or end_year >= 1995 or start_year >= 1995 or end_year <= 1979):
    print("invalid range of years")
    sys.exit()


months = ['01','02','03','04','05','06','07','08','09','10','11','12']
print("grabbing "+str(start_year)+" to "+str(end_year))
current_year = start_year

data_dir = scratch_dir+"era5"+"_"+str(start_year)+"-"+str(end_year)

if(os.path.exists(data_dir) and os.path.isdir(data_dir)):
    shutil.rmtree(data_dir)

try:
    print("making directory in: "+data_dir)
    p1 = subprocess.run(["mkdir",data_dir], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
except Exception:
    print("directory error")



while (current_year <= end_year):
    for month in months:
        atm_files = glob.glob(atm_data+str(current_year)+month+'/*')
        sfc_files = glob.glob(sfc_data+str(current_year)+month+'/*')
        try:

            for i in atm_files:

                p2 = subprocess.run(["ln","-s",i,data_dir],stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                p2.check_returncode()
            for p in sfc_files:
                p3 = subprocess.run(["ln","-s",p,data_dir],stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                p3.check_returncode()


        except subprocess.CalledProcessError:
            print("Making or linking exited in error")
            sys.exit()

        except Exception as e:
            print("Something went wrong with linking or directory")
            print(e.message)
            print(e.args)
            sys.exit()
    current_year =current_year + 1
