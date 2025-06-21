#!/bin/bash
#
# Smooth functional data

if [[ $# -lt 1 ]]; then
    echo ""
    exit 1
fi

sl_dir=$1

for sub in moshiGO_201 moshiGO_202 moshiGO_203 moshiGO_208 moshiGO_211 moshiGO_212 moshiGO_213 moshiGO_220 moshiGO_221 \
moshiGO_222 moshiGO_223 moshiGO_224 moshiGO_226 moshiGO_228 moshiGO_229 moshiGO_230 moshiGO_231 moshiGO_232 moshiGO_235 \
moshiGO_238 moshiGO_239 moshiGO_240 moshiGO_241 moshiGO_243 moshiGO_246 moshiGO_247 moshiGO_248 moshiGO_249 moshiGO_250 \
moshiGO_251 moshiGO_252 moshiGO_253 moshiGO_255 moshiGO_258 moshiGO_259 moshiGO_260 moshiGO_261 moshiGO_262 moshiGO_266 \
moshiGO_268 moshiGO_270 moshiGO_271 moshiGO_273 moshiGO_277 moshiGO_278 moshiGO_279 moshiGO_280 moshiGO_281 moshiGO_282 \
moshiGO_284 moshiGO_285 moshiGO_289 moshiGO_291 moshiGO_292 moshiGO_293 moshiGO_294 moshiGO_297 moshiGO_298 moshiGO_302 \
moshiGO_304 moshiGO_305 moshiGO_306 moshiGO_308 moshiGO_310 moshiGO_312 moshiGO_313 moshiGO_314 moshiGO_315 moshiGO_316 \
moshiGO_320 moshiGO_321 moshiGO_322 moshiGO_323 moshiGO_324 moshiGO_327 moshiGO_329 moshiGO_331 moshiGO_333 moshiGO_334 \
moshiGO_336 moshiGO_339 moshiGO_341 moshiGO_343 moshiGO_345 moshiGO_350 moshiGO_351; do
  /home1/09123/ofriend/analysis/moshigo_model/bin/moshi_sl_grid_last3.py ${sub}
done