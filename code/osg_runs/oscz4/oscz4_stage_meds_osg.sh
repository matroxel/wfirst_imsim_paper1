tar -cvf /stash/user/troxel/wfirst_sim_oscz4/run.tar /stash/user/troxel/wfirst_sim_oscz4/truth/*truth_gal.fits /stash/user/troxel/wfirst_sim_oscz4/truth/*index_sorted.fits
if [ $1 = "setup" ]; then
    condor_submit oscz4_meds_setup_osg.sh
fi
if [ $1 = "build" ]; then
    condor_submit oscz4_meds_build_osg.sh
fi
if [ $1 = "run" ]; then
    condor_submit oscz4_meds_run_osg.sh
fi
