tar -cvf /stash/user/troxel/wfirst_sim_tilt/run.tar /stash/user/troxel/wfirst_sim_tilt/truth/*truth_gal.fits /stash/user/troxel/wfirst_sim_tilt/truth/*index_sorted.fits
if [ $1 = "setup" ]; then
    condor_submit tilt_meds_setup_osg.sh
fi
if [ $1 = "build" ]; then
    condor_submit tilt_meds_build_osg.sh
fi
if [ $1 = "run" ]; then
    condor_submit tilt_meds_run_osg.sh
fi
