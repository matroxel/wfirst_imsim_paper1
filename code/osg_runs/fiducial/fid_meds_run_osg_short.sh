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



        
transfer_input_files    = /home/troxel/wfirst_stack/wfirst_stack.tar.gz, /home/troxel/wfirst_imsim_paper1/code/osg_runs/fiducial/fid_osg.yaml, /home/troxel/wfirst_imsim_paper1/code/meds_pix_list.txt, /stash/user/troxel/wfirst_sim_fiducial/run.tar, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30587_17_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30588_17_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30589_17_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30590_17_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147830_5_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147830_6_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147831_5_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147831_6_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147832_5_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147832_9_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147833_5_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_147833_9_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_176233_11_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_176234_11_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_176235_11_0.cPickle.gz
MEDS=2284535
Queue


transfer_input_files    = /home/troxel/wfirst_stack/wfirst_stack.tar.gz, /home/troxel/wfirst_imsim_paper1/code/osg_runs/fiducial/fid_osg.yaml, /home/troxel/wfirst_imsim_paper1/code/meds_pix_list.txt, /stash/user/troxel/wfirst_sim_fiducial/run.tar, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30587_11_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30587_14_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30588_11_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30588_14_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30589_10_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30589_11_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30590_10_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_30590_11_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_176233_18_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_176234_18_0.cPickle.gz, /stash/user/troxel/wfirst_sim_fiducial/stamps/fiducial_H158_176235_18_0.cPickle.gz
MEDS=2284539
Queue


