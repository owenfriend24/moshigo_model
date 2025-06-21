#!/bin/bash
#
# Smooth functional data
subject=$1


module load afni

for sub in moshiGO_222  moshiGO_211  moshiGO_351  moshiGO_298  moshiGO_226  moshiGO_323  moshiGO_341  moshiGO_229  moshiGO_279  moshiGO_282  moshiGO_350  moshiGO_212  moshiGO_240  moshiGO_262  moshiGO_297  moshiGO_280  moshiGO_329  moshiGO_253  moshiGO_268  moshiGO_221  moshiGO_343  moshiGO_273  moshiGO_324  moshiGO_239  moshiGO_247  moshiGO_220  moshiGO_243  moshiGO_281  moshiGO_251  moshiGO_322  moshiGO_327  moshiGO_314  moshiGO_336  moshiGO_250  moshiGO_310  moshiGO_308  moshiGO_331  moshiGO_339  moshiGO_320  moshiGO_246  moshiGO_208  moshiGO_249  moshiGO_313  moshiGO_315  moshiGO_333  moshiGO_201  moshiGO_266  moshiGO_238  moshiGO_258  moshiGO_231  moshiGO_304  moshiGO_259  moshiGO_261  moshiGO_284  moshiGO_305  moshiGO_312  moshiGO_224  moshiGO_291  moshiGO_223  moshiGO_235  moshiGO_202  moshiGO_306  moshiGO_293  moshiGO_260  moshiGO_292  moshiGO_203  moshiGO_271  moshiGO_252  moshiGO_270  moshiGO_228  moshiGO_232  moshiGO_302; do
  python acf_grid.py ${sub}
  echo "ran for subject ${sub}"
done