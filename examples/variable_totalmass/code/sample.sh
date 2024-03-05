#!/bin/bash


current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI" # change to your PEWSBI dir.
example_folder="/examples/variable_totalmass"

sample \
    --neural-net $current_folder$example_folder/neural_nets/NN_totalmass2.pickle \
    --output-file $current_folder$example_folder/samples/total_mass_samples2.hdf \
    --observation-file $current_folder$example_folder/simulations/observation_simulations.hdf \
    --sample-parameters 'total_mass' \
    --observation-num 100 \
    --n-samples 10000 \
    --n-bins 500 \
    --write-pycbc-posterior $current_folder$example_folder/samples/pycbc_posterior0.hdf \
    -v