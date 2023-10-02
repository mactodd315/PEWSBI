#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate


#generate noise
python ~/Projects/machine_learning_sbi/PEWSBI/bin/generate_noise.py \
    --output-file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/noise.hdf \
    --ini-file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
    --verbose 

#generate injection parameters file
pycbc_create_injections --verbose \
    --config-files ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
    --ninjections 50000 \
    --seed 0 \
    --output-file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.hdf \
    --variable-params-section variable_params \
    --static-params-section static_params \
    --dist-section prior \
    --force

#generate simulation data
python ~/Projects/machine_learning_sbi/PEWSBI/bin/simulate_data.py \
    --verbose \
    --signal-length 2048 \
    --delta-f 512 \
    --monitor-rate 100 \
    --injfile ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.hdf \
    --output_file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/training_simulations5e4.hdf
