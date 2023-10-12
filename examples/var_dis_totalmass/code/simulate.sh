#!/bin/bash

#use sbi_env environment
source ~/miniconda3/bin/activate sbi_env


#generate noise
python ~/PEWSBI/bin/generate_noise.py \
    --output-folder $PWD/simulations \
    --ini-file $PWD/code/injection2d.ini \
    --verbose 

# generate injection parameters file
pycbc_create_injections --verbose \
    --config-files $PWD/code/injection2d.ini \
    --ninjections 100 \
    --seed 0 \
    --output-file $PWD/simulations/injection2d.hdf \
    --variable-params-section variable_params \
    --static-params-section static_params \
    --dist-section prior \
    --force

#generate simulation data
python ~/PEWSBI/bin/simulate_data.py \
    --verbose \
    --signal-length 2048\
    --delta-f 512 \
    --monitor-rate 10 \
    --injfile simulations/injection2d.hdf \
    --output-folder $PWD/simulations \
    --file-name observations2d \
    --add-noise \
    --noise-file simulations/noise.hdf

