#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/var_all_physical"

python $current_folder/bin/sample.py \
    --neural-net $current_folder$example_folder/neural_nets/NN_TS1e+04_LR5e-05_BS1e+03.pickle \
    --output-folder $current_folder$example_folder/samples \
    --observation-file $current_folder$example_folder/simulations/observations1e2.hdf \
    --config-file  $current_folder$example_folder/code/injection.ini \
    --observation-num 100 \
    --n-samples 10000 \
    --n-bins 500 \
    -v