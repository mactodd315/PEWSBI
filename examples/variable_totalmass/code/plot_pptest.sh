#!/bin/bash


current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/variable_totalmass"

python $current_folder/bin/plot.py \
    --samples-file $current_folder$example_folder/samples/total_mass_samples.hdf \
    --plot-folder   $current_folder$example_folder/plots \
    --plot-content 'pptest' \
    --n-trainings 10000 \
    --sample-parameters 'total_mass' \
    --num-posteriors 100

python $current_folder/bin/plot.py \
    --samples-file  $current_folder$example_folder/samples/total_mass_samples.hdf \
    --plot-folder  $current_folder$example_folder/plots \
    --plot-content 'posterior' \
    --sample-parameter 'total_mass' \
    --posterior-index 0 \
    --plot-true