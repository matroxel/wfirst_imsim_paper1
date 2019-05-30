#PBS -N z4_diff_meds_run
#PBS -l nodes=1:ppn=20
#PBS -A PCON0003
#PBS -l walltime=5:00:00
#PBS -t 1-210%8

cd $PBS_O_WORKDIR
export OMP_NUM_THREADS=1
#psrecord --log memory_log.txt --interval 1.0 --include-children "python mcaltest.py"
export PYTHONPATH=$PYTHONPATH:/users/PCON0003/cond0083/wfirst_imsim/
source activate galsim

mpiexec -n 20 python ../../wfirst_imsim/wfirst_imsim/simulate.py z4_diff.yaml H158 meds $PBS_ARRAYID
