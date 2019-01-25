#PBS -N H158
# request 1 node
#PBS -l nodes=1:ppn=20
#PBS -m abe
#PBS -A PCON0003
# request 5 hours of cpu time
#PBS -l walltime=4:00:00
# mail is sent to you when the job starts and when it terminates or aborts
cd $PBS_O_WORKDIR
# run the program
export OMP_NUM_THREADS=1
#psrecord --log memory_log.txt --interval 1.0 --include-children "python mcaltest.py"
source activate galsim
export PYTHONPATH=$PYTHONPATH:/users/PCON0003/osu10670/wfirst_imsim/
mpiexec -n 20 python ../../wfirst_imsim/wfirst_imsim/simulate.py noerror.yaml H158 30597

