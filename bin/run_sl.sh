#!/bin/bash
#
# Smooth functional data

if [[ $# -lt 1 ]]; then
    echo ""
    exit 1
fi

sl_dir=$1

for sub in /scratch/09123/ofriend/moshi/grid_coding/moshiGO_*; do
  #/home1/09123/ofriend/analysis/moshigo_model/bin/prep_grid_data.py ${sub} both
  /home1/09123/ofriend/analysis/moshigo_model/bin/pull_grid_sim_values.py ${sub}
#  /home1/09123/ofriend/analysis/moshigo_model/bin/prep_grid_data.py ${sub} cone
#  /home1/09123/ofriend/analysis/moshigo_model/bin/moshi_sl_grid.py ${sub} cone gm
#  /home1/09123/ofriend/analysis/moshigo_model/bin/prep_grid_data.py ${sub} mountain
#  /home1/09123/ofriend/analysis/moshigo_model/bin/moshi_sl_grid.py ${sub} mountain gm

done