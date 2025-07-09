#!/bin/bash
#
# Smooth functional data

if [[ $# -lt 1 ]]; then
    echo ""
    exit 1
fi

sl_dir=$1

for sub in moshiGO_293 moshiGO_294 moshiGO_297 moshiGO_298 moshiGO_302 \
moshiGO_304 moshiGO_305 moshiGO_306 moshiGO_308 moshiGO_310 moshiGO_312 moshiGO_313 moshiGO_314 moshiGO_315 moshiGO_316 \
moshiGO_320 moshiGO_321 moshiGO_322 moshiGO_323 moshiGO_324 moshiGO_327 moshiGO_329 moshiGO_331 moshiGO_333 moshiGO_334 \
moshiGO_336 moshiGO_339 moshiGO_341 moshiGO_343 moshiGO_345 moshiGO_350 moshiGO_351; do

  /home1/09123/ofriend/analysis/moshigo_model/bin/prep_grid_data.py ${sub} both
  /home1/09123/ofriend/analysis/moshigo_model/bin/pull_grid_sim_values.py ${sub}

#  /home1/09123/ofriend/analysis/moshigo_model/bin/prep_grid_data.py ${sub} cone
#  /home1/09123/ofriend/analysis/moshigo_model/bin/moshi_sl_grid.py ${sub} cone gm
#  /home1/09123/ofriend/analysis/moshigo_model/bin/prep_grid_data.py ${sub} mountain
#  /home1/09123/ofriend/analysis/moshigo_model/bin/moshi_sl_grid.py ${sub} mountain gm

done