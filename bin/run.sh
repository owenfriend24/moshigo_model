#!/bin/bash
#
subject=$1
#python /home1/09123/ofriend/analysis/moshigo_model/bin/pca_cluster_model.py
#python /home1/09123/ofriend/analysis/moshigo_model/bin/plot_ssm_traj.py


re_transform.sh ${subject}
transform_sl_to_2mm.sh ${subject}
smooth_sl.sh /scratch/09123/ofriend/moshi/grid_coding/mni/new2 ${subject}