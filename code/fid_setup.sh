#PBS -N fid_setup
#PBS -l nodes=1:ppn=20
#PBS -A PCON0003
#PBS -l walltime=4:00:00

cd $PBS_O_WORKDIR
export OMP_NUM_THREADS=1
#psrecord --log memory_log.txt --interval 1.0 --include-children "python mcaltest.py"
export PYTHONPATH=$PYTHONPATH:/users/PCON0003/cond0083/wfirst_imsim/

mpiexec -n 20 python ../../wfirst_imsim/wfirst_imsim/simulate.py fid.yaml None setup
