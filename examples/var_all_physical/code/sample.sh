#!/bin/bash

#use sbi_env environment
source ~/miniconda3/bin/activate sbi_env

current_folder="/home/mrtodd/PEWSBI"
example_folder="/examples/var_all_physical"

python $current_folder/bin/sample.py \
    --neural-net $current_folder$example_folder/neural_nets/NN_all_snpe.pickle \
    --output-file $current_folder$example_folder/samples/samples_all_snpe.hdf \
    --observation-file $current_folder$example_folder/simulations/observations.hdf \
    --config-file  $current_folder$example_folder/code/injection.ini \
    --sample-parameter 'total_mass' 'mass_ratio'\
    --observation-num 100 \
    --n-samples 10000 \
    --write-pycbc-posterior  $current_folder$example_folder/samples/post1.hdf \
    -v
    
