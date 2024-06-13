OMP_NUM_THREADS=1 pycbc_inference \
    --config-file marg_time_injection.ini \
    --nprocesses 2 \
    --processing-scheme mkl \
    --output-file marg_150914.hdf \
    --seed 0 \
    --force \
    --verbose