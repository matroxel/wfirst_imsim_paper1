tar -cvf /stash/user/troxel/wfirst_sim_ransmear/run.tar /stash/user/troxel/wfirst_sim_ransmear/truth/*truth_gal.fits /stash/user/troxel/wfirst_sim_ransmear/truth/*index_sorted.fits
if [ $1 = "setup" ]; then
    condor_submit ransmear_meds_setup_osg.sh
fi
if [ $1 = "build" ]; then
    condor_submit ransmear_meds_build_osg.sh
fi
if [ $1 = "run" ]; then
    condor_submit ransmear_meds_run_osg.sh
fi
