#PBS -N H158
# request 1 node
#PBS -l nodes=1:ppn=20
#PBS -A PCON0003
# request 4 hours and 30 minutes of cpu time
#PBS -l walltime=4:00:00
# mail is sent to you when the job starts and when it terminates or aborts
cd $PBS_O_WORKDIR
# run the program
export OMP_NUM_THREADS=1
#psrecord --log memory_log.txt --interval 1.0 --include-children "python mcaltest.py"
export PYTHONPATH=$PYTHONPATH:/users/PCON0003/cond0083/wfirst_imsim/
#mpiexec -n 1 python ../../wfirst_imsim/wfirst_imsim/simulate.py fid.yaml H158 meds setup
mpiexec -n 20 python ../../wfirst_imsim/wfirst_imsim/simulate.py fid.yaml H158 meds 1
mpiexec -n 20 python ../../wfirst_imsim/wfirst_imsim/simulate.py fid.yaml H158 meds 2
mpiexec -n 20 python ../../wfirst_imsim/wfirst_imsim/simulate.py fid.yaml H158 meds 3
mpiexec -n 20 python ../../wfirst_imsim/wfirst_imsim/simulate.py fid.yaml H158 meds 4
mpiexec -n 20 python ../../wfirst_imsim/wfirst_imsim/simulate.py fid.yaml H158 meds 5
#571311
##mpiexec -n 1 python ../../wfirst_imsim/wfirst_imsim/simulate.py fid.yaml H158 meds 571322
##mpiexec -n 1 python ../../wfirst_imsim/wfirst_imsim/simulate.py fid.yaml H158 meds 572688
##mpiexec -n 1 python ../../wfirst_imsim/wfirst_imsim/simulate.py fid.yaml H158 meds 572691
##mpiexec -n 1 python ../../wfirst_imsim/wfirst_imsim/simulate.py fid.yaml H158 meds 572692
