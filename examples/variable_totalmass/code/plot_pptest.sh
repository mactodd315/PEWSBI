#!/bin/bash


current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/variable_totalmass"

plot \
    --samples-file $current_folder$example_folder/samples/total_mass_samples2.hdf \
    --output-plot   $current_folder$example_folder/plots/pptest.png \
    --plot-content 'pptest' \
    --n-trainings 10000 \
    --sample-parameters 'total_mass' \
    --num-posteriors 100

plot \
    --samples-file  $current_folder$example_folder/samples/total_mass_samples2.hdf \
    --plot-folder  $current_folder$example_folder/plots/posterior0_totalmass.png \
    --plot-content 'posterior' \
    --sample-parameter 'total_mass' \
    --posterior-index 0 \
    --plot-true