#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate


# #generate noise
# python ~/Projects/machine_learning_sbi/PEWSBI/bin/generate_noise.py \
#     --output-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/simulations \
#     --ini-file ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/code/injection1d.ini \
#     --verbose 

# # generate injection parameters file
# pycbc_create_injections --verbose \
#     --config-files ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/code/injection1d.ini \
#     --ninjections 10 \
#     --seed 0 \
#     --output-file ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/simulations/injection1d.hdf \
#     --variable-params-section variable_params \
#     --static-params-section static_params \
#     --dist-section prior \
#     --force

#generate simulation data
python ~/Projects/machine_learning_sbi/PEWSBI/bin/simulate_data.py \
    --verbose \
    --signal-length 12311 \
    --add-noise \
    --noise-file ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/simulations/noise.hdf\
    --delta-f 1024 \
    --monitor-rate 20 \
    --injfile ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/simulations/injection1d.hdf \
    --output-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/simulations \
    --file-name tests \
    --snr

