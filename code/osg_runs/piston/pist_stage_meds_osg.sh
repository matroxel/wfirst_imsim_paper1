tar -cvf /stash/user/troxel/wfirst_sim_piston/run.tar /stash/user/troxel/wfirst_sim_piston/truth/*truth_gal.fits /stash/user/troxel/wfirst_sim_piston/truth/*index_sorted.fits
if [ $1 = "setup" ]; then
    condor_submit pist_meds_setup_osg.sh
fi
if [ $1 = "build" ]; then
    condor_submit pist_meds_build_osg.sh
fi
if [ $1 = "run" ]; then
    condor_submit pist_meds_run_osg.sh
fi
