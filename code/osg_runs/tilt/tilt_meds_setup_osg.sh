#-*-shell-script-*- 

universe     = vanilla
Requirements = OSGVO_OS_VERSION == "7" && \
               CVMFS_oasis_opensciencegrid_org_REVISION >= 10686 

+ProjectName = "duke.lsst"
+WantsCvmfsStash = true
request_memory = 4G

#PeriodicRemove = ( JobStatus == 2 ) && ( ( CurrentTime - EnteredCurrentStatus ) > 600 )

# If the job doesn't finish normally by itself, resubmit.
# on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)

# If a job has been running for more than 5 hours, hold it then resubmit
#periodic_hold         = ((JobStatus == 2) && (time() - EnteredCurrentStatus) > (3600*5))
#periodic_hold_reason  = "Job exceeded 5-hour runtime limit."
#periodic_hold_subcode = 1

#periodic_release = (HoldReasonCode == 3) && (HoldReasonSubCode == 1)

should_transfer_files = YES
when_to_transfer_output = ON_EXIT_OR_EVICT
transfer_input_files    = /home/troxel/wfirst_stack/wfirst_stack.tar.gz, \
                          /home/troxel/wfirst_imsim_paper1/code/tilt_osg.yaml, \
                          /home/troxel/wfirst_imsim_paper1/code/dither_list.txt,\
                          /home/troxel/wfirst_imsim_paper1/code/meds_pix_list.txt, \
                          /stash/user/troxel/wfirst_sim_tilt/run.tar

transfer_output_files   = truth/tilt_H158_index_sorted.fits
transfer_output_remaps  = "tilt_H158_index_sorted.fits.gz = /stash/user/troxel/wfirst_sim_tilt/truth/tilt_H158_index_sorted.fits.gz"

Initialdir     = /stash/user/troxel/wfirst_sim_tilt/
log            = tilt_meds_setup_log.log

Arguments = tilt_osg.yaml H158 meds setup
Executable     = ../run_osg.sh
Output         = tilt_meds_setup.log
Error          = tilt_meds_setup.log

# Science sensors only. Ignore 0,0 4,0 0,4 and 4,4. 

Queue

