#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate # change to your env dir.

current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/variable_totalmass"

# generate injection parameters file
pycbc_create_injections --verbose \
    --config-files $current_folder$example_folder/code/injection.ini \
    --ninjections 10000 \
    --seed 0 \
    --output-file $current_folder$example_folder/simulations/injection.hdf \
    --variable-params-section variable_params \
    --static-params-section static_params \
    --dist-section prior \
    --force

#generate simulation data
python $current_folder/bin/simulate_data.py \
    --verbose \
    --signal-length 2048\
    --delta-f 512 \
    --monitor-rate 50 \
    --injfile $current_folder$example_folder/simulations/injection.hdf \
    --output-file $current_folder$example_folder/simulations/training_simulations.hdf
