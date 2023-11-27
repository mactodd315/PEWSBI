#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/var_all_physical"

python $current_folder/bin/sample.py \
    --neural-net $current_folder$example_folder/neural_nets/NN1.pickle \
    --output-file $current_folder$example_folder/samples/samples1.hdf \
    --observation-file $current_folder$example_folder/simulations/observations.hdf \
    --config-file  $current_folder$example_folder/code/injection.ini \
    --sample-parameter 'total_mass' \
    --observation-num 1 \
    --n-samples 10000 \
    --write-pycbc-posterior  $current_folder$example_folder/samples/post1.hdf \
    -v
    
