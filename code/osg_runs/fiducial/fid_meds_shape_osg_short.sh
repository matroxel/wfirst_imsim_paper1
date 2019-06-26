#-*-shell-script-*- 

universe     = vanilla
Requirements = OSGVO_OS_VERSION == "7" && CVMFS_oasis_opensciencegrid_org_REVISION >= 10686 

+ProjectName = "duke.lsst"
+WantsCvmfsStash = true
request_memory = 4G

should_transfer_files = YES
when_to_transfer_output = ON_EXIT_OR_EVICT
Executable     = ../run_osg.sh
transfer_output_files   = ngmix, meds
Initialdir     = /stash/user/troxel/wfirst_sim_fiducial/
log            = fid_meds_log_$(MEDS)_$(ITER).log
Arguments = fid_osg.yaml H158 meds shape $(MEDS) $(ITER) 10
Output         = fid_meds_$(MEDS)_$(ITER).log
Error          = fid_meds_$(MEDS)_$(ITER).log

transfer_input_files    = /home/troxel/wfirst_stack/wfirst_stack.tar.gz, /home/troxel/wfirst_imsim_paper1/code/osg_runs/fiducial/fid_osg.yaml, /home/troxel/wfirst_imsim_paper1/code/meds_pix_list.txt, /stash/user/troxel/wfirst_sim_fiducial/run.tar, /stash/user/troxel/wfirst_sim_fiducial/meds/fiducial_H158_$(MEDS).fits.gz

MEDS=2290005
Queue ITER in 0,1,2,3,4,5,6,7,8,9



