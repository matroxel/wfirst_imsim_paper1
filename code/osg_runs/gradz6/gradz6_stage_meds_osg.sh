if [ $1 = "setup" ]; then
    tar -cvf /stash/user/troxel/wfirst_sim_gradz6/run.tar /stash/user/troxel/wfirst_sim_gradz6/truth/*truth_gal.fits /stash/user/troxel/wfirst_sim_gradz6/truth/*index*.fits
    condor_submit gradz6_meds_setup_osg.sh
fi
if [ $1 = "build" ]; then
    tar -cvf /stash/user/troxel/wfirst_sim_gradz6/run.tar /stash/user/troxel/wfirst_sim_gradz6/truth/*truth_gal.fits /stash/user/troxel/wfirst_sim_gradz6/truth/*index_sorted.fits.gz
    condor_submit gradz6_meds_build_osg.sh
fi
if [ $1 = "run" ]; then
    condor_submit gradz6_meds_run_osg.sh
fi
