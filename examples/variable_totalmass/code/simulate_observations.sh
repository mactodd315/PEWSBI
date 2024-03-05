#!/bin/bash

current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/variable_totalmass"

# generate injection parameters file
pycbc_create_injections --verbose \
    --config-files $current_folder$example_folder/code/injection.ini \
    --ninjections 100 \
    --seed 0 \
    --output-file $current_folder$example_folder/simulations/injection.hdf \
    --variable-params-section variable_params \
    --static-params-section static_params \
    --dist-section prior \
    --force

#generate simulation data
simulate_data \
    --verbose \
    --signal-length 2048\
    --delta-f 512 \
    --monitor-rate 50 \
    --injfile $current_folder$example_folder/simulations/injection.hdf \
    --output-file $current_folder$example_folder/simulations/observation_simulations.hdf \
    --add-noise \
    --noise-file $current_folder$example_folder/simulations/noise.hdf
    # observations must have noise added in already

