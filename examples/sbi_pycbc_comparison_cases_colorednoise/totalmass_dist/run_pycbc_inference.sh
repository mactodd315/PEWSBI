OMP_NUM_THREADS=1 pycbc_inference \
    --config-file pycbc_inference_both.ini \
    --nprocesses 2 \
    --processing-scheme mkl \
    --output-file both_learned/pycbc_inference.hdf \
    --seed 0 \
    --force \
    --verbose

OMP_NUM_THREADS=1 pycbc_inference \
    --config-file pycbc_inference_hide_dist.ini \
    --nprocesses 2 \
    --processing-scheme mkl \
    --output-file hiding_dist/pycbc_inference.hdf \
    --seed 0 \
    --force \
    --verbose