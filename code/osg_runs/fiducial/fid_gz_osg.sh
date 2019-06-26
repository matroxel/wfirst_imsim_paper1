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
transfer_input_files    = stamps/$(GZ)

transfer_output_files   = stamps

Initialdir     = /stash/user/troxel/wfirst_sim_fiducial/
log            = fid_gz_$(GZ).log

Arguments      =  $(GZ)
Executable     = ../gz_osg.sh
Output         = fid_gz_$(GZ).log
Error          = fid_gz_$(GZ).log

# Science sensors only. Ignore 0,0 4,0 0,4 and 4,4. 

#Queue

Queue GZ From ../../gz.txt
