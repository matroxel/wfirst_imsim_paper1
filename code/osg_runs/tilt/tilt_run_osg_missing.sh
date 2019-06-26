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
                          /stash/user/troxel/wfirst_sim_input/, \
                          /home/troxel/wfirst_imsim_paper1/code/osg_runs/tilt/tilt_osg.yaml, \
                          /home/troxel/wfirst_imsim_paper1/code/dither_list.txt,\
                          /home/troxel/wfirst_imsim_paper1/code/meds_pix_list.txt, \
                          /stash/user/troxel/wfirst_sim_tilt/run.tar

transfer_output_files   = stamps, \
                          images, \
                          truth

Initialdir     = /stash/user/troxel/wfirst_sim_tilt/
log            = tilt_run_short_log_$(DITHER)_$(CHIP).log

Arguments = tilt_osg.yaml None $(DITHER) $(CHIP) verify_output
Executable     = ../run_osg.sh
Output         = tilt_run_short_$(DITHER)_$(CHIP).log
Error          = tilt_run_short_$(DITHER)_$(CHIP).log

# Science sensors only. Ignore 0,0 4,0 0,4 and 4,4. 

#Queue

CHIP=16
DITHER=81017
Queue

CHIP=16
DITHER=81018
Queue

CHIP=16
DITHER=81021
Queue

CHIP=16
DITHER=81022
Queue

CHIP=16
DITHER=81023
Queue

CHIP=16
DITHER=81024
Queue

CHIP=16
DITHER=81025
Queue

CHIP=16
DITHER=81026
Queue

CHIP=12
DITHER=147836
Queue

CHIP=14
DITHER=147843
Queue


