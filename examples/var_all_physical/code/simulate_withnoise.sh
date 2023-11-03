#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/var_all_physical"

# #generate noise
python $current_folder/bin/generate_noise.py \
    --output-folder $current_folder$example_folder/simulations \
    --ini-file $current_folder$example_folder/code/injection.ini \
    --verbose 

# generate injection parameters file
pycbc_create_injections --verbose \
    --config-files $current_folder$example_folder/code/injection.ini \
    --ninjections 10 \
    --seed 0 \
    --output-file $current_folder$example_folder/simulations/injection.hdf \
    --variable-params-section variable_params \
    --static-params-section static_params \
    --dist-section prior \
    --force

#generate simulation data
python $current_folder/bin/simulate_data.py \
    --verbose \
    --signal-length 4096\
    --delta-f 1024 \
    --monitor-rate 1 \
    --injfile simulations/injection.hdf \
    --output-file $current_folder$example_folder/simulations/observations.hdf \
    --add-noise \
    --noise-file $current_folder$example_folder/simulations/noise.hdf \
    --snr
