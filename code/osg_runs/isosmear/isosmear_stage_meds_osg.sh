if [ $1 = "setup" ]; then
    tar -cvf /stash/user/troxel/wfirst_sim_isosmear/run.tar /stash/user/troxel/wfirst_sim_isosmear/truth/*truth_gal.fits /stash/user/troxel/wfirst_sim_isosmear/truth/*index*.fits
    condor_submit isosmear_meds_setup_osg.sh
fi
if [ $1 = "build" ]; then
    tar -cvf /stash/user/troxel/wfirst_sim_isosmear/run.tar /stash/user/troxel/wfirst_sim_isosmear/truth/*truth_gal.fits /stash/user/troxel/wfirst_sim_isosmear/truth/*index_sorted.fits.gz
    condor_submit isosmear_meds_build_osg.sh
fi
if [ $1 = "run" ]; then
    condor_submit isosmear_meds_run_osg.sh
fi
