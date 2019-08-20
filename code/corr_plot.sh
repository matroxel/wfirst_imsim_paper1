#PBS -N corr_test
# request 1 node
#PBS -l nodes=1:ppn=20
#PBS -A PCON0003
# request 4 hours and 30 minutes of cpu time
#PBS -l walltime=4:00:00
# mail is sent to you when the job starts and when it terminates or aborts
# run the program

cd $PBS_O_WORKDIR
export OMP_NUM_THREADS=1
#psrecord --log memory_log.txt --interval 1.0 --include-children "python mcaltest.py"
source loadLSST.bash
source activate galsim

mpiexec -n 20 python corr_plot.py anismear
