#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate # change to your env dir.

current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/variable_totalmass"

# make noise file
python $current_folder/bin/generate_noise.py \
    --output-file $current_folder$example_folder/simulations/noise.hdf \
    --ini-file $current_folder$example_folder/code/injection.ini \
    -v