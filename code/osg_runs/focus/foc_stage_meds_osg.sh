if [ $1 = "setup" ]; then
    tar -cvf /stash/user/troxel/wfirst_sim_focus/run.tar /stash/user/troxel/wfirst_sim_focus/truth/*truth_gal.fits /stash/user/troxel/wfirst_sim_focus/truth/*index*.fits
    condor_submit foc_meds_setup_osg.sh
fi
if [ $1 = "build" ]; then
    tar -cvf /stash/user/troxel/wfirst_sim_focus/run.tar /stash/user/troxel/wfirst_sim_focus/truth/*truth_gal.fits /stash/user/troxel/wfirst_sim_focus/truth/*index_sorted.fits.gz
    condor_submit foc_meds_build_osg.sh
fi
if [ $1 = "run" ]; then
    condor_submit foc_meds_run_osg.sh
fi
