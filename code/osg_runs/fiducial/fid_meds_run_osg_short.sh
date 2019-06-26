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
log            = fid_meds_log_$(MEDS).log
Arguments = fid_osg.yaml H158 meds $(MEDS)
Output         = fid_meds_$(MEDS).log
Error          = fid_meds_$(MEDS).log



transfer_input_files    = /home/troxel/wfirst_stack/wfirst_stack.tar.gz, /home/troxel/wfirst_imsim_paper1/code/osg_runs/fiducial/fid_osg.yaml, /home/troxel/wfirst_imsim_paper1/code/meds_pix_list.txt, /stash/user/troxel/wfirst_sim_fiducial/run.tar, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30585_16_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30586_16_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30591_5_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30591_8_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30591_9_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30592_8_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30592_9_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30593_8_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30593_9_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81018_6_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81019_6_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81019_9_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81020_5_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81020_6_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81020_9_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81021_4_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81021_7_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81022_4_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81022_7_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81023_4_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_81023_7_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147834_4_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147834_5_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147834_8_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147834_9_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147835_4_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147835_5_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147835_8_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147835_9_0.cPickle.gz
MEDS=2285231
Queue
