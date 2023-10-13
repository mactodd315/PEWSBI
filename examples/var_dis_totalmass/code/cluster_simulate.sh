#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate


# #generate noise
# python ~/Projects/machine_learning_sbi/PEWSBI/bin/generate_noise.py \
#     --output-folder $PWD/simulations \
#     --ini-file $PWD/code/injection2d.ini \
#     --verbose 

# generate injection parameters file
pycbc_create_injections --verbose \
    --config-files $PWD/code/injection2d.ini \
    --ninjections $2 \
    --seed 0 \
    --output-file $PWD/simulations/injection2d$1.hdf \
    --variable-params-section variable_params \
    --static-params-section static_params \
    --dist-section prior \
    --force

#generate simulation data
python ~/Projects/machine_learning_sbi/PEWSBI/bin/simulate_data.py \
    --verbose \
    --signal-length 2048\
    --delta-f 512 \
    --monitor-rate 500 \
    --injfile $PWD/simulations/injection2d$1.hdf \
    --output-folder $PWD/simulations \
    --file-name trainings5e5_$1

