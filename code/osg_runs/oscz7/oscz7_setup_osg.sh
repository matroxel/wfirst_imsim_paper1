#-*-shell-script-*- 

universe     = vanilla
Requirements = OSGVO_OS_VERSION == "7" && \
               CVMFS_oasis_opensciencegrid_org_REVISION >= 10686 

+ProjectName = "duke.lsst"
+WantsCvmfsStash = true
request_memory = 2G

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
                          /home/troxel/wfirst_imsim_paper1/code/oscz7_osg.yaml, \
                          /home/troxel/wfirst_imsim_paper1/code/dither_list.txt,\
                          /home/troxel/wfirst_imsim_paper1/code/meds_pix_list.txt

transfer_output_files   = truth

Initialdir     = /stash/user/troxel/wfirst_sim_oscz7/
log            = oscz7_setup.log

Executable     = run_osg.sh
Arguments      = oscz7_osg.yaml None setup
Output         = oscz7_setup.log
Error          = oscz7_setup.log

# Science sensors only. Ignore 0,0 4,0 0,4 and 4,4. 

Queue

#Queue SENSORID From (
# R:0,1_S:0,0
# R:0,1_S:0,1
# R:0,1_S:0,2
# R:0,1_S:1,0
