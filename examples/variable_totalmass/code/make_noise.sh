#!/bin/bash


current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/variable_totalmass"

# make noise file
generate_noise \
    --output-file $current_folder$example_folder/simulations/noise.hdf \
    --ini-file $current_folder$example_folder/code/injection.ini \
    -v